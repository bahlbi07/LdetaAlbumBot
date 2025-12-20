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

# --- State Definitions for Conversation ---
SELECT_LANG, SELECT_ALBUM, SELECT_LOCATION, AWAIT_PROOF, SHOW_GUIDE, SHOW_HELP = range(6)

def get_text(context, key, **kwargs):
    lang = context.user_data.get('lang', 'ti')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, f"_{key}_").format(**kwargs)

# --- Handlers ---
async def start_command(update, context):
    context.user_data.clear()
    if update.callback_query:
        await update.callback_query.answer()
        try: await update.callback_query.message.delete()
        except: pass

    keyboard = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ (ኢሮብ)", callback_data="lang_saho")],
        [InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="lang_om")]
    ]
    msg_obj = update.message or (update.callback_query and update.callback_query.message)
    prompt = TRANSLATIONS['en']['language_select_prompt']
    if ALBUM_ART_FILE_ID and not update.callback_query:
        await msg_obj.reply_photo(photo=ALBUM_ART_FILE_ID, caption=prompt, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await msg_obj.reply_text(prompt, reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_LANG

async def select_language_handler(update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['lang'] = query.data.split('_')[1]

    if context.user_data['lang'] == 'saho':
        kb = [[InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")]]
        await query.edit_message_text(text=get_text(context, 'saho_unavailable'), reply_markup=InlineKeyboardMarkup(kb))
        return SELECT_LANG

    try: await query.message.delete()
    except: pass
    return await show_main_menu(update, context)

async def show_main_menu(update, context):
    kb = [
        [InlineKeyboardButton(get_text(context, 'album_vol_4'), callback_data="select_vol4")],
        [InlineKeyboardButton(get_text(context, 'album_vol_3'), callback_data="select_vol3")],
        [InlineKeyboardButton(get_text(context, 'album_vol_2'), callback_data="select_vol2")],
        [InlineKeyboardButton(get_text(context, 'album_vol_1'), callback_data="select_vol1")],
        [InlineKeyboardButton(get_text(context, 'how_to_buy_button'), callback_data="show_guide")],
        [InlineKeyboardButton(get_text(context, 'home_button'), callback_data="back_to_start")],
        [InlineKeyboardButton(get_text(context, 'help_button'), callback_data="help_main_menu")]
    ]
    welcome_text = get_text(context, 'welcome_message', user_name=update.effective_user.first_name)
    msg_text = f"{welcome_text}\n\n{get_text(context, 'main_menu_prompt')}"

    # We need to send a new message because we deleted the old one.
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg_text,
        reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML
    )
    return SELECT_ALBUM

async def main_menu_dispatcher(update, context):
    """Handles all buttons pressed on the main album menu."""
    query = update.callback_query; await query.answer()
    
    if query.data.startswith("select_vol"): # Album selected
        context.user_data['album_key'] = query.data.split('_')[1]
        context.user_data['album_title'] = get_text(context, f'album_{context.user_data["album_key"]}')
        kb = [
            [InlineKeyboardButton(get_text(context, 'location_in_button'), callback_data="location_in")],
            [InlineKeyboardButton(get_text(context, 'location_out_button'), callback_data="location_out")],
            [InlineKeyboardButton(get_text(context, 'back_button'), callback_data="back_to_main_menu")]
        ]
        await query.edit_message_text(get_text(context, 'ask_location'), reply_markup=InlineKeyboardMarkup(kb))
        return SELECT_LOCATION
    
    elif query.data == "show_guide": # How to buy
        kb = [[InlineKeyboardButton(get_text(context, 'back_button'), callback_data="back_to_main_menu")]]
        await query.edit_message_text(get_text(context, 'guide_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        return SELECT_ALBUM # Stay in same state
    
    elif query.data == "help_main_menu": # Help
        kb = [[InlineKeyboardButton(get_text(context, 'back_button'), callback_data="back_to_main_menu")]]
        await query.edit_message_text(get_text(context, 'help_text_main_menu'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        return SELECT_ALBUM

async def select_location_handler(update, context):
    query = update.callback_query; await query.answer()

    if query.data == 'location_out':
        await query.edit_message_text(text=get_text(context, 'location_out_unavailable'))
        await asyncio.sleep(4)
        return await show_main_menu(update, context)

    price = ALBUM_PRICE_VOL4 if context.user_data.get('album_key') == 'vol4' else ALBUM_PRICE_OTHERS
    payment_text = get_text(context, 'payment_instructions_ethiopia', album_title=context.user_data.get('album_title', ''), album_price=price)
    kb = [
        [InlineKeyboardButton(get_text(context, 'back_button'), callback_data=f"select_{context.user_data.get('album_key')}")],
        [InlineKeyboardButton(get_text(context, 'help_button'), callback_data="help_payment")]
    ]
    await query.edit_message_text(text=payment_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return AWAIT_PROOF

async def proof_handler(update, context):
    user = update.effective_user; album_title = context.user_data.get('album_title', ''); album_key = context.user_data.get('album_key', 'unknown')
    notif_text = get_text(context, 'admin_notification', user_mention=user.mention_html(), user_id=user.id, album_title=album_title, album_key=album_key)
    try:
        if update.message.text:
            await context.bot.send_message(ADMIN_CHAT_ID, f"{notif_text}\n<b>Trans ID:</b> <code>{update.message.text}</code>", parse_mode=ParseMode.HTML)
        elif update.message.photo:
            await context.bot.send_message(ADMIN_CHAT_ID, notif_text, parse_mode=ParseMode.HTML)
            await update.message.forward(ADMIN_CHAT_ID)
        await update.message.reply_text(get_text(context, 'proof_received'), parse_mode=ParseMode.HTML)
    except: await update.message.reply_text(get_text(context, 'payment_rejected_user'))
    return ConversationHandler.END

# --- ADMIN COMMANDS ---
async def admin_command_handler(update, context, approve=True):
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID): return
    command = "approve" if approve else "reject"
    if not context.args or (approve and len(context.args) != 2) or (not approve and len(context.args) != 1):
        return await update.message.reply_text(get_text(context, f'{command}_usage'))
    try:
        user_id = int(context.args[0])
        if approve:
            album_key = context.args[1].lower()
            album_title = get_text({'user_data': {'lang': 'ti'}}, f'album_{album_key}')
            await send_success_message(user_id, album_key, album_title)
            await update.message.reply_text(get_text(context, 'approval_success_admin', user_id=user_id, album_title=album_title))
        else: # Reject
            await context.bot.send_message(user_id, get_text(context, 'payment_rejected_user'), parse_mode=ParseMode.HTML)
            await update.message.reply_text(get_text(context, 'rejection_success_admin', user_id=user_id))
    except: await update.message.reply_text(f"Invalid args for /{command}.")

# --- Utility & Web ---
async def send_success_message(user_id, album_key, album_title):
    # Simplified logic from previous version
    invite_link = await bot_app.bot.create_chat_invite_link(CHANNEL_IDS[album_key], member_limit=1)
    await bot_app.bot.send_message(user_id, get_text({},'approve_success_user_privacy', invite_link=invite_link.invite_link), parse_mode=ParseMode.HTML)

# Web Server can remain the same
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.send_header("Content-type", "text/plain"); self.end_headers(); self.wfile.write(bytes("Bot running!", "utf-8"))
def run_web_server():
    httpd = HTTPServer(('', PORT), HealthCheckHandler); httpd.serve_forever()

# --- MAIN ---
def main():
    global bot_app
    if not all([TELEGRAM_TOKEN, ADMIN_CHAT_ID] + list(CHANNEL_IDS.values())):
        logging.critical("CRITICAL: Missing essential environment variables."); return

    threading.Thread(target=run_web_server, daemon=True).start()
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app = application
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            SELECT_LANG: [CallbackQueryHandler(select_language_handler, pattern="^lang_")],
            SELECT_ALBUM: [CallbackQueryHandler(main_menu_dispatcher)],
            SELECT_LOCATION: [
                CallbackQueryHandler(select_location_handler, pattern="^location_"),
                CallbackQueryHandler(show_main_menu, pattern="^back_to_main_menu$")
            ],
            AWAIT_PROOF: [MessageHandler(filters.TEXT | filters.PHOTO, proof_handler)],
        },
        fallbacks=[CallbackQueryHandler(start_command, pattern="^back_to_start$")],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("approve", lambda u,c: admin_command_handler(u,c,approve=True)))
    application.add_handler(CommandHandler("reject", lambda u,c: admin_command_handler(u,c,approve=False)))

    logging.info("Starting bot..."); application.run_polling()

if __name__ == "__main__":
    main()