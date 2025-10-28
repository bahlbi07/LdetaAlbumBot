import logging
import os
import uuid
import requests
import threading
import json
import asyncio
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler, # Make sure MessageHandler is imported
    filters # Make sure filters is imported
)

# Load environment variables
load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "100")
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID") # New: For the album cover
PORT = int(os.environ.get('PORT', 8080))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

# --- Global variable ---
bot_app = None

# --- Logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- Conversation Handler States ---
MAIN_MENU, BUY_CONFIRM = range(2)

# --- Chapa Payment Function ---
async def generate_chapa_link(user_id: int, first_name: str, last_name: str, price: str) -> str:
    tx_ref = f"ldeta-album-{user_id}-{uuid.uuid4()}"
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    payload = {
        "amount": price, "currency": "ETB", "email": f"{user_id}@telegram.user",
        "first_name": first_name, "last_name": last_name or first_name,
        "tx_ref": tx_ref,
        "callback_url": f"{RENDER_URL}/chapa_webhook",
        "return_url": "https://t.me/YOUR_BOT_USERNAME_HERE",
        "customization[title]": "Lidetamariam Vol. 4 Album",
        "customization[description]": "Payment for the new album"
    }
    try:
        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data["data"]["checkout_url"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Chapa API error: {e}")
    return None

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
    if ALBUM_ART_FILE_ID:
        try:
            await context.bot.send_photo(chat_id=user.id, photo=ALBUM_ART_FILE_ID)
        except Exception as e:
            logging.error(f"Could not send album art photo: {e}")
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=main_menu_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
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
            "ብዙሓት ሓደሽቲን መንፈሳውያን መዝሙራትን ዝሓዘ እዩ።\n\n"
            "<i>(ኣብዚ ተወሰኺ ሓበሬታ ወይ ዝርዝር መዝሙራት ክንውስኽ ንኽእል ኢና።)</i>"
        )
        keyboard = [[InlineKeyboardButton("🔙 ናብ መጀመርታ ተመለስ", callback_data="back_to_start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=about_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        return MAIN_MENU
    elif query.data == "buy_album_start":
        keyboard = [
            [InlineKeyboardButton("🇪🇹 ኣብ ውሽጢ ኢትዮጵያ", callback_data="location_ethiopia")],
            [InlineKeyboardButton("🌍 ካብ ኢትዮጵያ ወጻኢ", callback_data="location_outside")],
            [InlineKeyboardButton("🔙 ናብ መጀመርታ ተመለስ", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="በጃኻ ክፍሊት ንምፍጻም ኣበይ ከም ዘለኻ ምረጽ፦", reply_markup=reply_markup)
        return BUY_CONFIRM
    return MAIN_MENU

async def handle_buy_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    if query.data == "location_ethiopia":
        await query.edit_message_text(text=f"ጽቡቕ! ዋጋ ኣልበም <b>{ALBUM_PRICE} ብር</b> እዩ።\n\n<i>ናይ ክፍያ መላግቦ እናዳለና ስለ ዝኾና በጃኻ ጽንሕ በል።</i>", parse_mode=ParseMode.HTML)
        payment_link = await generate_chapa_link(user.id, user.first_name, user.last_name, ALBUM_PRICE)
        if payment_link:
            await query.message.reply_text(f"ክፍሊት ንምፍጻም ነዚ ዝስዕብ መላግቦ ተጠቐም:\n\n{payment_link}")
        else:
            await query.message.reply_text("ይቕሬታ! ኣብዚ እዋን'ዚ ናይ ክፍያ መላግቦ ክፍጠር ኣይተኻእለን።")
        return ConversationHandler.END
    elif query.data == "location_outside":
        await query.edit_message_text(text="እዚ ናይ ወጻኢ ክፍያ ኣገልግሎት ኣብዚ እዋን'ዚ ኣይጀመረን።")
        await asyncio.sleep(3)
        return await start_command(update, context)
    return ConversationHandler.END

# THIS IS A TEMPORARY FUNCTION TO GET FILE_ID
    """Prints the update object to the logs to find the file_id of a photo."""
    logging.info("--- PHOTO RECEIVED ---")
    logging.info(f"Full update object: {update}")
    logging.info("--- END OF PHOTO INFO ---")
    await update.message.reply_text("Photo received. Checking logs for file_id...")

# ... (Webhook functions and Web Server remain the same) ...
async def send_success_message(user_id: int):
    try:
        invite_link = await bot_app.bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
        success_text = (
            "✅ <b>ክፍሊትኩም ብዓወት ተፈጺሙ እዩ!</b> ✅\n\n"
            "ንመርኣይትና ዝገበርኩምዎ ደገፍ ኣዚና ነምስግን።\n\n"
            "ነዚ ሓደ ግዜ ጥራይ ዝሰርሕ መላግቦ ተጠቒምኩም ናብቲ መዝሙራት ዘለዎ ቻነል ክትኣትዉ ትኽእሉ ኢኹም፦\n"
            f"<b>{invite_link.invite_link}</b>"
        )
        await bot_app.bot.send_message(chat_id=user_id, text=success_text, parse_mode=ParseMode.HTML)
        logging.info(f"Successfully sent invite link to user {user_id}")
    except Exception as e:
        logging.error(f"Failed to send invite link to user {user_id}: {e}")

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers(); self.wfile.write(bytes("Bot is running!", "utf-8"))
    def do_POST(self):
        if self.path == '/chapa_webhook':
            content_length = int(self.headers['Content-Length']); post_data = self.rfile.read(content_length); data = json.loads(post_data)
            logging.info(f"Webhook received: {data}")
            if data.get("status") == "success":
                tx_ref = data.get("tx_ref")
                try:
                    user_id = int(tx_ref.split('-')[2])
                    logging.info(f"Payment success for user_id: {user_id}")
                    asyncio.run_coroutine_threadsafe(send_success_message(user_id), bot_app.loop)
                except Exception as e: logging.error(f"Could not parse user_id from tx_ref: {tx_ref} - Error: {e}")
            self.send_response(200); self.end_headers(); self.wfile.write(bytes("OK", "utf-8"))
        else: self.send_response(404); self.end_headers()

def run_web_server():
    server_address = ('', PORT); httpd = HTTPServer(server_address, WebhookHandler)
    logging.info(f"Starting web server on port {PORT}..."); httpd.serve_forever()

# PASTE THIS NEW CORRECTED SECTION
def main() -> None:
    global bot_app

    # --- START: NEW DIAGNOSTIC CODE ---
    if CHAPA_SECRET_KEY:
        logging.info("--- CHAPA KEY CHECK ---")
        logging.info(f"Key Found. Starts with: {CHAPA_SECRET_KEY[:15]}")
        logging.info(f"Key Ends with: {CHAPA_SECRET_KEY[-6:]}")
        logging.info("-----------------------")
    else:
        logging.error("!!! FATAL: CHAPA_SECRET_KEY IS NOT FOUND AT ALL !!!")
    # --- END: NEW DIAGNOSTIC CODE ---

    if not all([TELEGRAM_TOKEN, CHAPA_SECRET_KEY, PRIVATE_CHANNEL_ID]):
        logging.error("!!! ERROR: Missing one or more environment variables.")
        return

    web_server_thread = threading.Thread(target=run_web_server)
    web_server_thread.daemon = True
    web_server_thread.start()

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app = application
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(handle_main_menu, pattern="^(about_album|buy_album_start)$"),
                CallbackQueryHandler(start_command, pattern="^back_to_start$")
            ],
            BUY_CONFIRM: [
                CallbackQueryHandler(handle_buy_process, pattern="^(location_ethiopia|location_outside)$"),
                CallbackQueryHandler(start_command, pattern="^back_to_start$")
            ],
        },
        fallbacks=[CommandHandler("start", start_command)],
        allow_reentry=True
    )
    application.add_handler(conv_handler)
    
    logging.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()