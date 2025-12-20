import logging, os, threading, asyncio
from datetime import timedelta
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    Application, CommandHandler, ContextTypes, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
)

from translations import TRANSLATIONS

load_dotenv()

# --- Config ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ALBUM_PRICE_VOL4 = "300"
ALBUM_PRICE_OTHERS = "100"
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")
PORT = int(os.environ.get('PORT', 8080))
CHANNEL_IDS = {
    'vol4': int(os.getenv("CHANNEL_ID_VOL_4", 0)),
    'vol3': int(os.getenv("CHANNEL_ID_VOL_3", 0)),
    'vol2': int(os.getenv("CHANNEL_ID_VOL_2", 0)),
    'vol1': int(os.getenv("CHANNEL_ID_VOL_1", 0)),
}

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# --- States ---
SELECT_LANG, WELCOME_SCREEN, MAIN_MENU, SELECT_LOCATION, AWAIT_PROOF, SHOW_HELP = range(6)

def get_text(lang, key, **kwargs):
    return TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, f"_{key}_").format(**kwargs)

# --- Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """1. መጀመሪያ ቋንቋ ጥራይ ምስ ፖስተር"""
    context.user_data.clear()
    keyboard = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="lang_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="lang_saho")]
    ]
    
    if ALBUM_ART_FILE_ID:
        await update.message.reply_photo(photo=ALBUM_ART_FILE_ID, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("Please select your language / በጃኹም ቋንቋ ምረጹ / እባክዎ ቋንቋ ይምረጡ", reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_LANG

async def lang_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """2. ድሕሪ ቋንቋ ምምራጽ - እንኳዕ ብደሓን መጻእካ"""
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    
    keyboard = [[InlineKeyboardButton(get_text(lang, 'continue_button'), callback_data="show_main_menu")]]
    welcome_text = get_text(lang, 'welcome_msg', user_name=update.effective_user.first_name)
    
    await query.message.delete()
    if ALBUM_ART_FILE_ID:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=ALBUM_ART_FILE_ID, caption=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    return WELCOME_SCREEN

async def main_menu_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """3. ዝርዝር ኣልበማት"""
    query = update.callback_query
    if query: await query.answer()
    lang = context.user_data.get('lang', 'ti')
    
    kb = [
        [InlineKeyboardButton(get_text(lang, 'album_vol_4'), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_3'), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_2'), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_1'), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_text(lang, 'guide_button'), callback_data="show_guide")],
        [InlineKeyboardButton(get_text(lang, 'help_button'), callback_data="help_main")],
        [InlineKeyboardButton(get_text(lang, 'back_to_lang'), callback_data="restart")]
    ]
    
    text = get_text(lang, 'main_menu_prompt')
    if query and query.message.caption:
        await query.edit_message_caption(caption=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MAIN_MENU

async def buy_album_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """4. ምርጫ ቦታ (ኢትዮጵያ ወይ ወጻኢ)"""
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    album_key = query.data.split('_')[1]
    context.user_data['album_key'] = album_key
    context.user_data['album_title'] = get_text(lang, f'album_{album_key}')
    
    kb = [
        [InlineKeyboardButton(get_text(lang, 'loc_in'), callback_data="loc_ethiopia")],
        [InlineKeyboardButton(get_text(lang, 'loc_out'), callback_data="loc_outside")],
        [InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="show_main_menu")],
        [InlineKeyboardButton(get_text(lang, 'back_to_lang'), callback_data="restart")]
    ]
    await query.edit_message_caption(caption=get_text(lang, 'ask_loc_text'), reply_markup=InlineKeyboardMarkup(kb))
    return SELECT_LOCATION

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    
    if query.data == "loc_outside":
        kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="show_main_menu")], [InlineKeyboardButton(get_text(lang, 'back_to_lang'), callback_data="restart")]]
        await query.edit_message_caption(caption=get_text(lang, 'loc_out_unavailable'), reply_markup=InlineKeyboardMarkup(kb))
        return SELECT_LOCATION

    # Inside Ethiopia - Show Bank Details
    album_key = context.user_data['album_key']
    price = ALBUM_PRICE_VOL4 if album_key == 'vol4' else ALBUM_PRICE_OTHERS
    instr = get_text(lang, 'payment_instructions', album_title=context.user_data['album_title'], price=price)
    
    kb = [[InlineKeyboardButton(get_text(lang, 'help_button'), callback_data="help_payment")], [InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="show_main_menu")]]
    await query.edit_message_caption(caption=instr, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return AWAIT_PROOF

async def proof_receiver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """5. መረጋገጺ ምቕባል"""
    lang = context.user_data.get('lang', 'ti')
    user = update.effective_user
    album_title = context.user_data.get('album_title')
    album_key = context.user_data.get('album_key')
    
    # Notify Admin
    admin_msg = f"🔔 <b>New Payment!</b>\nUser: {user.mention_html()}\nID: <code>{user.id}</code>\nAlbum: {album_title}\n\nApprove: `/approve {user.id} {album_key}`\nReject: `/reject {user.id}`"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode=ParseMode.HTML)
    if update.message.photo:
        await update.message.forward(ADMIN_CHAT_ID)
    elif update.message.text:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Trans ID: {update.message.text}")

    await update.message.reply_text(get_text(lang, 'proof_received_msg'), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

# --- Admin System ---

async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID): return
    try:
        user_id = int(context.args[0]); album_key = context.args[1]
        channel_id = CHANNEL_IDS[album_key]
        
        # Try Auto-Add
        try:
            await context.bot.unban_chat_member(chat_id=channel_id, user_id=user_id, only_if_banned=True)
            # Create link anyway as fallback
            invite = await context.bot.create_chat_invite_link(chat_id=channel_id, member_limit=1)
            
            # Send Success Message
            success_text = get_text('ti', 'success_user_msg', user_name="ሰላም", album_title=album_key)
            await context.bot.send_message(chat_id=user_id, text=success_text, parse_mode=ParseMode.HTML)
            await context.bot.send_message(chat_id=user_id, text=f"🔗 Link: {invite.invite_link}")
            await update.message.reply_text(f"✅ Approved {user_id}")
        except Exception as e:
            # Privacy setting fallback
            invite = await context.bot.create_chat_invite_link(chat_id=channel_id, member_limit=1)
            privacy_msg = get_text('ti', 'privacy_fallback_msg', user_name="User", album_title=album_key, invite_link=invite.invite_link)
            await context.bot.send_message(chat_id=user_id, text=privacy_msg, parse_mode=ParseMode.HTML)
            await update.message.reply_text(f"✅ Approved (Sent via Link due to privacy)")
    except:
        await update.message.reply_text("Use: /approve [user_id] [vol1/2/3/4]")

# --- Helpers ---
async def show_help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    help_type = query.data # help_main or help_payment
    text = get_text(lang, f'help_text_{help_type.split("_")[1]}')
    kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="show_main_menu")]]
    await query.edit_message_caption(caption=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)

async def show_guide_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="show_main_menu")], [InlineKeyboardButton(get_text(lang, 'back_to_lang'), callback_data="restart")]]
    await query.edit_message_caption(caption=get_text(lang, 'full_guide'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            SELECT_LANG: [CallbackQueryHandler(lang_selected, pattern="^lang_")],
            WELCOME_SCREEN: [CallbackQueryHandler(main_menu_screen, pattern="show_main_menu")],
            MAIN_MENU: [
                CallbackQueryHandler(buy_album_handler, pattern="^buy_"),
                CallbackQueryHandler(show_guide_handler, pattern="show_guide"),
                CallbackQueryHandler(show_help_handler, pattern="^help_"),
                CallbackQueryHandler(start_command, pattern="restart")
            ],
            SELECT_LOCATION: [
                CallbackQueryHandler(location_handler, pattern="^loc_"),
                CallbackQueryHandler(main_menu_screen, pattern="show_main_menu"),
                CallbackQueryHandler(start_command, pattern="restart")
            ],
            AWAIT_PROOF: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, proof_receiver),
                CallbackQueryHandler(show_help_handler, pattern="^help_"),
                CallbackQueryHandler(main_menu_screen, pattern="show_main_menu")
            ]
        },
        fallbacks=[CommandHandler("start", start_command)]
    )
    
    app.add_handler(conv)
    app.add_handler(CommandHandler("approve", approve_user))
    app.run_polling()

if __name__ == "__main__":
    main()