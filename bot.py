# FINAL CORRECTED bot.py file
import logging, os, threading, asyncio
from datetime import timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    Application, CommandHandler, ContextTypes, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
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
CHANNEL_IDS = {
    'vol4': int(os.getenv("CHANNEL_ID_VOL_4", 0)),
    'vol3': int(os.getenv("CHANNEL_ID_VOL_3", 0)),
    'vol2': int(os.getenv("CHANNEL_ID_VOL_2", 0)),
    'vol1': int(os.getenv("CHANNEL_ID_VOL_1", 0)),
}

bot_app = None
logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- State Definitions ---
SELECT_LANG, SELECT_ALBUM, SELECT_LOCATION, AWAIT_PROOF = range(4)

def get_text(lang, key, **kwargs):
    """Helper to get translated text based on language code."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, f"_{key}_").format(**kwargs)

# --- Handlers ---
async def start_command(update, context):
    context.user_data.clear()
    keyboard = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="lang_saho")],
        [InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="lang_om")]
    ]
    prompt = TRANSLATIONS['ti']['welcome_language'] # Default to Tigrinya for start
    
    if ALBUM_ART_FILE_ID:
        await update.message.reply_photo(photo=ALBUM_ART_FILE_ID, caption=prompt, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(prompt, reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_LANG

async def select_language_handler(update, context):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split('_')[1]
    context.user_data['lang'] = lang_code
    
    return await show_main_menu(update, context)

async def show_main_menu(update, context):
    lang = context.user_data.get('lang', 'ti')
    kb = [
        [InlineKeyboardButton(get_text(lang, 'album_vol_4'), callback_data="select_vol4")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_3'), callback_data="select_vol3")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_2'), callback_data="select_vol2")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_1'), callback_data="select_vol1")],
        [InlineKeyboardButton(get_text(lang, 'how_to_buy_button'), callback_data="show_guide")],
        [InlineKeyboardButton(get_text(lang, 'help_button'), callback_data="help_main_menu")]
    ]
    welcome_text = get_text(lang, 'welcome_message', user_name=update.effective_user.first_name)
    msg_text = f"{welcome_text}\n\n{get_text(lang, 'main_menu_prompt')}"

    if update.callback_query:
        await update.callback_query.edit_message_text(text=msg_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return SELECT_ALBUM

async def main_menu_dispatcher(update, context):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'ti')
    
    if query.data.startswith("select_vol"):
        context.user_data['album_key'] = query.data.split('_')[1]
        context.user_data['album_title'] = get_text(lang, f'album_{context.user_data["album_key"]}')
        kb = [
            [InlineKeyboardButton(get_text(lang, 'location_in_button'), callback_data="location_in")],
            [InlineKeyboardButton(get_text(lang, 'location_out_button'), callback_data="location_out")],
            [InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="back_to_main_menu")]
        ]
        await query.edit_message_text(get_text(lang, 'ask_location'), reply_markup=InlineKeyboardMarkup(kb))
        return SELECT_LOCATION
    
    elif query.data == "show_guide":
        kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="back_to_main_menu")]]
        await query.edit_message_text(get_text(lang, 'guide_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        return SELECT_ALBUM
    
    elif query.data == "help_main_menu":
        kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="back_to_main_menu")]]
        await query.edit_message_text(get_text(lang, 'help_text_main_menu'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        return SELECT_ALBUM

async def select_location_handler(update, context):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'ti')

    if query.data == 'location_out':
        kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="back_to_main_menu")]]
        await query.edit_message_text(text=get_text(lang, 'location_out_unavailable'), reply_markup=InlineKeyboardMarkup(kb))
        return SELECT_ALBUM

    if query.data == 'back_to_main_menu':
        return await show_main_menu(update, context)

    price = ALBUM_PRICE_VOL4 if context.user_data.get('album_key') == 'vol4' else ALBUM_PRICE_OTHERS
    payment_text = get_text(lang, 'payment_instructions_ethiopia', album_title=context.user_data.get('album_title', ''), album_price=price)
    kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="back_to_main_menu")]]
    await query.edit_message_text(text=payment_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return AWAIT_PROOF

async def proof_handler(update, context):
    lang = context.user_data.get('lang', 'ti')
    user = update.effective_user
    album_title = context.user_data.get('album_title', '')
    album_key = context.user_data.get('album_key', 'unknown')
    
    notif_text = get_text('en', 'admin_notification', user_mention=user.mention_html(), user_id=user.id, album_title=album_title, album_key=album_key)
    
    try:
        if update.message.text:
            await context.bot.send_message(ADMIN_CHAT_ID, f"{notif_text}\n<b>Trans ID:</b> <code>{update.message.text}</code>", parse_mode=ParseMode.HTML)
        elif update.message.photo:
            await context.bot.send_message(ADMIN_CHAT_ID, notif_text, parse_mode=ParseMode.HTML)
            await update.message.forward(ADMIN_CHAT_ID)
        
        await update.message.reply_text(get_text(lang, 'slip_received'), parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Error in proof_handler: {e}")
        await update.message.reply_text("Error sending proof. Please try again later.")
    
    return ConversationHandler.END

# --- ADMIN COMMANDS ---
async def admin_command_handler(update, context, approve=True):
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID): return
    if not context.args: return await update.message.reply_text("Usage: /approve [user_id] [volX] or /reject [user_id]")
    
    try:
        user_id = int(context.args[0])
        if approve:
            album_key = context.args[1].lower()
            invite_link = await context.bot.create_chat_invite_link(CHANNEL_IDS[album_key], member_limit=1)
            # Default to Amharic/Tigrinya for user notification if lang not known
            msg = get_text('ti', 'payment_success_user_privacy', user_name="User", invite_link=invite_link.invite_link)
            await context.bot.send_message(user_id, msg, parse_mode=ParseMode.HTML)
            await update.message.reply_text(f"Approved user {user_id} for {album_key}")
        else:
            await context.bot.send_message(user_id, get_text('ti', 'payment_rejected_user'), parse_mode=ParseMode.HTML)
            await update.message.reply_text(f"Rejected user {user_id}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# --- Web Server ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"Bot is alive")

def run_web_server():
    HTTPServer(('', PORT), HealthCheckHandler).serve_forever()

def main():
    threading.Thread(target=run_web_server, daemon=True).start()
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            SELECT_LANG: [CallbackQueryHandler(select_language_handler, pattern="^lang_")],
            SELECT_ALBUM: [CallbackQueryHandler(main_menu_dispatcher)],
            SELECT_LOCATION: [CallbackQueryHandler(select_location_handler)],
            AWAIT_PROOF: [MessageHandler(filters.TEXT | filters.PHOTO, proof_handler)],
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("approve", lambda u,c: admin_command_handler(u,c,approve=True)))
    application.add_handler(CommandHandler("reject", lambda u,c: admin_command_handler(u,c,approve=False)))

    application.run_polling()

if __name__ == "__main__":
    main()