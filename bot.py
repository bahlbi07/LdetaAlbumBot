import logging
import os
import threading
from datetime import timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from translations import TRANSLATIONS

load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ALBUM_PRICE_VOL4 = os.getenv("ALBUM_PRICE_VOL4", "300")
ALBUM_PRICE_OTHERS = os.getenv("ALBUM_PRICE_OTHERS", "100")
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")
PORT = int(os.environ.get('PORT', 8080))

# Channel IDs for each album. Ensure these are set in your environment variables.
CHANNEL_IDS = {
    'vol4': int(os.getenv("CHANNEL_ID_VOL_4", 0)),
    'vol3': int(os.getenv("CHANNEL_ID_VOL_3", 0)),
    'vol2': int(os.getenv("CHANNEL_ID_VOL_2", 0)),
    'vol1': int(os.getenv("CHANNEL_ID_VOL_1", 0)),
}

# --- Global variable & Logging ---
bot_app = None
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- State Definitions for Conversation ---
SELECT_LANG, SELECT_ALBUM, SELECT_LOCATION, AWAIT_PROOF, SHOW_GUIDE, SHOW_HELP = range(6)

# --- Helper Functions ---
def get_text(context: ContextTypes.DEFAULT_TYPE, key: str, **kwargs) -> str:
    lang = context.user_data.get('lang', 'ti')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, f"_{key}_").format(**kwargs)

# === CONVERSATION FLOW HANDLERS ===

# --- STAGE 1: Language Selection ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    context.user_data.clear()

    if update.callback_query:
        await update.callback_query.answer()
        try: await update.callback_query.message.delete()
        except Exception: pass
    
    keyboard = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ (ኢሮብ)", callback_data="lang_saho")],
        [InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="lang_om")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_object = update.message or (update.callback_query and update.callback_query.message)
    
    if ALBUM_ART_FILE_ID:
        await message_object.reply_photo(
            photo=ALBUM_ART_FILE_ID, 
            caption=TRANSLATIONS['en']['language_select_prompt'], # Neutral prompt
            reply_markup=reply_markup
        )
    else:
        await message_object.reply_text(TRANSLATIONS['en']['language_select_prompt'], reply_markup=reply_markup)
        
    return SELECT_LANG

# --- STAGE 2: Main Menu (Album Selection) ---
async def select_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang

    if lang == 'saho':
        # Temporary message for Saho
        await query.edit_message_text(
            text=get_text(context, 'saho_unavailable'),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")]])
        )
        return SELECT_LANG

    # Delete the language message and send a fresh main menu
    try: await query.message.delete()
    except Exception: pass

    await show_main_menu(update, context)
    return SELECT_ALBUM

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Reusable function to display the main album menu."""
    target_chat_id = update.effective_chat.id
    keyboard = [
        [InlineKeyboardButton(get_text(context, 'album_vol_4'), callback_data="select_vol4")],
        [InlineKeyboardButton(get_text(context, 'album_vol_3'), callback_data="select_vol3")],
        [InlineKeyboardButton(get_text(context, 'album_vol_2'), callback_data="select_vol2")],
        [InlineKeyboardButton(get_text(context, 'album_vol_1'), callback_data="select_vol1")],
        [InlineKeyboardButton(get_text(context, 'how_to_buy_button'), callback_data="show_guide")],
        [InlineKeyboardButton(get_text(context, 'help_button'), callback_data="help_main_menu")],
    ]
    welcome_text = get_text(context, 'welcome_message', user_name=update.effective_user.first_name)
    await context.bot.send_message(
        chat_id=target_chat_id, text=f"{welcome_text}\n\n{get_text(context, 'main_menu_prompt')}",
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML
    )
    return SELECT_ALBUM

# --- STAGE 3: Location Selection ---
async def select_album_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    album_key = query.data.split('_')[1]
    context.user_data['album_key'] = album_key
    context.user_data['album_title'] = get_text(context, f'album_{album_key}')

    keyboard = [
        [InlineKeyboardButton(get_text(context, 'location_in_button'), callback_data="location_in")],
        [InlineKeyboardButton(get_text(context, 'location_out_button'), callback_data="location_out")],
        [InlineKeyboardButton(get_text(context, 'back_button'), callback_data="back_to_main_menu")],
        [InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")],
    ]
    await query.edit_message_text(text=get_text(context, 'ask_location'), reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_LOCATION

# --- STAGE 4: Payment Instructions ---
async def select_location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'location_out':
        await query.edit_message_text(text=get_text(context, 'location_out_unavailable'))
        await asyncio.sleep(4)
        # Go back to the previous (album selection) screen
        return await show_main_menu(update, context, is_edit=True)

    album_key = context.user_data.get('album_key', 'vol4')
    price = ALBUM_PRICE_VOL4 if album_key == 'vol4' else ALBUM_PRICE_OTHERS
    album_title = context.user_data.get('album_title', '')

    payment_text = get_text(context, 'payment_instructions_ethiopia', album_title=album_title, album_price=price)
    keyboard = [
        [InlineKeyboardButton(get_text(context, 'back_button'), callback_data=f"select_{album_key}")],
        [InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")],
        [InlineKeyboardButton(get_text(context, 'help_button'), callback_data="help_payment")],
    ]
    await query.edit_message_text(text=payment_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    return AWAITING_PROOF

# --- STAGE 5: Receive and Forward Proof ---
async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    album_key = context.user_data.get('album_key', 'unknown')
    album_title = context.user_data.get('album_title', 'Unknown Album')
    admin_notif_text = get_text(context, 'admin_notification', user_mention=user.mention_html(), user_id=user.id, album_title=album_title, album_key=album_key)
    
    try:
        if update.message.text: # Transaction ID
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"{admin_notif_text}\n\n<b>Transaction ID Rec'd:</b>\n<code>{update.message.text}</code>", parse_mode=ParseMode.HTML)
        elif update.message.photo: # Screenshot
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notif_text, parse_mode=ParseMode.HTML)
            await context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=user.id, message_id=update.message.message_id)
        
        await update.message.reply_text(text=get_text(context, 'proof_received'), parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Could not notify admin: {e}")
        await update.message.reply_text(get_text(context, 'payment_rejected_user'))

    return ConversationHandler.END

# --- Special Handlers (Guide, Help) ---
async def guide_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    keyboard = [[InlineKeyboardButton(get_text(context, 'back_button'), callback_data="back_to_main_menu")]]
    await query.edit_message_text(text=get_text(context, 'guide_text'), reply_markup=InlineKeyboardMarkup(keyboard))
    return SHOW_GUIDE

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    # Determine which help text to show based on the callback data
    help_key = query.data
    keyboard = [[InlineKeyboardButton(get_text(context, 'back_button'), callback_data=context.user_data.get('last_callback', 'back_to_main_menu'))]]
    await query.edit_message_text(text=get_text(context, help_key), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    # Stays in the current state to allow 'back' button to work
    return context.user_data.get('current_state', MAIN_MENU)

# === ADMIN-ONLY COMMANDS (Outside Conversation) ===
async def approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID): return
    if len(context.args) != 2: return await update.message.reply_text(get_text(context, 'approve_usage'))
    try:
        user_id, album_key = int(context.args[0]), context.args[1].lower()
        album_title = get_text({'user_data': {'lang': 'ti'}}, f'album_{album_key}') # Title in Tigrinya
        await send_success_message(user_id, album_key, album_title)
        await update.message.reply_text(get_text(context, 'approve_success_admin', user_id=user_id, album_title=album_title))
    except Exception: await update.message.reply_text("Invalid User ID or Album Key.")

async def reject_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID): return
    if len(context.args) != 1: return await update.message.reply_text(get_text(context, 'reject_usage'))
    try:
        user_id = int(context.args[0])
        await context.bot.send_message(chat_id=user_id, text=get_text(context, 'payment_rejected_user'), parse_mode=ParseMode.HTML)
        await update.message.reply_text(get_text(context, 'rejection_success_admin', user_id=user_id))
    except Exception: await update.message.reply_text("Invalid User ID.")

# --- UTILITY Functions ---
async def send_success_message(user_id: int, album_key: str, album_title: str):
    target_channel_id = CHANNEL_IDS.get(album_key)
    if not target_channel_id:
        logging.error(f"Channel ID for key '{album_key}' not found.")
        await bot_app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"⚠️ ERROR: No Channel ID for `{album_key}`.")
        return
    try:
        # Smart Auto-Add
        await bot_app.bot.unban_chat_member(chat_id=target_channel_id, user_id=user_id)
        success = await bot_app.bot.add_chat_members(chat_id=target_channel_id, user_ids=[user_id])
        if success:
            await bot_app.bot.send_message(user_id, text=get_text({'user_data': {'lang': 'ti'}}, 'approve_success_user_auto_add', user_name=str(user_id), album_title=album_title), parse_mode=ParseMode.HTML)
        else: # Fallback to invite link
            raise BadRequest("Could not add user, likely due to privacy settings.")
    except BadRequest:
        invite_link = await bot_app.bot.create_chat_invite_link(chat_id=target_channel_id, member_limit=1)
        await bot_app.bot.send_message(user_id, text=get_text({'user_data': {'lang': 'ti'}}, 'approve_success_user_privacy', user_name=str(user_id), invite_link=invite_link.invite_link), parse_mode=ParseMode.HTML)
    
    # Schedule Feedback Request
    if bot_app.job_queue:
        bot_app.job_queue.run_once(schedule_feedback, when=timedelta(days=3), data={'user_id': user_id, 'album_title': album_title})
        await bot_app.bot.send_message(user_id, text=get_text({'user_data': {'lang': 'ti'}}, 'feedback_prompt'))


async def schedule_feedback(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    await context.bot.send_message(
        chat_id=job_data['user_id'],
        text=get_text({'user_data': {'lang': 'ti'}}, 'feedback_request', user_name="User", album_title=job_data['album_title']),
        parse_mode=ParseMode.HTML
    )

# --- Web Server for Health Check ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers(); self.wfile.write(bytes("Bot is running!", "utf-8"))
def run_web_server():
    server_address = ('', PORT); httpd = HTTPServer(server_address, HealthCheckHandler); httpd.serve_forever()

# --- MAIN FUNCTION ---
def main() -> None:
    global bot_app
    if not TELEGRAM_TOKEN or not ADMIN_CHAT_ID or not all(CHANNEL_IDS.values()):
        logging.critical("CRITICAL ERROR: One or more essential environment variables are missing."); return

    web_server_thread = threading.Thread(target=run_web_server); web_server_thread.daemon = True; web_server_thread.start()
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app = application
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            SELECT_LANG: [CallbackQueryHandler(select_language_handler, pattern="^lang_")],
            SELECT_ALBUM: [
                CallbackQueryHandler(select_album_handler, pattern="^select_vol"),
                CallbackQueryHandler(guide_handler, pattern="^show_guide$"),
                CallbackQueryHandler(help_handler, pattern="^help_main_menu$"),
            ],
            SELECT_LOCATION: [
                CallbackQueryHandler(select_location_handler, pattern="^location_"),
                CallbackQueryHandler(main_menu_handler, pattern="^back_to_main_menu$"),
            ],
            AWAITING_PROOF: [
                MessageHandler(filters.TEXT & ~filters.COMMAND | filters.PHOTO, proof_handler),
                CallbackQueryHandler(select_album_handler, pattern="^back_to_album_select$"),
                CallbackQueryHandler(help_handler, pattern="^help_payment$"),
            ],
            # Add other states like SHOW_GUIDE here if they need their own logic
        },
        fallbacks=[CallbackQueryHandler(start_command, pattern="^back_to_start$"), CommandHandler("start", start_command)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("approve", approve_command))
    application.add_handler(CommandHandler("reject", reject_command))

    logging.info("Starting bot polling..."); application.run_polling()

if __name__ == "__main__":
    main()