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
POSTER_MAIN = os.getenv("ALBUM_ART_FILE_ID")
CHANNELS = {
    'vol4': os.getenv("CHANNEL_ID_VOL_4"),
    'vol3': os.getenv("CHANNEL_ID_VOL_3"),
    'vol2': os.getenv("CHANNEL_ID_VOL_2"),
    'vol1': os.getenv("CHANNEL_ID_VOL_1"),
}

# --- States ---
SELECT_LANG, MAIN_MENU, ALBUM_INFO, PAY_PROCESS, PROOF_SECTION = range(5)

def get_txt(lang, key, **kwargs):
    return TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, f"_{key}_").format(**kwargs)

# --- Logic ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """100X Start: ቋንቋ ምረጽ"""
    context.user_data.clear()
    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"), InlineKeyboardButton("🇪🇹 Oromoo", callback_data="l_om")]
    ]
    caption = "<b>🙏 ሰላም / Welcome</b>\n\nበጃኹም ቋንቋ ምረጹ / Please select your language."
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.delete()

    if POSTER_MAIN:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=POSTER_MAIN, caption=caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return SELECT_LANG

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ቀንዲ ገጽ: ኩሉ ገጽ ናብዚ ይመለስ"""
    query = update.callback_query; await query.answer()
    lang = query.data.split('_')[1] if 'l_' in query.data else context.user_data.get('lang', 'ti')
    context.user_data['lang'] = lang

    kb = [
        [InlineKeyboardButton(get_txt(lang, 'vol4'), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_txt(lang, 'vol3'), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_txt(lang, 'vol2'), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_txt(lang, 'vol1'), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_txt(lang, 'btn_guide'), callback_data="view_guide")],
        [InlineKeyboardButton("🌐 Change Language", callback_data="back_to_start")]
    ]
    
    # እቲ ስእሊ ኣብ ኩሉ ገጽ ከይመጽእ፣ እቲ ናይ መጀመሪያ መልእኽቲ ዲሊት ንገብሮ
    try: await query.message.delete()
    except: pass

    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_txt(lang, 'welcome_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MAIN_MENU

async def album_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ምርጫ ኣልበም"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    album = query.data.split('_')[1]
    context.user_data['album'] = album

    kb = [
        [InlineKeyboardButton(get_txt(lang, 'loc_eth'), callback_data="loc_ok")],
        [InlineKeyboardButton(get_txt(lang, 'loc_intl'), callback_data="loc_no")],
        [InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data=f"l_{lang}")]
    ]
    await query.edit_message_text(text=get_txt(lang, 'ask_loc_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return ALBUM_INFO

async def payment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ክፍሊት"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    
    if query.data == "loc_no":
        kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data=f"buy_{context.user_data['album']}")]]
        return await query.edit_message_text(text=get_txt(lang, 'loc_out_unavailable'), reply_markup=InlineKeyboardMarkup(kb))

    album = context.user_data['album']
    price = "300" if album == "vol4" else "100"
    
    kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data=f"buy_{album}")]]
    msg = get_txt(lang, 'payment_instructions', album_title=album.upper(), price=price)
    await query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return PROOF_SECTION

async def guide_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """መምርሒ"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    kb = [[InlineKeyboardButton(get_txt(lang, 'btn_back'), callback_data=f"l_{lang}")]]
    await query.edit_message_text(text=get_txt(lang, 'full_guide'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MAIN_MENU

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """መረጋገጺ ንኣድሚን ብተንቀሳቃሲ በተን ምስዳድ"""
    lang = context.user_data['lang']
    user = update.effective_user
    album = context.user_data['album']
    
    # መጀመሪያ ንተጠቃሚ መልእኽቲ
    await update.message.reply_text(get_txt(lang, 'proof_received_msg'), parse_mode=ParseMode.HTML)
    
    # ንኣድሚን ብተንቀሳቃሲ በተን (Inline Buttons)
    admin_kb = [
        [InlineKeyboardButton("✅ Approve (አጽድቅ)", callback_data=f"adm_ok_{user.id}_{album}")],
        [InlineKeyboardButton("❌ Reject (ሰርዝ)", callback_data=f"adm_no_{user.id}")]
    ]
    
    alert = f"💎 <b>New Purchase!</b>\n👤 User: {user.mention_html()}\n🆔 ID: <code>{user.id}</code>\n💿 Album: <b>{album.upper()}</b>"
    
    await context.bot.send_message(ADMIN_ID, alert, parse_mode=ParseMode.HTML)
    if update.message.photo: await update.message.forward(ADMIN_ID)
    elif update.message.text: await context.bot.send_message(ADMIN_ID, f"💬 ID/Text: {update.message.text}")
    
    await context.bot.send_message(ADMIN_ID, "👇 Control Panel:", reply_markup=InlineKeyboardMarkup(admin_kb))
    return ConversationHandler.END

# --- Admin Button Action ---
async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    data = query.data.split('_')
    action = data[1] # ok or no
    target_uid = int(data[2])
    
    if action == "ok":
        album = data[3]
        try:
            invite = await context.bot.create_chat_invite_link(chat_id=CHANNELS[album], member_limit=1)
            await context.bot.send_message(target_uid, get_txt('ti', 'success_user_msg', album_title=album.upper()), parse_mode=ParseMode.HTML)
            await context.bot.send_message(target_uid, f"🔗 Link: {invite.invite_link}")
            await query.edit_message_text(f"✅ Approved for {target_uid}")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {str(e)}")
    else:
        await context.bot.send_message(target_uid, "❌ ይቕሬታ ክፍሊትኩም ኣይተረጋገጸን። / Sorry, payment not verified.")
        await query.edit_message_text(f"❌ Rejected user {target_uid}")

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
                CallbackQueryHandler(menu_handler, pattern="^l_")
            ],
            PROOF_SECTION: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, proof_handler),
                CallbackQueryHandler(album_select, pattern="^buy_")
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )
    
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_buttons, pattern="^adm_"))
    app.run_polling()

if __name__ == "__main__": main()