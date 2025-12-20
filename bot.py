import logging, os, threading, asyncio
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
)

from translations import TRANSLATIONS

load_dotenv()

# --- Configurations ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ALBUM_ART_FILE_ID = os.getenv("ALBUM_ART_FILE_ID")
PORT = int(os.environ.get('PORT', 8080))
CHANNEL_IDS = {
    'vol4': int(os.getenv("CHANNEL_ID_VOL_4", 0)),
    'vol3': int(os.getenv("CHANNEL_ID_VOL_3", 0)),
    'vol2': int(os.getenv("CHANNEL_ID_VOL_2", 0)),
    'vol1': int(os.getenv("CHANNEL_ID_VOL_1", 0)),
}

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# --- Enhanced Conversation States ---
(START_STAGE, WELCOME_STAGE, MENU_STAGE, LOCATION_STAGE, 
 PROOF_STAGE, GUIDE_STAGE, HELP_STAGE) = range(7)

def get_text(lang, key, **kwargs):
    return TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, f"_{key}_").format(**kwargs)

# --- Core Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ደረጃ 1: ፖስተርን ቋንቋ ጥራይን"""
    context.user_data.clear()
    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="lang_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇹 Afaan Oromoo", callback_data="lang_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="lang_saho")]
    ]
    
    if update.callback_query:
        await update.callback_query.answer()
        msg = update.callback_query.message
        if ALBUM_ART_FILE_ID:
            await msg.edit_caption(caption="<b>Please Select Your Language</b>", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        else:
            await msg.edit_text("<b>Please Select Your Language</b>", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    else:
        if ALBUM_ART_FILE_ID:
            await update.message.reply_photo(photo=ALBUM_ART_FILE_ID, caption="<b>Please Select Your Language</b>", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("<b>Please Select Your Language</b>", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return START_STAGE

async def lang_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ደረጃ 2: እንኳዕ ብደሓን መጻእካ (መንፈሳዊ ሰላምታ)"""
    query = update.callback_query; await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    
    kb = [[InlineKeyboardButton(get_text(lang, 'enter_store_btn'), callback_data="go_to_menu")]]
    welcome_text = get_text(lang, 'welcome_msg', user_name=update.effective_user.first_name)
    
    await query.edit_message_caption(caption=welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return WELCOME_STAGE

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ደረጃ 3: ቀንዲ ማእኸል ኣልበማት"""
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    
    kb = [
        [InlineKeyboardButton(get_text(lang, 'album_vol_4'), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_3'), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_2'), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_text(lang, 'album_vol_1'), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_text(lang, 'guide_button'), callback_data="go_guide")],
        [InlineKeyboardButton(get_text(lang, 'help_button'), callback_data="go_help")],
        [InlineKeyboardButton(get_text(lang, 'back_to_lang'), callback_data="restart")]
    ]
    await query.edit_message_caption(caption=get_text(lang, 'main_menu_prompt'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU_STAGE

async def album_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ደረጃ 4: ምርጫ ቦታ"""
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    album_key = query.data.split('_')[1]
    context.user_data['album_key'] = album_key
    
    kb = [
        [InlineKeyboardButton(get_text(lang, 'loc_in'), callback_data="loc_et")],
        [InlineKeyboardButton(get_text(lang, 'loc_out'), callback_data="loc_os")],
        [InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="go_to_menu")]
    ]
    await query.edit_message_caption(caption=get_text(lang, 'ask_loc_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return LOCATION_STAGE

async def payment_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ደረጃ 5: ናይ ክፍሊት ሓበሬታ"""
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    
    if query.data == "loc_os":
        kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="go_to_menu")]]
        await query.edit_message_caption(caption=get_text(lang, 'loc_out_unavailable'), reply_markup=InlineKeyboardMarkup(kb))
        return LOCATION_STAGE

    album_key = context.user_data['album_key']
    price = "300" if album_key == "vol4" else "100"
    instr = get_text(lang, 'payment_instructions', album_title=album_key.upper(), price=price)
    
    kb = [
        [InlineKeyboardButton(get_text(lang, 'help_button'), callback_data="go_help")],
        [InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="go_to_menu")]
    ]
    await query.edit_message_caption(caption=instr, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return PROOF_STAGE

async def guide_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ቀሊል መምርሒ (ንህጻን ዝርድኦ)"""
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="go_to_menu")]]
    await query.edit_message_caption(caption=get_text(lang, 'full_guide'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU_STAGE

async def help_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ሓገዝ ገጽ"""
    query = update.callback_query; await query.answer()
    lang = context.user_data.get('lang', 'ti')
    kb = [[InlineKeyboardButton(get_text(lang, 'back_button'), callback_data="go_to_menu")]]
    await query.edit_message_caption(caption=get_text(lang, 'help_page_text'), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    return MENU_STAGE

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """መረጋገጺ ምቕባል"""
    lang = context.user_data.get('lang', 'ti')
    user = update.effective_user
    album_key = context.user_data.get('album_key', 'N/A')
    
    # Notify Admin
    admin_msg = f"🔔 <b>New Payment!</b>\nUser: {user.mention_html()}\nID: <code>{user.id}</code>\nAlbum: {album_key}\n\nApprove: `/approve {user.id} {album_key}`"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode=ParseMode.HTML)
    if update.message.photo: await update.message.forward(ADMIN_CHAT_ID)
    elif update.message.text: await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Trans ID: {update.message.text}")

    await update.message.reply_text(get_text(lang, 'proof_received_msg'), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

# --- Admin Function ---
async def approve_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != str(ADMIN_CHAT_ID): return
    try:
        user_id, album_key = int(context.args[0]), context.args[1]
        invite = await context.bot.create_chat_invite_link(chat_id=CHANNEL_IDS[album_key], member_limit=1)
        # Success message to user
        msg = get_text('ti', 'success_user_msg', album_title=album_key.upper())
        await context.bot.send_message(chat_id=user_id, text=f"{msg}\n\n🔗 <b>Link:</b> {invite.invite_link}", parse_mode=ParseMode.HTML)
        # Final encouraging message
        await context.bot.send_message(chat_id=user_id, text=get_text('ti', 'feedback_invite'), parse_mode=ParseMode.HTML)
        await update.message.reply_text(f"✅ User {user_id} Approved.")
    except: await update.message.reply_text("Usage: /approve [id] [volX]")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            START_STAGE: [CallbackQueryHandler(lang_selected, pattern="^lang_")],
            WELCOME_STAGE: [CallbackQueryHandler(main_menu, pattern="^go_to_menu$")],
            MENU_STAGE: [
                CallbackQueryHandler(album_details, pattern="^buy_"),
                CallbackQueryHandler(guide_screen, pattern="^go_guide$"),
                CallbackQueryHandler(help_screen, pattern="^go_help$"),
                CallbackQueryHandler(start_command, pattern="^restart$")
            ],
            LOCATION_STAGE: [
                CallbackQueryHandler(payment_screen, pattern="^loc_"),
                CallbackQueryHandler(main_menu, pattern="^go_to_menu$")
            ],
            PROOF_STAGE: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, proof_handler),
                CallbackQueryHandler(main_menu, pattern="^go_to_menu$"),
                CallbackQueryHandler(help_screen, pattern="^go_help$")
            ]
        },
        fallbacks=[CommandHandler("start", start_command)]
    )
    
    app.add_handler(conv)
    app.add_handler(CommandHandler("approve", approve_cmd))
    app.run_polling()

if __name__ == "__main__": main()