import logging
import os
import threading
import json
import asyncio
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
)

# Load environment variables
load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "100")
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")
PORT = int(os.environ.get('PORT', 8080))

# --- Logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- Conversation Handler States ---
MAIN_MENU, BUY_CONFIRM = range(2)

# --- Bot Handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    main_menu_text = (
        f"ሰላም <b>{user.first_name}</b>!\n\n"
        "እንኳዕ ብደሓን ናብ ወግዓዊ መሸጢ ቦት <b>'መዘምራን ልደታ ማርያም ቁምስና መቐለ'</b> ራብዓይ ኣልበም መጻእካ።"
    )
    keyboard = [
        [InlineKeyboardButton("🛒 ኣልበም ግዛእ", callback_data="buy_album_start")],
        [InlineKeyboardButton("ℹ️ ብዛዕባ እዚ ኣልበም", callback_data="about_album")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query is None and ALBUM_ART_FILE_ID:
        try:
            await context.bot.send_photo(chat_id=user.id, photo=ALBUM_ART_FILE_ID)
        except Exception as e: logging.error(f"Could not send album art photo: {e}")

    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(text=main_menu_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except Exception as e: logging.warning(f"Could not edit message: {e}")
    else:
        await update.message.reply_text(text=main_menu_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        
    return MAIN_MENU

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == "about_album":
        about_text = (
            "<b><u>ብዛዕባ ራብዓይ ኣልበም</u></b>\n\n"
            "እዚ ብ'መዘምራን ልደታ ማርያም ቁምስና መቐለ' ዝተዳለወ ራብዓይ ኣልበም ኮይኑ፡ "
            "ብዙሓት ሓደሽቲን መንፈሳውያን መዝሙራትን ዝሓዘ እዩ።"
        )
        keyboard = [[InlineKeyboardButton("🔙 ናብ መጀመርታ ተመለስ", callback_data="back_to_start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=about_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        return MAIN_MENU

    elif query.data == "buy_album_start":
        # This is the NEW implementation
        payment_instructions = (
            f"ጽቡቕ! ዋጋ ኣልበም <b>{ALBUM_PRICE} ብር</b> እዩ።\n\n"
            "ክፍሊት ንምፍጻም በዞም ዝስዕቡ ኣማራጺታት ተጠቐም፦\n\n"
            "<b><u>1. ብናይ ንግድ ባንክ (CBE):</u></b>\n"
            "<b>ስም:</b> [ኣብዚ ናይ ባንክ ስምካ ጽሓፍ]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [ኣብዚ ናይ ባንክ ቁጽርኻ ጽሓፍ]\n\n"
            "<b><u>2. ብቴሌብር (Telebirr):</u></b>\n"
            "<b>ቁጽሪ ስልኪ:</b> [ኣብዚ ናይ ቴሌብር ቁጽርኻ ጽሓፍ]\n\n"
            "⚠️ <b>ኣገዳሲ:</b> ክፍሊት ምስ ፈጸምካ፡ ነቲ ደረሰኝ (screenshot) ናብ @YourAdminUsername ብምስዳድ ብኡንብኡ ናይ መእተዊ መላግቦ ክንሰደልካ ኢና።"
        )
        keyboard = [[InlineKeyboardButton("🔙 ናብ መጀመርታ ተመለስ", callback_data="back_to_start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=payment_instructions, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        return MAIN_MENU # Go back to the main menu state after showing instructions


# --- Web Server for Render/Railway Health Check ---
class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers(); self.wfile.write(bytes("Bot is running!", "utf-8"))

def run_web_server():
    server_address = ('', PORT); httpd = HTTPServer(server_address, WebhookHandler)
    logging.info(f"Starting web server on port {PORT}..."); httpd.serve_forever()

def main() -> None:
    if not TELEGRAM_TOKEN:
        logging.error("!!! ERROR: TELEGRAM_TOKEN is missing."); return
    web_server_thread = threading.Thread(target=run_web_server); web_server_thread.daemon = True; web_server_thread.start()
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(handle_main_menu, pattern="^(about_album|buy_album_start)$"),
                CallbackQueryHandler(start_command, pattern="^back_to_start$")
            ],
        },
        fallbacks=[CommandHandler("start", start_command)],
        allow_reentry=True
    )
    application.add_handler(conv_handler)
    logging.info("Starting bot polling..."); application.run_polling()
if __name__ == "__main__": main()