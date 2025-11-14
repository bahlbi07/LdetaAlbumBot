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
    MessageHandler,
    filters,
)

from translations import TRANSLATIONS

load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "299")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Dmtsibereket").replace("@", "")
PORT = int(os.environ.get('PORT', 8080))
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")

bot_app = None

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

LANG_SELECT, LOCATION_SELECT, MAIN_MENU, AWAIT_SLIP_CONFIRM = range(4)

def get_text(lang_code: str, key: str, **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])
    text = lang_dict.get(key)
    if text is None:
        text = TRANSLATIONS['en'].get(key, f"_{key}_")
    return text.format(**kwargs)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    context.user_data.clear()

    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.delete()
        except Exception: pass

    keyboard = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ (ኢሮብ)", callback_data="lang_saho")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # We will use the Tigrinya welcome message by default as it's the main language
    welcome_text = TRANSLATIONS['ti']['welcome_language'].format(user_name=user.first_name)
    
    target_message = update.message or (update.callback_query and update.callback_query.message)

    if ALBUM_ART_FILE_ID and not update.callback_query:
        try:
            await target_message.reply_photo(photo=ALBUM_ART_FILE_ID, caption=welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.error(f"Could not send photo: {e}")
            await target_message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await target_message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        
    return LANG_SELECT

async def select_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split('_')[1]
    context.user_data['lang'] = lang_code
    
    if lang_code == 'saho':
        keyboard = [[InlineKeyboardButton(get_text('ti', 'back_to_start_button'), callback_data="back_to_start")]]
        await query.edit_message_text(text=get_text(lang_code, 'saho_unavailable'), reply_markup=InlineKeyboardMarkup(keyboard))
        return LANG_SELECT
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang_code, 'location_in_button'), callback_data="location_in")],
        [InlineKeyboardButton(get_text(lang_code, 'location_out_button'), callback_data="location_out")],
        [InlineKeyboardButton(get_text(lang_code, 'back_to_start_button'), callback_data="back_to_start")],
    ]
    await query.edit_message_text(text=get_text(lang_code, 'ask_location'), reply_markup=InlineKeyboardMarkup(keyboard))
    return LOCATION_SELECT

async def select_location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    location = query.data.split('_')[1]
    context.user_data['location'] = location
    lang_code = context.user_data.get('lang', 'en')
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang_code, 'buy_album_button'), callback_data="main_buy")],
        [InlineKeyboardButton(get_text(lang_code, 'about_album_button'), callback_data="main_about")],
        [InlineKeyboardButton(get_text(lang_code, 'back_to_start_button'), callback_data="back_to_start")]
    ]
    await query.edit_message_text(text=get_text(lang_code, 'welcome_main'), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    return MAIN_MENU

async def main_menu_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang_code = context.user_data.get('lang', 'en')
    choice = query.data

    if choice == "main_about":
        keyboard = [[InlineKeyboardButton(get_text(lang_code, 'back_to_main_menu_button'), callback_data="back_to_location_select")]]
        await query.edit_message_text(text=get_text(lang_code, 'about_album_text'), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
        return MAIN_MENU

    elif choice == "main_buy":
        if context.user_data.get('location') == 'out':
            await query.edit_message_text(text=get_text(lang_code, 'saho_unavailable'))
            await asyncio.sleep(4)
            return await select_language_handler(update, context) # Go back to language select gracefully

        payment_text = get_text(lang_code, 'payment_instructions', album_price=ALBUM_PRICE, YOUR_ADMIN_USERNAME_HERE=ADMIN_USERNAME)
        keyboard = [
            [InlineKeyboardButton(get_text(lang_code, 'slip_sent_button'), callback_data="slip_is_sent")],
            [InlineKeyboardButton(get_text(lang_code, 'back_to_main_menu_button'), callback_data="back_to_location_select")]
        ]
        await query.edit_message_text(text=payment_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
        return AWAIT_SLIP_CONFIRM

async def slip_confirmation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang_code = context.user_data.get('lang', 'en')
    user = update.effective_user

    await query.edit_message_text(text=get_text(lang_code, 'wait_for_verification'), parse_mode=ParseMode.HTML)
    
    try:
        admin_notif_text = get_text('en', 'payment_notif_admin', user_mention=user.mention_html(), user_id=user.id)
        await context.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=admin_notif_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Could not notify admin @{ADMIN_USERNAME}: {e}")
        # THIS IS THE CORRECTED PART - uses lang_code
        error_notif_text = get_text(lang_code, 'payment_rejected_user', YOUR_ADMIN_USERNAME_HERE=ADMIN_USERNAME) # Using reject message for this error
        await query.message.reply_text(error_notif_text, parse_mode=ParseMode.HTML)
        
    return ConversationHandler.END

async def approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin_user = update.effective_user
    if admin_user.username.lower() != ADMIN_USERNAME.lower():
        return
    if not context.args or len(context.args) != 1:
        return await update.message.reply_text(get_text('en', 'approve_usage'))
    try:
        user_id = int(context.args[0])
        await send_success_message_to_user(user_id)
        await update.message.reply_text(get_text('en', 'approval_success_admin', user_id=user_id))
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid User ID.")

async def reject_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin_user = update.effective_user
    if admin_user.username.lower() != ADMIN_USERNAME.lower():
        return
    if not context.args or len(context.args) != 1:
        return await update.message.reply_text(get_text('en', 'reject_usage'))
    try:
        user_id = int(context.args[0])
        rejection_text = get_text('ti', 'payment_rejected_user', YOUR_ADMIN_USERNAME_HERE=ADMIN_USERNAME)
        await context.bot.send_message(chat_id=user_id, text=rejection_text, parse_mode=ParseMode.HTML)
        await update.message.reply_text(get_text('en', 'rejection_success_admin', user_id=user_id))
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid User ID.")

async def send_success_message_to_user(user_id: int):
    try:
        invite_link = await bot_app.bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
        success_text = get_text('ti', 'payment_success_user', invite_link=invite_link.invite_link)
        await bot_app.bot.send_message(chat_id=user_id, text=success_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Failed to send invite to {user_id}: {e}")
        await bot_app.bot.send_message(chat_id=f"@{ADMIN_USERNAME}", text=f"⚠️ Failed to send invite to user `{user_id}`. Please do it manually.", parse_mode="MarkdownV2")

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers(); self.wfile.write(bytes("Bot is running!", "utf-8"))

def run_web_server():
    server_address = ('', PORT); httpd = HTTPServer(server_address, HealthCheckHandler)
    logging.info(f"Starting web server..."); httpd.serve_forever()

def main() -> None:
    global bot_app
    if not TELEGRAM_TOKEN or not PRIVATE_CHANNEL_ID:
        logging.critical("CRITICAL ERROR: Missing essential environment variables.")
        return

    web_server_thread = threading.Thread(target=run_web_server); web_server_thread.daemon = True; web_server_thread.start()
    application = Application.builder().token(TELEGRAM_TOKEN).build(); bot_app = application
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            LANG_SELECT: [CallbackQueryHandler(select_language_handler, pattern="^lang_")],
            LOCATION_SELECT: [
                CallbackQueryHandler(select_location_handler, pattern="^location_"),
                CallbackQueryHandler(start_command, pattern="^back_to_start$")
            ],
            MAIN_MENU: [
                CallbackQueryHandler(main_menu_button_handler, pattern="^main_"),
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

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("approve", approve_command, filters=filters.User(username=ADMIN_USERNAME)))
    application.add_handler(CommandHandler("reject", reject_command, filters=filters.User(username=ADMIN_USERNAME)))

    logging.info("Bot polling started..."); application.run_polling()

if __name__ == "__main__":
    main()