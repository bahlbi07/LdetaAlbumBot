import logging
import os
import uuid
import requests
import asyncio
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)

# Load environment variables
load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
PRIVATE_CHANNEL_ID = os.getenv("PRIVATE_CHANNEL_ID")
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "100")
PORT = int(os.environ.get('PORT', 8080)) # Port for Render

# --- Logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# --- Conversation Handler States ---
CHOOSE_LOCATION, CHOOSE_ACTION = range(2)

# --- Chapa Payment Function ---
async def generate_chapa_link(user: dict, price: str, currency: str = "ETB") -> str:
    tx_ref = f"ldeta-album-{user['id']}-{uuid.uuid4()}"
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}", "Content-Type": "application/json"}
    payload = {
        "amount": price, "currency": currency, "email": f"{user['id']}@telegram.user",
        "first_name": user.get('first_name', 'User'), "last_name": user.get('last_name', 'Bot'),
        "tx_ref": tx_ref, "callback_url": "https://webhook.site/",
        "return_url": "https://t.me/your_bot_username", # Change your_bot_username
        "customization[title]": "Ldeta Mariam Vol. 4 Album",
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
    keyboard = [["🇪🇹 ኣብ ውሽጢ ኢትዮጵያ"], ["🌍 ካብ ኢትዮጵያ ወጻኢ"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        f"ሰላም {update.effective_user.first_name}! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ኣበይ ከም ዘለኻ ምረጽ፦",
        reply_markup=reply_markup
    )
    return CHOOSE_LOCATION

async def handle_location_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "🇪🇹 ኣብ ውሽጢ ኢትዮጵያ":
        keyboard = [["✅ ኣልበም ግዛእ"], ["🔙 ናብ መጀመርታ ተመለስ"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            f"ጽቡቕ ምርጫ! ዋጋ ናይ'ዚ ራብዓይ ኣልበም {ALBUM_PRICE} ብር እዩ።\n\nክፍሊት ንምፍጻም 'ኣልበም ግዛእ' ዝብል ጠውቕ።",
            reply_markup=reply_markup
        )
        return CHOOSE_ACTION
    elif choice == "🌍 ካብ ኢትዮጵያ ወጻኢ":
        await update.message.reply_text("እዚ ናይ ወጻኢ ክፍያ ኣገልግሎት ኣብዚ እዋን'ዚ ኣይጀመረን።", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def handle_buy_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    user = update.effective_user
    if choice == "✅ ኣልበም ግዛእ":
        await update.message.reply_text("የመስግነልና! ናይ ክፍያ መላግቦ እናዳለና ስለ ዝኾና በጃኻ ጽንሕ በል።", reply_markup=ReplyKeyboardRemove())
        payment_link = await generate_chapa_link(user.to_dict(), ALBUM_PRICE)
        if payment_link:
            await update.message.reply_text(f"ክፍሊት ንምፍጻም ነዚ ዝስዕብ መላግቦ ተጠቐም:\n\n{payment_link}")
        else:
            await update.message.reply_text("ይቕሬታ! ኣብዚ እዋን'ዚ ናይ ክፍያ መላግቦ ክፍጠር ኣይተኻእለን።")
    elif choice == "🔙 ናብ መጀመርታ ተመለስ":
        await start_command(update, context)
    return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("መስርሕ ተቋሪጹ ኣሎ። ዳግማይ ንምጅማር /start በል።", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# --- Simple Web Server for Render Health Check ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Bot is running!", "utf-8"))

def run_web_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    logging.info(f"Starting web server on port {PORT}")
    httpd.serve_forever()

# --- Main Application Setup ---
async def main():
    if not all([TELEGRAM_TOKEN, CHAPA_SECRET_KEY, PRIVATE_CHANNEL_ID]):
        logging.error("!!! ERROR: Missing one or more environment variables.")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSE_LOCATION: [MessageHandler(filters.Regex("^(🇪🇹 ኣብ ውሽጢ ኢትዮጵያ|🌍 ካብ ኢትዮጵያ ወጻኢ)$"), handle_location_choice)],
            CHOOSE_ACTION: [MessageHandler(filters.Regex("^(✅ ኣልበም ግዛእ|🔙 ናብ መጀመርታ ተመለስ)$"), handle_buy_choice)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    application.add_handler(conv_handler)

    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logging.info("Bot is polling...")

    # Keep the main thread alive for the web server (which runs in a separate thread)
    # The web server is just to keep Render happy. The bot logic is in the polling above.
    # In a real-world scenario, you might run the web server in its own thread.
    # For this simple case, we just need the script to not exit.
    
    # We will run a simple web server in the main thread now
    run_web_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped manually.")