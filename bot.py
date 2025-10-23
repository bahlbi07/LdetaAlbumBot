import logging
import os
import uuid
import requests
import threading
import json
import asyncio
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "100")
PORT = int(os.environ.get('PORT', 8080))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

# --- Global variable to hold the bot application instance ---
bot_app = None

# --- Logging ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- Conversation Handler States ---
CHOOSE_ACTION = 1

# --- Chapa Payment Function ---
async def generate_chapa_link(user_id: int, first_name: str, last_name: str, price: str) -> str:
    tx_ref = f"ldeta-album-{user_id}-{uuid.uuid4()}"
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    payload = {
        "amount": price, "currency": "ETB", "email": f"{user_id}@telegram.user",
        "first_name": first_name, "last_name": last_name or first_name,
        "tx_ref": tx_ref,
        "callback_url": f"{RENDER_URL}/chapa_webhook",
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
    keyboard = [
        [InlineKeyboardButton("🇪🇹 ኣብ ውሽጢ ኢትዮጵያ", callback_data="location_ethiopia")],
        [InlineKeyboardButton("🌍 ካብ ኢትዮጵያ ወጻኢ", callback_data="location_outside")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Check if this is a new start or a callback
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=f"ሰላም {update.effective_user.first_name}! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ኣበይ ከም ዘለኻ ምረጽ፦",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            f"ሰላም {update.effective_user.first_name}! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ኣበይ ከም ዘለኻ ምረጽ፦",
            reply_markup=reply_markup
        )
    return CHOOSE_ACTION

async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer() # Respond to the button press
    
    user_choice = query.data
    user = update.effective_user

    if user_choice == "location_ethiopia":
        keyboard = [
            [InlineKeyboardButton("✅ ኣልበም ግዛእ", callback_data="buy_album")],
            [InlineKeyboardButton("🔙 ናብ መጀመርታ ተመለስ", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"ጽቡቕ ምርጫ! ዋጋ ናይ'ዚ ራብዓይ ኣልበም {ALBUM_PRICE} ብር እዩ።\n\nክፍሊት ንምፍጻም 'ኣልበም ግዛእ' ዝብል ጠውቕ።",
            reply_markup=reply_markup
        )
        return CHOOSE_ACTION

    elif user_choice == "location_outside":
        await query.edit_message_text(text="እዚ ናይ ወጻኢ ክፍያ ኣገልግሎት ኣብዚ እዋን'ዚ ኣይጀመረን። ኣብ ቀረባ እዋን ክንጅምር ኢና።")
        return ConversationHandler.END

    elif user_choice == "buy_album":
        await query.edit_message_text(text="የመስግነልና! ናይ ክፍያ መላግቦ እናዳለና ስለ ዝኾና በጃኻ ጽንሕ በል።")
        payment_link = await generate_chapa_link(user.id, user.first_name, user.last_name, ALBUM_PRICE)
        if payment_link:
            await query.message.reply_text(f"ክፍሊት ንምፍጻም ነዚ ዝስዕብ መላግቦ ተጠቐም:\n\n{payment_link}")
        else:
            await query.message.reply_text("ይቕሬታ! ኣብዚ እዋን'ዚ ናይ ክፍያ መላግቦ ክፍጠር ኣይተኻእለን።")
        return ConversationHandler.END
        
    elif user_choice == "back_to_start":
        return await start_command(update, context)

    return ConversationHandler.END

# ... (Webhook functions and Web Server remain the same) ...
async def send_success_message(user_id: int):
    try:
        invite_link = await bot_app.bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
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

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers()
        self.wfile.write(bytes("Bot is running and webhook is ready!", "utf-8"))
    def do_POST(self):
        if self.path == '/chapa_webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length); data = json.loads(post_data)
            logging.info(f"Webhook received: {data}")
            if data.get("status") == "success":
                tx_ref = data.get("tx_ref")
                try:
                    user_id = int(tx_ref.split('-')[2])
                    logging.info(f"Payment success for user_id: {user_id}")
                    asyncio.run_coroutine_threadsafe(send_success_message(user_id), bot_app.loop)
                except (IndexError, ValueError) as e:
                    logging.error(f"Could not parse user_id from tx_ref: {tx_ref} - Error: {e}")
            self.send_response(200); self.end_headers(); self.wfile.write(bytes("OK", "utf-8"))
        else: self.send_response(404); self.end_headers()

def run_web_server():
    server_address = ('', PORT); httpd = HTTPServer(server_address, WebhookHandler)
    logging.info(f"Starting web server on port {PORT} for webhook..."); httpd.serve_forever()

def main() -> None:
    global bot_app
    if not all([TELEGRAM_TOKEN, CHAPA_SECRET_KEY, PRIVATE_CHANNEL_ID, RENDER_URL]):
        logging.error("!!! ERROR: Missing one or more environment variables."); return
    web_server_thread = threading.Thread(target=run_web_server); web_server_thread.daemon = True; web_server_thread.start()
    application = Application.builder().token(TELEGRAM_TOKEN).build(); bot_app = application
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={CHOOSE_ACTION: [CallbackQueryHandler(handle_button_press)]},
        fallbacks=[CommandHandler("start", start_command)],
        allow_reentry=True
    )
    application.add_handler(conv_handler)
    logging.info("Starting bot polling..."); application.run_polling()
if __name__ == "__main__": main()