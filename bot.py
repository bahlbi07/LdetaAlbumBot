import logging
import os
import threading
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
)

# Import the translations
from translations import TRANSLATIONS

# Load environment variables
load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "299") # Default Price
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Dmtsibereket").replace("@", "") # Admin for receiving slips
PORT = int(os.environ.get('PORT', 8080))
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")

# --- Global variable to hold the application instance ---
bot_app = None

# --- Logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING) # Reduce noisy logging from httpx

# --- Conversation Handler States ---
LANG_SELECT, LOCATION_SELECT, MAIN_MENU, AWAIT_SLIP_CONFIRM = range(4)

# --- Helper function for translations ---
def get_text(lang_code: str, key: str, **kwargs) -> str:
    """Gets translated text, falling back to English if the key is not in the specific language."""
    # Start with the selected language
    lang_dict = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])
    text = lang_dict.get(key)
    # If the key is not found, fall back to English
    if text is None:
        text = TRANSLATIONS['en'].get(key, f"_{key}_")
    return text.format(**kwargs)

# --- START of conversation flow ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks for language selection."""
    user = update.effective_user
    context.user_data.clear() # Clear any old data for a fresh start

    if update.callback_query:
        await update.callback_query.answer()
        try: # Try to delete the previous message to clean up the chat
            await update.callback_query.message.delete()
        except Exception: pass # Ignore if it fails

    keyboard = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ (ኢሮብ)", callback_data="lang_saho")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = TRANSLATIONS['ti']['welcome_language'].format(user_name=user.first_name) # Default welcome
    
    # Send Album Art if available and this is a fresh start
    if ALBUM_ART_FILE_ID and not update.callback_query:
        try:
            await update.message.reply_photo(photo=ALBUM_ART_FILE_ID, caption=welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.error(f"Could not send photo: {e}")
            await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        
    return LANG_SELECT

async def select_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the language choice and asks for location."""
    query = update.callback_query
    await query.answer()
    
    lang_code = query.data.split('_')[1]
    context.user_data['lang'] = lang_code
    
    if lang_code == 'saho':
        saho_text = get_text(lang_code, 'saho_unavailable')
        keyboard = [[InlineKeyboardButton(get_text('ti', 'back_to_start_button'), callback_data="back_to_start")]]
        await query.edit_message_text(text=saho_text, reply_markup=InlineKeyboardMarkup(keyboard))
        return LANG_SELECT
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang_code, 'location_in_button'), callback_data="location_in")],
        [InlineKeyboardButton(get_text(lang_code, 'location_out_button'), callback_data="location_out")],
        [InlineKeyboardButton(get_text(lang_code, 'back_to_start_button'), callback_data="back_to_start")],
    ]
    await query.edit_message_text(text=get_text(lang_code, 'ask_location'), reply_markup=InlineKeyboardMarkup(keyboard))
    return LOCATION_SELECT

async def select_location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores location choice and shows the main menu."""
    query = update.callback_query
    await query.answer()

    location = query.data.split('_')[1]
    context.user_data['location'] = location
    
    lang_code = context.user_data.get('lang', 'en')
    
    main_menu_text = get_text(lang_code, 'welcome_main')
    keyboard = [
        [InlineKeyboardButton(get_text(lang_code, 'buy_album_button'), callback_data="main_buy")],
        [InlineKeyboardButton(get_text(lang_code, 'about_album_button'), callback_data="main_about")],
        [InlineKeyboardButton(get_text(lang_code, 'back_to_start_button'), callback_data="back_to_start")]
    ]
    await query.edit_message_text(text=main_menu_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    return MAIN_MENU

async def main_menu_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles button presses from the main menu."""
    query = update.callback_query
    await query.answer()
    
    lang_code = context.user_data.get('lang', 'en')
    choice = query.data

    if choice == "main_about":
        keyboard = [[InlineKeyboardButton(get_text(lang_code, 'back_to_main_menu_button'), callback_data="back_to_main_menu")]]
        await query.edit_message_text(
            text=get_text(lang_code, 'about_album_text'), 
            reply_markup=InlineKeyboardMarkup(keyboard), 
            parse_mode=ParseMode.HTML
        )
        return MAIN_MENU

    elif choice == "main_buy":
        # Check if the user is outside Ethiopia
        if context.user_data.get('location') == 'out':
            await query.edit_message_text(text=get_text(lang_code, 'saho_unavailable')) # Using Saho message as it means 'under construction'
            await asyncio.sleep(4) # Give user time to read
            return await select_location_handler(update, context) # Go back gracefully

        payment_text = get_text(lang_code, 'payment_instructions', album_price=ALBUM_PRICE)
        keyboard = [
            [InlineKeyboardButton(get_text(lang_code, 'slip_sent_button'), callback_data="slip_is_sent")],
            [InlineKeyboardButton(get_text(lang_code, 'back_to_main_menu_button'), callback_data="back_to_main_menu")]
        ]
        await query.edit_message_text(text=payment_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
        return AWAIT_SLIP_CONFIRM

    return MAIN_MENU

async def slip_confirmation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User confirms they sent the slip. Notifies admin."""
    query = update.callback_query
    await query.answer()
    lang_code = context.user_data.get('lang', 'en')
    user = update.effective_user

    await query.edit_message_text(text=get_text(lang_code, 'wait_for_verification'), parse_mode=ParseMode.HTML)
    
    try: # Notify the admin
        admin_notif_text = get_text('en', 'payment_notif_admin', user_mention=user.mention_html(), user_id=user.id)
        await context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=admin_notif_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Could not notify admin @{ADMIN_USERNAME}: {e}")
        # Inform user if admin notification failed
        await query.message.reply_text(f"Could not notify admin automatically. Please contact @{ADMIN_USERNAME} manually.")
        
    return ConversationHandler.END # End conversation, wait for admin

# --- END of conversation flow ---


# --- Admin-only Commands ---

async def approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ADMIN ONLY: Approve payment and send invite link."""
    admin_user = update.effective_user
    lang_code = 'en' # Admin language is English
    
    if admin_user.username.lower() != ADMIN_USERNAME.lower():
        return await update.message.reply_text(get_text(lang_code, 'approval_not_admin'))

    if not context.args or len(context.args) != 1:
        return await update.message.reply_text(get_text(lang_code, 'approve_usage'))
    try:
        user_id_to_approve = int(context.args[0])
        await send_success_message_to_user(user_id_to_approve)
        await update.message.reply_text(get_text(lang_code, 'approval_success_admin', user_id=user_id_to_approve))
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid User ID format.")

async def reject_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ADMIN ONLY: Reject payment and notify user."""
    admin_user = update.effective_user
    lang_code = 'en'
    
    if admin_user.username.lower() != ADMIN_USERNAME.lower():
        return await update.message.reply_text(get_text(lang_code, 'approval_not_admin'))

    if not context.args or len(context.args) != 1:
        return await update.message.reply_text(get_text(lang_code, 'reject_usage'))
    try:
        user_id_to_reject = int(context.args[0])
        # Defaulting to Tigrinya, as it's the primary audience language.
        rejection_text = get_text('ti', 'payment_rejected_user', YOUR_ADMIN_USERNAME_HERE=ADMIN_USERNAME)
        await context.bot.send_message(chat_id=user_id_to_reject, text=rejection_text, parse_mode=ParseMode.HTML)
        await update.message.reply_text(get_text(lang_code, 'rejection_success_admin', user_id=user_id_to_reject))
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid User ID format.")

async def send_success_message_to_user(user_id: int):
    try:
        invite_link = await bot_app.bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
        # Defaulting to Tigrinya
        success_text = get_text('ti', 'payment_success_user', invite_link=invite_link.invite_link)
        await bot_app.bot.send_message(chat_id=user_id, text=success_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Failed to send invite to {user_id}: {e}")
        # Notify admin if it failed
        await bot_app.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=f"⚠️ Failed to auto-send invite to user `{user_id}`. Please do it manually.", parse_mode="MarkdownV2")

# --- Web Server (for health checks, can be removed if not needed) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers(); self.wfile.write(bytes("Bot is running!", "utf-8"))

def run_web_server():
    server_address = ('', PORT); httpd = HTTPServer(server_address, HealthCheckHandler)
    logging.info(f"Starting web server on port {PORT}..."); httpd.serve_forever()


def main() -> None:
    """Set up and run the bot."""
    global bot_app
    if not TELEGRAM_TOKEN or not PRIVATE_CHANNEL_ID:
        logging.critical("CRITICAL: Missing TELEGRAM_TOKEN or PRIVATE_CHANNEL_ID in environment variables.")
        return

    # Run web server in a background thread
    web_server_thread = threading.Thread(target=run_web_server)
    web_server_thread.daemon = True
    web_server_thread.start()

    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app = application
    
    # --- The Conversation Flow ---
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            LANG_SELECT: [
                CallbackQueryHandler(select_language_handler, pattern="^lang_"),
                CallbackQueryHandler(start_command, pattern="^back_to_start$"),
            ],
            LOCATION_SELECT: [
                CallbackQueryHandler(select_location_handler, pattern="^location_"),
                CallbackQueryHandler(start_command, pattern="^back_to_start$"),
            ],
            MAIN_MENU: [
                CallbackQueryHandler(main_menu_button_handler, pattern="^main_"),
                # This makes the back button from About go to the main menu screen
                CallbackQueryHandler(select_location_handler, pattern="^back_to_main_menu$"), 
                CallbackQueryHandler(start_command, pattern="^back_to_start$"),
            ],
            AWAIT_SLIP_CONFIRM: [
                CallbackQueryHandler(slip_confirmation_handler, pattern="^slip_is_sent$"),
                CallbackQueryHandler(select_location_handler, pattern="^back_to_main_menu$")
            ]
        },
        fallbacks=[CommandHandler("start", start_command)],
        per_message=False,
    )

    # --- Add all handlers to the application ---
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("approve", approve_command, filters=filters.User(username=ADMIN_USERNAME)))
    application.add_handler(CommandHandler("reject", reject_command, filters=filters.User(username=ADMIN_USERNAME)))

    # --- Start the Bot ---
    logging.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()