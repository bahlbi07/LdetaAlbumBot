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

# --- Config ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_CHAT_ID")
POSTER = os.getenv("ALBUM_ART_FILE_ID")
CHANNELS = {
    'vol4': os.getenv("CHANNEL_ID_VOL_4"),
    'vol3': os.getenv("CHANNEL_ID_VOL_3"),
    'vol2': os.getenv("CHANNEL_ID_VOL_2"),
    'vol1': os.getenv("CHANNEL_ID_VOL_1"),
}

# --- Logic States ---
SELECT_LANG, GREETING, MENU, LOCATION, PAYMENT = range(5)

def get_txt(lang, key, **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, f"_{key}_")
    if "{user_name}" in text and "user_name" not in kwargs:
        kwargs["user_name"] = "ክቡር ዓሚል"
    return text.format(**kwargs)

# --- Core Logic ---

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """1. ቋንቋ ጥራይ ምስ ፖስተር"""
    context.user_data.clear()
    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"), InlineKeyboardButton("🇪🇹 Oromoo", callback_data="l_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="l_saho")]
    ]
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.delete()

    cap = "Please select your language / በጃኹም ቋንቋ ምረጹ"
    if POSTER:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=POSTER, caption=cap, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=cap, reply_markup=InlineKeyboardMarkup(kb))
    return SELECT_LANG

async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """2. እንኳዕ ብደሓን መጻእካ"""
    query = update.callback_query; await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    u_name = update.effective_user.first_name

    kb = [[InlineKeyboardButton(get_txt(lang, 'btn_continue'), callback_data="go_menu")]]
    txt = get_txt(lang, 'welcome_text', user_name=u_name)
    
    await query.edit_message_caption(caption=txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return GREETING

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """3. ዝርዝር ኣልበማት"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    
    kb = [
        [InlineKeyboardButton(get_txt(lang, 'vol4'), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_txt(lang, 'vol3'), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_txt(lang, 'vol2'), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_txt(lang, 'vol1'), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_txt(lang, 'btn_guide'), callback_data="guide")],
        [InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="restart")]
    ]
    await query.edit_message_caption(caption=get_txt(lang, 'main_menu_prompt'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU

async def location_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """4. ምርጫ ቦታ"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    if "buy_" in query.data:
        context.user_data['album'] = query.data.split('_')[1]
    
    kb = [
        [InlineKeyboardButton(get_txt(lang, 'loc_eth'), callback_data="loc_ok")],
        [InlineKeyboardButton(get_txt(lang, 'loc_intl'), callback_data="loc_no")],
        [InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="go_menu")]
    ]
    await query.edit_message_caption(caption=get_txt(lang, 'ask_loc_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return LOCATION

async def payment_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """5. ክፍሊት"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    
    if query.data == "loc_no":
        kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="go_menu")]]
        await query.edit_message_caption(caption=get_txt(lang, 'loc_out_unavailable'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        return LOCATION

    album = context.user_data['album']
    price = "300" if album == "vol4" else "100"
    kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data=f"buy_{album}")]]
    msg = get_txt(lang, 'payment_instructions', album_title=album.upper(), price=price)
    
    await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return PAYMENT

async def guide_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """መምርሒ ገጽ"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="go_menu")]]
    await query.edit_message_caption(caption=get_txt(lang, 'full_guide'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """መረጋገጺ"""
    lang = context.user_data['lang']
    user = update.effective_user
    album = context.user_data['album']
    
    await update.message.reply_text(get_txt(lang, 'proof_received_msg'), parse_mode=ParseMode.HTML)
    
    admin_kb = [[InlineKeyboardButton("✅ Approve", callback_data=f"adm_ok_{user.id}_{album}"), InlineKeyboardButton("❌ Reject", callback_data=f"adm_no_{user.id}")]]
    alert = f"🔔 <b>New!</b>\nUser: {user.mention_html()}\nID: <code>{user.id}</code>\nAlbum: {album}"
    await context.bot.send_message(ADMIN_ID, alert, parse_mode=ParseMode.HTML)
    if update.message.photo: await update.message.forward(ADMIN_ID)
    elif update.message.text: await context.bot.send_message(ADMIN_ID, f"ID: {update.message.text}")
    await context.bot.send_message(ADMIN_ID, "Action:", reply_markup=InlineKeyboardMarkup(admin_kb))
    return ConversationHandler.END

async def admin_btns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    _, act, uid, *ext = query.data.split('_')
    uid = int(uid)
    
    if act == "ok":
        alb = ext[0]
        link = await context.bot.create_chat_invite_link(CHANNELS[alb], member_limit=1)
        await context.bot.send_message(uid, get_txt('ti', 'success_user_msg', album_title=alb.upper()), parse_mode=ParseMode.HTML)
        await context.bot.send_message(uid, f"🎁 Link: {link.invite_link}\n\n{get_txt('ti', 'feedback_link')}", parse_mode=ParseMode.HTML)
        await query.edit_message_text(f"✅ Approved {uid}")
    else:
        await context.bot.send_message(uid, "❌ Rejected.")
        await query.edit_message_text(f"❌ Rejected {uid}")

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start_cmd), CallbackQueryHandler(start_cmd, pattern="restart")],
        states={
            SELECT_LANG: [CallbackQueryHandler(welcome_handler, pattern="^l_")],
            GREETING: [CallbackQueryHandler(main_menu, pattern="go_menu"), CallbackQueryHandler(start_cmd, pattern="restart")],
            MENU: [
                CallbackQueryHandler(location_select, pattern="^buy_"),
                CallbackQueryHandler(guide_screen, pattern="guide"),
                CallbackQueryHandler(start_cmd, pattern="restart")
            ],
            LOCATION: [
                CallbackQueryHandler(payment_screen, pattern="^loc_"),
                CallbackQueryHandler(main_menu, pattern="go_menu")
            ],
            PAYMENT: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, proof_handler),
                CallbackQueryHandler(location_select, pattern="^buy_")
            ]
        },
        fallbacks=[CommandHandler("start", start_cmd)]
    )
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_btns, pattern="^adm_"))
    app.run_polling()

if __name__ == "__main__": main()