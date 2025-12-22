import logging, os, threading
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, 
    CallbackQueryHandler, ConversationHandler, MessageHandler, filters
)
from translations import TRANSLATIONS

# --- Config & Environment ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_CHAT_ID")
POSTER_MAIN = os.getenv("ALBUM_ART_FILE_ID")

CHANNELS = {
    'vol4': os.getenv("CHANNEL_ID_VOL_4"),
    'vol3': os.getenv("CHANNEL_ID_VOL_3"),
    'vol2': os.getenv("CHANNEL_ID_VOL_2"),
    'vol1': os.getenv("CHANNEL_ID_VOL_1"),
}

# --- States ---
SELECT_LANG, MAIN_MENU, ALBUM_INFO, PAY_PROCESS, PROOF_SECTION = range(5)

# --- Robust Translation Helper ---
def get_txt(lang, key, **kwargs):
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS['ti'])
    text = lang_dict.get(key, TRANSLATIONS['ti'].get(key, f"_{key}_"))
    try:
        if "{user_name}" in text and "user_name" not in kwargs:
            kwargs["user_name"] = "ክቡር ዓሚል"
        return text.format(**kwargs)
    except KeyError:
        return text

# --- Bot Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ቋንቋ ምረጽ - Poster shown only here"""
    context.user_data.clear()
    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"), InlineKeyboardButton("🇪🇹 Oromoo", callback_data="l_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="l_saho")]
    ]
    caption = "<b>🙏 ሰላም / Welcome / ሰላም</b>\n\nPlease select your language.\nበጃኹም ቋንቋ ምረጹ።"
    
    if update.callback_query:
        await update.callback_query.answer()
        try: await update.callback_query.message.delete()
        except: pass

    if POSTER_MAIN:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=POSTER_MAIN, 
            caption=caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=caption, 
            reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML
        )
    return SELECT_LANG

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main Menu screen"""
    query = update.callback_query; await query.answer()
    lang = query.data.split('_')[1] if 'l_' in query.data else context.user_data.get('lang', 'ti')
    context.user_data['lang'] = lang
    u_name = update.effective_user.first_name if update.effective_user else "ዓሚል"

    kb = [
        [InlineKeyboardButton(get_txt(lang, 'vol4'), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_txt(lang, 'vol3'), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_txt(lang, 'vol2'), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_txt(lang, 'vol1'), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_txt(lang, 'btn_guide'), callback_data="view_guide")],
        [InlineKeyboardButton("🌐 Change Language", callback_data="back_to_start")]
    ]
    
    msg = get_txt(lang, 'welcome_text', user_name=u_name)
    try: await query.message.delete()
    except: pass

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg, 
        reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML
    )
    return MAIN_MENU

async def album_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Album detail & Location choice"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    if "buy_" in query.data:
        context.user_data['album'] = query.data.split('_')[1]

    kb = [
        [InlineKeyboardButton(get_txt(lang, 'loc_eth'), callback_data="loc_ok")],
        [InlineKeyboardButton(get_txt(lang, 'loc_intl'), callback_data="loc_no")],
        [InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="back_to_menu")]
    ]
    await query.edit_message_text(text=get_txt(lang, 'ask_loc_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return ALBUM_INFO

async def payment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Payment Instructions"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    album = context.user_data.get('album', 'vol4')
    
    if query.data == "loc_no":
        kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="back_to_album")]]
        return await query.edit_message_text(text=get_txt(lang, 'loc_out_unavailable'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)

    price = "300" if album == "vol4" else "100"
    kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="back_to_album")]]
    msg = get_txt(lang, 'payment_instructions', album_title=album.upper(), price=price)
    await query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return PROOF_SECTION

async def guide_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guide view"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data="back_to_menu")]]
    await query.edit_message_text(text=get_txt(lang, 'full_guide'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MAIN_MENU

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive proof and alert admin"""
    lang = context.user_data['lang']
    user = update.effective_user
    album = context.user_data.get('album', 'N/A')
    
    await update.message.reply_text(get_txt(lang, 'proof_received_msg'), parse_mode=ParseMode.HTML)
    
    admin_kb = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"adm_ok_{user.id}_{album}")],
        [InlineKeyboardButton("❌ Reject", callback_data=f"adm_no_{user.id}")]
    ]
    alert = f"💎 <b>New Purchase!</b>\n👤 User: {user.mention_html()}\n🆔 ID: <code>{user.id}</code>\n💿 Album: <b>{album.upper()}</b>"
    
    await context.bot.send_message(ADMIN_ID, alert, parse_mode=ParseMode.HTML)
    if update.message.photo: await update.message.forward(ADMIN_ID)
    elif update.message.text: await context.bot.send_message(ADMIN_ID, f"💬 Message: {update.message.text}")
    await context.bot.send_message(ADMIN_ID, "👇 Admin Action:", reply_markup=InlineKeyboardMarkup(admin_kb))
    return ConversationHandler.END

async def admin_action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    data = query.data.split('_') # adm, ok/no, uid, album
    action, target_uid = data[1], int(data[2])
    
    if action == "ok":
        album_key = data[3]
        try:
            invite = await context.bot.create_chat_invite_link(chat_id=CHANNELS[album_key], member_limit=1)
            await context.bot.send_message(target_uid, get_txt('ti', 'success_user_msg', album_title=album_key.upper()), parse_mode=ParseMode.HTML)
            await context.bot.send_message(target_uid, f"🎁 <b>Access Link:</b> {invite.invite_link}\n\n{get_txt('ti', 'feedback_link')}", parse_mode=ParseMode.HTML)
            await query.edit_message_text(f"✅ User {target_uid} Approved for {album_key}")
        except Exception as e: await query.edit_message_text(f"❌ Error: {str(e)}")
    else:
        await context.bot.send_message(target_uid, "❌ Payment not verified. / ክፍሊትኩም ኣይተረጋገጸን።", parse_mode=ParseMode.HTML)
        await query.edit_message_text(f"❌ Rejected User {target_uid}")

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(start, pattern="back_to_start")],
        states={
            SELECT_LANG: [CallbackQueryHandler(menu_handler, pattern="^l_")],
            MAIN_MENU: [
                CallbackQueryHandler(album_select, pattern="^buy_"),
                CallbackQueryHandler(guide_view, pattern="view_guide"),
                CallbackQueryHandler(start, pattern="back_to_start")
            ],
            ALBUM_INFO: [
                CallbackQueryHandler(payment_info, pattern="^loc_"),
                CallbackQueryHandler(menu_handler, pattern="back_to_menu")
            ],
            PROOF_SECTION: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, proof_handler),
                CallbackQueryHandler(album_select, pattern="back_to_album")
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_action_handler, pattern="^adm_"))
    app.run_polling()

if __name__ == "__main__": main()