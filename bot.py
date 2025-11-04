import logging
import os
import threading
import json
import asyncio
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
    MessageHandler,
    filters,
)

# Import the translations
from translations import TRANSLATIONS

# Load environment variables
load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "100")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Dmtsibereket").replace("@", "") # Admin for receiving slips
PORT = int(os.environ.get('PORT', 8080))
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")

# --- Global variable ---
bot_app = None

# --- Logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- Conversation Handler States ---
LANGUAGE_SELECT, MAIN_MENU, AWAIT_SLIP = range(3)

# --- Helper function for translations ---
def get_text(lang_code: str, key: str, **kwargs) -> str:
    """Gets translated text, falling back to English if not found."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS['en']).get(key, f"_{key}_").format(**kwargs)

# --- Main Bot Handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks for language selection."""
    user = update.effective_user
    context.user_data.clear() # Clear data for a fresh start

    # This can be triggered by /start or a callback query
    if update.callback_query:
        await update.callback_query.answer()
        # Delete the previous message to clean up the chat
        try:
            await update.callback_query.message.delete()
        except Exception:
            pass # Ignore if it fails (e.g., message too old)

    keyboard = [
        [
            InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"),
            InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am"),
        ],
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ (ኢሮብ)", callback_data="lang_saho"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # If there's an album cover, send it first
    if ALBUM_ART_FILE_ID and update.callback_query is None:
        try:
            await context.bot.send_photo(
                chat_id=user.id, 
                photo=ALBUM_ART_FILE_ID,
                caption=TRANSLATIONS['ti']['welcome'].format(user_name=user.first_name),
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logging.error(f"Could not send photo with caption: {e}")
            # Fallback to text message if photo fails
            await update.message.reply_text(
                text=TRANSLATIONS['ti']['welcome'].format(user_name=user.first_name),
                reply_markup=reply_markup, 
                parse_mode=ParseMode.HTML
            )
    else:
        # Just send text (e.g., when coming back to the menu)
        welcome_text = get_text('ti', 'welcome', user_name=user.first_name) # Default to Tigrinya
        await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    
    return LANGUAGE_SELECT

async def language_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the user's language choice."""
    query = update.callback_query
    await query.answer()
    
    lang_code = query.data.split('_')[1]
    context.user_data['lang'] = lang_code
    
    if lang_code == 'saho':
        # Special case for Saho (Irob) as it's under construction
        saho_text = get_text(lang_code, 'saho_unavailable')
        keyboard = [
            [InlineKeyboardButton(get_text(lang_code, 'back_button'), callback_data="back_to_lang_select")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=saho_text, reply_markup=reply_markup)
        return LANGUAGE_SELECT # Stay in the language selection state
    
    # For other languages, proceed to the main menu
    return await main_menu_handler(update, context)


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displays the main menu in the selected language."""
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get('lang', 'en') # Default to English if no lang is set

    main_menu_text = get_text(lang_code, 'main_menu')
    keyboard = [
        [InlineKeyboardButton(get_text(lang_code, 'buy_album_button'), callback_data="buy_album_start")],
        [InlineKeyboardButton(get_text(lang_code, 'about_album_button'), callback_data="about_album")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=main_menu_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return MAIN_MENU
    
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles all button presses from the main menu onwards."""
    query = update.callback_query
    await query.answer()
    
    lang_code = context.user_data.get('lang', 'en')
    user_choice = query.data

    if user_choice == "about_album":
        about_text = get_text(lang_code, 'about_album_text')
        keyboard = [[InlineKeyboardButton(get_text(lang_code, 'back_button'), callback_data="back_to_main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=about_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        return MAIN_MENU

    elif user_choice == "buy_album_start":
        payment_instructions = get_text(lang_code, 'payment_instructions', album_price=ALBUM_PRICE)
        keyboard = [
            [InlineKeyboardButton(get_text(lang_code, 'slip_sent_button'), callback_data="slip_sent")],
            [InlineKeyboardButton(get_text(lang_code, 'back_button'), callback_data="back_to_main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=payment_instructions, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        return AWAIT_SLIP

    return MAIN_MENU
    
async def slip_sent_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirms that user sent the slip and waits for admin approval."""
    query = update.callback_query
    await query.answer()
    
    lang_code = context.user_data.get('lang', 'en')
    wait_text = get_text(lang_code, 'wait_for_verification')
    
    await query.edit_message_text(text=wait_text, parse_mode=ParseMode.HTML)
    
    # Notify admin
    user = update.effective_user
    admin_notification = get_text('en', 'payment_notif_admin', user_mention=user.mention_html(), user_id=user.id) # Admin notif in English
    try:
        await context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=admin_notification, parse_mode=ParseMode.HTML)
        logging.info(f"Notified admin @{ADMIN_USERNAME} about user {user.id}")
    except Exception as e:
        logging.error(f"Could not notify admin @{ADMIN_USERNAME}. Make sure the admin has started the bot. Error: {e}")
        await query.message.reply_text("Error notifying admin. Please manually contact @{ADMIN_USERNAME}")

    return ConversationHandler.END


# --- Admin Approval Command ---
async def approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin command to approve a payment and send invite link."""
    admin_user = update.effective_user
    
    # Check if the user is the admin
    if admin_user.username != ADMIN_USERNAME:
        await update.message.reply_text(get_text('en', 'approval_not_admin')) # Use English for admin replies
        return

    # Check for correct usage: /approve <user_id>
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(get_text('en', 'approve_usage'))
        return

    try:
        user_id_to_approve = int(context.args[0])
        # Find the target user's language from a real-world database or a simpler cache if needed
        # For now, we will send in English and Tigrinya for safety
        await send_success_message(user_id_to_approve)
        await update.message.reply_text(get_text('en', 'approval_success_admin', user_id=user_id_to_approve))
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please provide a numeric ID.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

# --- Helper to send success message ---
async def send_success_message(user_id: int):
    """Sends the success message and channel invite link to the user."""
    try:
        invite_link = await bot_app.bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
        # We don't know the user's selected language here, so we send a multilingual message or default to one
        success_text = get_text('ti', 'payment_success_user', invite_link=invite_link.invite_link) # Default to Tigrinya
        await bot_app.bot.send_message(chat_id=user_id, text=success_text, parse_mode=ParseMode.HTML)
        logging.info(f"Successfully sent invite link to user {user_id}")
    except Exception as e:
        logging.error(f"Failed to send invite link to user {user_id}: {e}")
        # Notify admin if sending failed
        await bot_app.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=f"Failed to send invite to user {user_id}. Please do it manually.")


# --- Simple Web Server for Health Check ---
class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Bot is running!", "utf-8"))

def run_web_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, WebhookHandler)
    logging.info(f"Starting web server on port {PORT}...")
    httpd.serve_forever()

# --- Main Application Setup ---
def main() -> None:
    global bot_app
    if not TELEGRAM_TOKEN or not PRIVATE_CHANNEL_ID:
        logging.error("!!! ERROR: Missing critical environment variables (TELEGRAM_TOKEN, PRIVATE_CHANNEL_ID).")
        return

    # Start the simple web server in a separate thread
    web_server_thread = threading.Thread(target=run_web_server)
    web_server_thread.daemon = True
    web_server_thread.start()

    # Create the Telegram Bot Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app = application
    
    # Conversation handler for the main user flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            LANGUAGE_SELECT: [
                CallbackQueryHandler(language_select_handler, pattern="^lang_"),
                CallbackQueryHandler(start_command, pattern="^back_to_lang_select$") # For Saho back button
            ],
            MAIN_MENU: [
                CallbackQueryHandler(button_handler, pattern="^(about_album|buy_album_start)$"),
                CallbackQueryHandler(main_menu_handler, pattern="^back_to_main_menu$")
            ],
            AWAIT_SLIP: [
                CallbackQueryHandler(slip_sent_handler, pattern="^slip_sent$"),
                CallbackQueryHandler(main_menu_handler, pattern="^back_to_main_menu$")
            ],
        },
        fallbacks=[CommandHandler("start", start_command)],
        per_message=False
    )
    
    application.add_handler(conv_handler)
    # Handler for the admin's /approve command
    application.add_handler(CommandHandler("approve", approve_command, filters=filters.User(username=ADMIN_USERNAME)))

    logging.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()