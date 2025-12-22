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

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# --- States ---
LANG_STAGE, WELCOME_STAGE, MENU_STAGE, LOCATION_STAGE, PROOF_STAGE = range(5)

def get_text(lang, key, **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, f"_{key}_")
    if "{user_name}" in text and "user_name" not in kwargs:
        kwargs["user_name"] = "ክቡር ዓሚል"
    return text.format(**kwargs)

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requirement 1: Poster + Language Selection Only"""
    context.user_data.clear()
    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"), InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="l_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ (ኢሮብ)", callback_data="l_saho")]
    ]
    if update.callback_query:
        await update.callback_query.answer()
        try: await update.callback_query.message.delete()
        except: pass

    caption = "Please choose your language / በጃኹም ቋንቋ ምረጹ / እባክዎ ቋንቋ ይምረጡ"
    if POSTER:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=POSTER, caption=caption, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=caption, reply_markup=InlineKeyboardMarkup(kb))
    return LANG_STAGE

async def welcome_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requirement 2: After Lang -> Welcome Msg + Poster"""
    query = update.callback_query; await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    u_name = update.effective_user.first_name

    kb = [[InlineKeyboardButton(get_text(lang, 'btn_continue'), callback_data="to_menu")]]
    text = get_text(lang, 'welcome_msg', user_name=u_name)
    
    await query.message.delete()
    if POSTER:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=POSTER, caption=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return WELCOME_STAGE

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requirement 3: Detailed Menu"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    
    kb = [
        [InlineKeyboardButton(get_text(lang, 'vol4_btn'), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_text(lang, 'vol3_btn'), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_text(lang, 'vol2_btn'), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_text(lang, 'vol1_btn'), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_text(lang, 'btn_guide'), callback_data="view_guide")],
        [InlineKeyboardButton(get_text(lang, 'btn_help'), callback_data="help_main")],
        [InlineKeyboardButton(get_text(lang, 'btn_back_lang'), callback_data="back_to_start")]
    ]
    
    msg = get_text(lang, 'menu_prompt')
    # Keep poster in menu for beauty (as per req 2)
    if query.message.photo:
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    else:
        await query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU_STAGE

async def select_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requirement 4: Location Options + Detailed Text"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    if "buy_" in query.data:
        context.user_data['album'] = query.data.split('_')[1]
    
    kb = [
        [InlineKeyboardButton(get_text(lang, 'loc_in'), callback_data="loc_et")],
        [InlineKeyboardButton(get_text(lang, 'loc_out'), callback_data="loc_os")],
        [InlineKeyboardButton(get_text(lang, 'btn_back_menu'), callback_data="to_menu")],
        [InlineKeyboardButton(get_text(lang, 'btn_back_lang'), callback_data="back_to_start")]
    ]
    text = get_text(lang, 'ask_loc_text')
    await query.edit_message_caption(caption=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return LOCATION_STAGE

async def payment_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requirement 5: Bank Info + 🙋‍♂️ Hello Professional Text"""
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    album = context.user_data['album']

    if query.data == "loc_os":
        kb = [[InlineKeyboardButton(get_text(lang, 'btn_back_menu'), callback_data="to_menu")], [InlineKeyboardButton(get_text(lang, 'btn_back_lang'), callback_data="back_to_start")]]
        await query.edit_message_caption(caption=get_text(lang, 'loc_out_unavailable'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        return LOCATION_STAGE

    price = "300" if album == "vol4" else "100"
    kb = [
        [InlineKeyboardButton(get_text(lang, 'btn_help'), callback_data="help_pay")],
        [InlineKeyboardButton(get_text(lang, 'btn_back_menu'), callback_data="to_menu")]
    ]
    msg = get_text(lang, 'payment_instructions', album_title=album.upper(), price=price)
    await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return PROOF_STAGE

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    help_type = query.data.split('_')[1] # main or pay
    kb = [[InlineKeyboardButton(get_text(lang, 'btn_back_menu'), callback_data="to_menu")]]
    await query.edit_message_caption(caption=get_text(lang, f'help_text_{help_type}'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU_STAGE

async def guide_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    lang = context.user_data['lang']
    kb = [[InlineKeyboardButton(get_text(lang, 'btn_back_menu'), callback_data="to_menu")], [InlineKeyboardButton(get_text(lang, 'btn_back_lang'), callback_data="back_to_start")]]
    await query.edit_message_caption(caption=get_text(lang, 'full_guide'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU_STAGE

async def receive_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requirement 5 & 6: Proof Handling & Admin Alert"""
    lang = context.user_data.get('lang', 'ti')
    user = update.effective_user
    album = context.user_data.get('album', 'N/A')
    
    await update.message.reply_text(get_text(lang, 'proof_received_msg'), parse_mode=ParseMode.HTML)
    
    admin_kb = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"adm_ok_{user.id}_{album}")],
        [InlineKeyboardButton("❌ Reject", callback_data=f"adm_no_{user.id}")]
    ]
    alert = f"🔔 <b>New Purchase!</b>\nUser: {user.mention_html()}\nID: <code>{user.id}</code>\nAlbum: {album}"
    await context.bot.send_message(ADMIN_ID, alert, parse_mode=ParseMode.HTML)
    if update.message.photo: await update.message.forward(ADMIN_ID)
    elif update.message.text: await context.bot.send_message(ADMIN_ID, f"💬 Text: {update.message.text}")
    await context.bot.send_message(ADMIN_ID, "Action:", reply_markup=InlineKeyboardMarkup(admin_kb))
    return ConversationHandler.END

async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Requirement 6 & 11: Auto-add / Success Msg / Privacy Link"""
    query = update.callback_query; await query.answer()
    _, action, uid, *album_info = query.data.split('_')
    uid = int(uid)
    
    if action == "ok":
        album = album_info[0]
        try:
            # Auto-add Logic (Bot must be admin)
            invite = await context.bot.create_chat_invite_link(CHANNELS[album], member_limit=1)
            # Success Message
            await context.bot.send_message(uid, get_text('ti', 'success_final'), parse_mode=ParseMode.HTML)
            # Link/Privacy Message
            msg = get_text('ti', 'privacy_link_msg', user_name="ዓሚል", album_title=album.upper(), invite_link=invite.invite_link)
            await context.bot.send_message(uid, msg, parse_mode=ParseMode.HTML)
            # Requirement 9: Feedback
            await context.bot.send_message(uid, get_text('ti', 'feedback_msg'), parse_mode=ParseMode.HTML)
            await query.edit_message_text(f"✅ Approved {uid}")
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {str(e)}")
    else:
        await context.bot.send_message(uid, "❌ Payment Rejected. Contact @Dmtsibereket.")
        await query.edit_message_text(f"❌ Rejected {uid}")

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(start, pattern="back_to_start")],
        states={
            LANG_STAGE: [CallbackQueryHandler(welcome_screen, pattern="^l_")],
            WELCOME_STAGE: [CallbackQueryHandler(main_menu, pattern="to_menu")],
            MENU_STAGE: [
                CallbackQueryHandler(select_location, pattern="^buy_"),
                CallbackQueryHandler(guide_handler, pattern="view_guide"),
                CallbackQueryHandler(help_handler, pattern="^help_"),
                CallbackQueryHandler(start, pattern="back_to_start")
            ],
            LOCATION_STAGE: [
                CallbackQueryHandler(payment_page, pattern="^loc_"),
                CallbackQueryHandler(main_menu, pattern="to_menu"),
                CallbackQueryHandler(start, pattern="back_to_start")
            ],
            PROOF_STAGE: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, receive_proof),
                CallbackQueryHandler(help_handler, pattern="^help_"),
                CallbackQueryHandler(main_menu, pattern="to_menu")
            ]
        },
        fallbacks=[CommandHandler("start", start), CallbackQueryHandler(start, pattern="back_to_start")]
    )
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_action, pattern="^adm_"))
    app.run_polling()

if __name__ == "__main__": main()