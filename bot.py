import logging
import os
import uuid
import requests
import threading
import json
import asyncio
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
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
PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID")) # Convert to integer
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "100")
PORT = int(os.environ.get('PORT', 8080))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL") # Render provides this automatically

# --- Global variable to hold the bot application instance ---
bot_app = None

# --- Logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- Conversation Handler States ---
CHOOSE_LOCATION, CHOOSE_ACTION = range(2)

# --- Chapa Payment Function ---
async def generate_chapa_link(user_id: int, first_name: str, last_name: str, price: str) -> str:
    # We include the user_id in the tx_ref to identify them later
    tx_ref = f"ldeta-album-{user_id}-{uuid.uuid4()}"
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    payload = {
        "amount": price, "currency": "ETB", "email": f"{user_id}@telegram.user",
        "first_name": first_name, "last_name": last_name or first_name,
        "tx_ref": tx_ref,
        "callback_url": f"{RENDER_URL}/chapa_webhook", # This tells Chapa where to send the confirmation
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

# ... (other bot handlers remain the same) ...
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
        payment_link = await generate_chapa_link(user.id, user.first_name, user.last_name, ALBUM_PRICE)
        if payment_link:
            await update.message.reply_text(f"ክፍሊት ንምፍጻም ነዚ ዝስዕብ መላግቦ ተጠቐም:\n\n{payment_link}")
        else:
            await update.message.reply_text("ይቕሬታ! ኣብዚ እዋን'ዚ ናይ ክፍያ መላግቦ ክፍጠር ኣይተኻእለን።")
    elif choice == "🔙 ናብ መጀመርታ ተመለስ":
        await start_command(update, context)
        return ConversationHandler.END
    return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("መስርሕ ተቋሪጹ ኣሎ። ዳግማይ ንምጅማр /start በል።", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# --- Functions to run from the Webhook thread ---
async def send_success_message(user_id: int):
    """Sends the success message and channel invite link to the user."""
    try:
        # Create a one-time invite link to the private channel
        invite_link = await bot_app.bot.create_chat_invite_link(
            chat_id=PRIVATE_CHANNEL_ID,
            member_limit=1
        )
        await bot_app.bot.send_message(
            chat_id=user_id,
            text=(
                "ክፍሊትኩም ብዓወት ተፈጺሙ እዩ! የመስግነልና።\n\n"
                "ነዚ ሓደ ግዜ ጥራይ ዝሰርሕ መላግቦ ተጠቒምኩም ናብቲ መዝሙራት ዘለዎ ቻነል ክትኣትዉ ትኽእሉ ኢኹም፦\n"
                f"{invite_link.invite_link}"
            )
        )
        logging.info(f"Successfully sent invite link to user {user_id}")
    except Exception as e:
        logging.error(f"Failed to send invite link to user {user_id}: {e}")

# --- Web Server for Render Health Check & Chapa Webhook ---
class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # This is for Render's health check
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Bot is running and webhook is ready!", "utf-8"))

    def do_POST(self):
        if self.path == '/chapa_webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            logging.info(f"Webhook received: {data}")

            # Verification (optional but recommended for production)
            # You can verify the signature from Chapa here

            if data.get("status") == "success":
                tx_ref = data.get("tx_ref")
                try:
                    # Extract user_id from tx_ref like "ldeta-album-USERID-uuid"
                    user_id = int(tx_ref.split('-')[2])
                    logging.info(f"Payment success for user_id: {user_id}")
                    
                    # Schedule the async function to be run in the bot's event loop
                    asyncio.run_coroutine_threadsafe(send_success_message(user_id), bot_app.loop)
                    
                except (IndexError, ValueError) as e:
                    logging.error(f"Could not parse user_id from tx_ref: {tx_ref} - Error: {e}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("OK", "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_web_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, WebhookHandler)
    logging.info(f"Starting web server on port {PORT} for webhook...")
    httpd.serve_forever()

# --- Main Application Setup ---
def main() -> None:
    global bot_app
    if not all([TELEGRAM_TOKEN, CHAPA_SECRET_KEY, PRIVATE_CHANNEL_ID, RENDER_URL]):
        logging.error("!!! ERROR: Missing one or more environment variables. RENDER_EXTERNAL_URL is crucial.")
        return

    # Start the simple web server in a separate thread
    web_server_thread = threading.Thread(target=run_web_server)
    web_server_thread.daemon = True
    web_server_thread.start()

    # Create the Telegram Bot Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app = application # Store the application instance globally
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSE_LOCATION: [MessageHandler(filters.Regex("^(🇪🇹 ኣብ ውሽጢ ኢትዮጵያ|🌍 ካብ ኢትዮጵያ ወጻኢ)$"), handle_location_choice)],
            CHOOSE_ACTION: [MessageHandler(filters.Regex("^(✅ ኣልበም ግዛእ|🔙 ናብ መጀመርታ ተመለስ)$"), handle_buy_choice)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    application.add_handler(conv_handler)

    logging.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()