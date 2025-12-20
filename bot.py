import logging, os, threading
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, 
    CallbackQueryHandler, ConversationHandler, MessageHandler, filters
)
from translations import TRANSLATIONS

load_dotenv()

# --- Config & Environment ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_CHAT_ID")
POSTER = os.getenv("ALBUM_ART_FILE_ID")
CHANNELS = {
    'vol4': int(os.getenv("CHANNEL_ID_VOL_4", 0)),
    'vol3': int(os.getenv("CHANNEL_ID_VOL_3", 0)),
    'vol2': int(os.getenv("CHANNEL_ID_VOL_2", 0)),
    'vol1': int(os.getenv("CHANNEL_ID_VOL_1", 0)),
}

# --- States ---
(CHOOSING_LANG, GREETING, NAVIGATING_MENU, SELECTING_LOC, 
 UPLOADING_PROOF, VIEWING_GUIDE, VIEWING_HELP) = range(7)

def t(lang, key, **kwargs):
    """Dynamic Translation Helper"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, f"_{key}_").format(**kwargs)

# --- Logic Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """[100X START] Poster + Multi-Language Grid"""
    context.user_data.clear()
    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"), InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="l_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="l_saho")]
    ]
    caption = "<b>🙏 ሰላም / Welcome / ሰላም</b>\n\nChoose your language to begin this spiritual journey.\nንኽትጅምር ቋንቋ ምረጽ። / ለመጀመር ቋንቋ ይምረጡ።"
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.edit_caption(caption=caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    else:
        if POSTER: await update.message.reply_photo(photo=POSTER, caption=caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        else: await update.message.reply_text(caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return CHOOSING_LANG

async def welcome_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """[100X WELCOME] Spiritual Greeting"""
    query = update.callback_query; await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    
    kb = [[InlineKeyboardButton(t(lang, 'btn_enter'), callback_data="menu"), InlineKeyboardButton(t(lang, 'btn_back'), callback_data="start")]]
    text = t(lang, 'welcome_text', name=update.effective_user.first_name)
    await query.edit_message_caption(caption=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return GREETING

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """[100X MENU] Modern Album Store Layout"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    
    kb = [
        [InlineKeyboardButton(t(lang, 'vol4'), callback_data="buy_vol4")],
        [InlineKeyboardButton(t(lang, 'vol3'), callback_data="buy_vol3"), InlineKeyboardButton(t(lang, 'vol2'), callback_data="buy_vol2")],
        [InlineKeyboardButton(t(lang, 'vol1'), callback_data="buy_vol1"), InlineKeyboardButton(t(lang, 'btn_guide'), callback_data="guide")],
        [InlineKeyboardButton(t(lang, 'btn_help'), callback_data="help"), InlineKeyboardButton(t(lang, 'btn_lang'), callback_data="start")]
    ]
    await query.edit_message_caption(caption=t(lang, 'menu_prompt'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return NAVIGATING_MENU

async def album_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """[100X LOCATION] Intelligent Geo-Check"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    context.user_data['album'] = query.data.split('_')[1]
    
    kb = [
        [InlineKeyboardButton(t(lang, 'loc_eth'), callback_data="loc_ok"), InlineKeyboardButton(t(lang, 'loc_intl'), callback_data="loc_no")],
        [InlineKeyboardButton(t(lang, 'btn_back'), callback_data="menu")]
    ]
    await query.edit_message_caption(caption=t(lang, 'loc_prompt'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return SELECTING_LOC

async def payment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """[100X PAYMENT] Clear Financial Instructions"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    
    if query.data == "loc_no":
        kb = [[InlineKeyboardButton(t(lang, 'btn_back'), callback_data="menu")]]
        return await query.edit_message_caption(caption=t(lang, 'intl_err'), reply_markup=InlineKeyboardMarkup(kb))

    album = context.user_data['album']
    price = "300" if album == "vol4" else "100"
    kb = [[InlineKeyboardButton(t(lang, 'btn_help'), callback_data="help"), InlineKeyboardButton(t(lang, 'btn_back'), callback_data="menu")]]
    
    msg = t(lang, 'pay_instr', album=album.upper(), price=price)
    await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return UPLOADING_PROOF

async def handle_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """[100X PROOF] Robust Submission & Admin Alert"""
    lang = context.user_data['lang']
    user = update.effective_user
    album = context.user_data['album']
    
    # Notify Admin
    alert = f"💎 <b>New Purchase Request!</b>\n👤 User: {user.mention_html()}\n🆔 ID: <code>{user.id}</code>\n💿 Album: <b>{album.upper()}</b>\n\nApprove: `/approve {user.id} {album}`"
    await context.bot.send_message(ADMIN_ID, alert, parse_mode=ParseMode.HTML)
    if update.message.photo: await update.message.forward(ADMIN_ID)
    elif update.message.text: await context.bot.send_message(ADMIN_ID, f"💬 Trans ID: <code>{update.message.text}</code>", parse_mode=ParseMode.HTML)

    await update.message.reply_text(t(lang, 'proof_done'), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

# --- Navigation Helpers ---

async def show_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    kb = [[InlineKeyboardButton(t(lang, 'btn_back'), callback_data="menu")]]
    await query.edit_message_caption(caption=t(lang, 'guide_content'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return NAVIGATING_MENU

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    kb = [[InlineKeyboardButton(t(lang, 'btn_back'), callback_data="menu")]]
    await query.edit_message_caption(caption=t(lang, 'help_content'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return NAVIGATING_MENU

# --- Admin Core ---

async def approve_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != str(ADMIN_ID): return
    try:
        uid, vol = int(context.args[0]), context.args[1]
        link = await context.bot.create_chat_invite_link(CHANNELS[vol], member_limit=1)
        # 100X Success Message
        await context.bot.send_message(uid, t('ti', 'user_success', album=vol.upper()), parse_mode=ParseMode.HTML)
        await context.bot.send_message(uid, f"🎁 <b>Your Link:</b> {link.invite_link}\n\n{t('ti', 'feedback_link')}", parse_mode=ParseMode.HTML)
        await update.message.reply_text(f"✅ User {uid} approved for {vol}")
    except Exception as e: await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_LANG: [CallbackQueryHandler(welcome_screen, pattern="^l_")],
            GREETING: [CallbackQueryHandler(main_menu, pattern="menu"), CallbackQueryHandler(start, pattern="start")],
            NAVIGATING_MENU: [
                CallbackQueryHandler(album_selected, pattern="^buy_"),
                CallbackQueryHandler(show_guide, pattern="guide"),
                CallbackQueryHandler(show_help, pattern="help"),
                CallbackQueryHandler(start, pattern="start")
            ],
            SELECTING_LOC: [
                CallbackQueryHandler(payment_info, pattern="^loc_"),
                CallbackQueryHandler(main_menu, pattern="menu")
            ],
            UPLOADING_PROOF: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_proof),
                CallbackQueryHandler(show_help, pattern="help"),
                CallbackQueryHandler(main_menu, pattern="menu")
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )
    
    app.add_handler(conv)
    app.add_handler(CommandHandler("approve", approve_logic))
    app.run_polling()

if __name__ == "__main__": main()