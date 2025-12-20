import logging
import os
import threading
import asyncio
from datetime import timedelta
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
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

# Import our brand new translations file
from translations import TRANSLATIONS

# Load environment variables from .env file
load_dotenv()

# --- Configurations ---
# These must be set in your Railway variables / .env file
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID") # Admin's unique Chat ID for receiving notifications
ALBUM_PRICE_VOL4 = os.getenv("ALBUM_PRICE_VOL4", "300")
ALBUM_PRICE_OTHERS = os.getenv("ALBUM_PRICE_OTHERS", "100")
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")
PORT = int(os.environ.get('PORT', 8080))
# Channel IDs for each album
CHANNEL_IDS = {
    'vol4': int(os.getenv("CHANNEL_ID_VOL_4")),
    'vol3': int(os.getenv("CHANNEL_ID_VOL_3")),
    'vol2': int(os.getenv("CHANNEL_ID_VOL_2")),
    'vol1': int(os.getenv("CHANNEL_ID_VOL_1")),
}

# --- Global variable to hold the application instance for background jobs ---
bot_app = None

# --- Logging Setup ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- Conversation Handler States ---
LANG_SELECT, MAIN_MENU, PAYMENT_INFO, AWAITING_PROOF = range(4)

# --- Helper Functions ---
def get_text(context: ContextTypes.DEFAULT_TYPE, key: str, **kwargs) -> str:
    """Gets translated text using the language stored in user_data."""
    lang_code = context.user_data.get('lang', 'ti') # Default to Tigrinya if not set
    lang_dict = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])
    text = lang_dict.get(key)
    if text is None: # Fallback to English if key is missing in the current language
        text = TRANSLATIONS['en'].get(key, f"_{key}_")
    return text.format(**kwargs)

# --- BOT HANDLERS START HERE ---

# 1. Start of Conversation: Language Selection
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    context.user_data.clear()

    # If the user clicked a "back" button, we handle it smoothly
    if update.callback_query:
        await update.callback_query.answer()
        # Clean up the chat by deleting the old message
        try: await update.callback_query.message.delete()
        except Exception: pass

    keyboard = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ (ኢሮብ)", callback_data="lang_saho")],
        [InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="lang_om")]
    ]
    
    welcome_text = TRANSLATIONS['ti']['welcome_language'].format(user_name=user.first_name)
    
    # Send the album art only on a fresh /start, not from a back button
    if ALBUM_ART_FILE_ID and not update.callback_query:
        await update.message.reply_photo(
            photo=ALBUM_ART_FILE_ID,
            caption=welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    else: # If no album art or coming from 'back', send text
        await update.message.reply_text(text=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
        
    return LANG_SELECT

# 2. After Language is Selected: Main Album Menu
async def language_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    lang_code = query.data.split('_')[1]
    context.user_data['lang'] = lang_code
    
    if lang_code == 'saho': # Saho language is not ready yet
        keyboard = [[InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")]]
        await query.edit_message_text(text=get_text(context, 'saho_unavailable'), reply_markup=InlineKeyboardMarkup(keyboard))
        return LANG_SELECT # Stay here until they choose another language
    
    # All other languages go to the main menu
    return await main_menu_handler(update, context)


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    # It might not be a query if we are coming from another state
    if query:
        await query.answer()

    # Build the main menu keyboard
    keyboard = [
        [InlineKeyboardButton(get_text(context, 'album_vol_4'), callback_data="select_vol4")],
        [InlineKeyboardButton(get_text(context, 'album_vol_3'), callback_data="select_vol3")],
        [InlineKeyboardButton(get_text(context, 'album_vol_2'), callback_data="select_vol2")],
        [InlineKeyboardButton(get_text(context, 'album_vol_1'), callback_data="select_vol1")],
        [InlineKeyboardButton(get_text(context, 'how_to_buy_button'), callback_data="guide")],
        [InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")],
        [InlineKeyboardButton(get_text(context, 'help_button'), callback_data="help_main")]
    ]
    
    target_message = query.message if query else update.message
    await target_message.edit_text(
        text=get_text(context, 'main_menu'),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return MAIN_MENU
    
# 3. Album Selected: Show Payment Instructions
async def album_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    album_key = query.data.split('_')[1] # e.g., 'vol4'
    context.user_data['album_key'] = album_key
    
    price = ALBUM_PRICE_VOL4 if album_key == 'vol4' else ALBUM_PRICE_OTHERS
    album_title = get_text(context, f'album_{album_key}')
    
    context.user_data['album_title'] = album_title # Store for later use
    
    payment_text = get_text(context, 'payment_instructions', album_title=album_title, album_price=price)

    keyboard = [
        [InlineKeyboardButton(get_text(context, 'back_to_main_menu_button'), callback_data="back_to_main_menu")],
        [InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")],
        [InlineKeyboardButton(get_text(context, 'help_button'), callback_data="help_payment")]
    ]
    
    await query.edit_message_text(text=payment_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    return AWAITING_PROOF

# 4. User sends Transaction ID (text) or Screenshot (photo)
async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    lang_code = context.user_data.get('lang', 'ti')
    album_title = context.user_data.get('album_title', 'Unknown Album')
    album_key = context.user_data.get('album_key', 'unknown')

    admin_notif_text = get_text(context, 'payment_notif_admin', user_mention=user.mention_html(), user_id=user.id, album_title=album_title, album_key=album_key)
    
    try:
        if update.message.text: # If they sent a Transaction ID
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"{admin_notif_text}\n\n<b>Transaction ID:</b>\n<code>{update.message.text}</code>", parse_mode=ParseMode.HTML)
        elif update.message.photo: # If they sent a screenshot
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notif_text, parse_mode=ParseMode.HTML)
            await context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=user.id, message_id=update.message.message_id)
        
        # Confirm to the user that we are waiting for the admin
        await update.message.reply_text(text=get_text(context, 'slip_received'), parse_mode=ParseMode.HTML)
    
    except Exception as e:
        logging.error(f"Could not notify admin: {e}")
        await update.message.reply_text(get_text(lang_code, 'payment_rejected_user'))

    # End the conversation here and wait for the admin's action
    return ConversationHandler.END


# --- ADMIN-ONLY COMMANDS (called outside the conversation) ---
async def approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID):
        return await update.message.reply_text(get_text(context, 'approval_not_admin'))

    if len(context.args) != 2:
        return await update.message.reply_text(get_text(context, 'approve_usage'))
        
    try:
        user_id = int(context.args[0])
        album_key = context.args[1].lower() # e.g., 'vol4'
        album_title = get_text({'user_data': {'lang': 'ti'}}, f'album_{album_key}') # Get title in Tigrinya for admin log

        await send_success_message(user_id, album_key, album_title)
        await update.message.reply_text(get_text(context, 'approval_success_admin', user_id=user_id, album_title=album_title))
    except (ValueError, IndexError, KeyError):
        await update.message.reply_text("Invalid User ID or Album Key format.")

async def reject_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID): return
    if len(context.args) != 1: return await update.message.reply_text(get_text(context, 'reject_usage'))
    try:
        user_id = int(context.args[0])
        await context.bot.send_message(chat_id=user_id, text=get_text(context, 'payment_rejected_user'), parse_mode=ParseMode.HTML)
        await update.message.reply_text(get_text(context, 'rejection_success_admin', user_id=user_id))
    except (ValueError, IndexError): await update.message.reply_text("Invalid User ID.")

# --- UTILITY Functions (run by commands) ---
async def send_success_message(user_id: int, album_key: str, album_title: str):
    target_channel_id = CHANNEL_IDS.get(album_key)
    if not target_channel_id:
        logging.error(f"No channel ID found for album key: {album_key}")
        await bot_app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"⚠️ ERROR: No Channel ID found for album `{album_key}` for user `{user_id}`.")
        return

    try:
        await bot_app.bot.unban_chat_member(chat_id=target_channel_id, user_id=user_id, only_if_banned=True) # Unban first
        await bot_app.bot.promote_chat_member(chat_id=target_channel_id, user_id=user_id, can_post_messages=False) # Smart way to add
        await bot_app.bot.send_message(user_id, get_text({'user_data': {'lang': 'ti'}}, 'payment_success_user', album_title=album_title, invite_link=f"Channel for {album_title}")) # Success message
        job_queue = bot_app.job_queue
        job_queue.run_once(schedule_feedback, when=timedelta(days=3), data={'user_id': user_id, 'album_title': album_title}, name=f"feedback_{user_id}")

    except BadRequest as e:
        if "USER_IS_BOT" in str(e): # Bot trying to approve a bot
            pass
        elif "USER_NOT_MUTUAL_CONTACT" in str(e): # Privacy setting
            invite_link = await bot_app.bot.create_chat_invite_link(chat_id=target_channel_id, member_limit=1)
            # You might want to create a special message for this case
            await bot_app.bot.send_message(user_id, get_text({'user_data': {'lang': 'ti'}}, 'payment_success_user_privacy', invite_link=invite_link.invite_link))
        else:
            logging.error(f"Failed to add {user_id} to channel {target_channel_id}: {e}")

async def schedule_feedback(context: ContextTypes.DEFAULT_TYPE):
    """Job to ask for feedback after 3 days."""
    job_data = context.job.data
    await context.bot.send_message(
        chat_id=job_data['user_id'], 
        text=get_text({'user_data': {'lang': 'ti'}}, 'feedback_request', album_title=job_data['album_title']),
        parse_mode=ParseMode.HTML
    )

# --- Web Server (for health checks on Railway/Render) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers(); self.wfile.write(bytes("Bot is running!", "utf-8"))
def run_web_server():
    server_address = ('', PORT); httpd = HTTPServer(server_address, HealthCheckHandler)
    httpd.serve_forever()

def main() -> None:
    """Set up and run the bot."""
    global bot_app
    
    # Critical check for necessary variables
    if not TELEGRAM_TOKEN or not ADMIN_CHAT_ID or not all(CHANNEL_IDS.values()):
        logging.critical("CRITICAL ERROR: One or more essential environment variables are missing.")
        return

    web_server_thread = threading.Thread(target=run_web_server); web_server_thread.daemon = True; web_server_thread.start()
    application = Application.builder().token(TELEGRAM_TOKEN).build()    
    # Conversation handler for the main user flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            LANG_SELECT: [CallbackQueryHandler(language_select_handler, pattern="^lang_")],
            MAIN_MENU: [
                CallbackQueryHandler(album_select_handler, pattern="^select_vol"),
                CallbackQueryHandler(main_menu_handler, pattern="^back_to_main_menu$")
            ],
            AWAITING_PROOF: [MessageHandler(filters.TEXT | filters.PHOTO, proof_handler)],
        },
        fallbacks=[
             CallbackQueryHandler(start_command, pattern="^back_to_start$"),
             CommandHandler("start", start_command)
        ],
    )

    # Add all handlers to the application
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("approve", approve_command, filters=filters.User(username=ADMIN_USERNAME)))
    application.add_handler(CommandHandler("reject", reject_command, filters=filters.User(username=ADMIN_USERNAME)))

    logging.info("Starting bot polling..."); application.run_polling()

if __name__ == "__main__":
    main()