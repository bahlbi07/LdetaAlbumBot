import os
import sqlite3
import datetime
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode, ChatAction
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, ContextTypes, filters
)
from translations import TRANSLATIONS

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_CHAT_ID"))
POSTER = os.getenv("ALBUM_ART_FILE_ID")

CHANNEL_IDS = {
    "vol1": -1003548469381, "vol2": -1003540162347, "vol3": -1003582450486, "vol4": -1003606695407
}

# States
SELECT_LANG, GREETING, MENU, LOCATION, PAYMENT, ADMIN_BROADCAST = range(6)

DB_PATH = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT, join_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, album TEXT, price INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

def add_user(user_id, lang):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, lang, join_date) VALUES (?, ?, ?)", 
              (user_id, lang, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def record_sale(user_id, album):
    price = 300 if album == "vol4" else 100
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sales (user_id, album, price, date) VALUES (?, ?, ?, ?)",
              (user_id, album, price, datetime.datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

init_db()

def get_txt(lang, key, **kwargs):
    return TRANSLATIONS.get(lang, TRANSLATIONS["ti"]).get(key, key).format(**kwargs)

async def edit_any(query, text, keyboard):
    if query.message.photo:
        await query.edit_message_caption(caption=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# ───────────── USER FLOW ─────────────

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id, "ti")
    context.user_data.clear()
    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"), InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"), InlineKeyboardButton("🇪🇹 Oromoo", callback_data="l_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="l_saho")]
    ]
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.delete()
    
    if POSTER:
        await context.bot.send_photo(update.effective_chat.id, POSTER, caption="Please select your language", reply_markup=InlineKeyboardMarkup(kb))
    else:
        await context.bot.send_message(update.effective_chat.id, "Please select your language", reply_markup=InlineKeyboardMarkup(kb))
    return SELECT_LANG

async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = q.data.split("_")[1]
    context.user_data["lang"] = lang
    add_user(update.effective_user.id, lang)
    kb = [[InlineKeyboardButton(get_txt(lang, "btn_continue"), callback_data="go_menu")]]
    await edit_any(q, get_txt(lang, "welcome_text", user_name=update.effective_user.first_name), InlineKeyboardMarkup(kb))
    return GREETING

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = context.user_data["lang"]
    kb = [
        [InlineKeyboardButton(get_txt(lang, "vol4"), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_txt(lang, "vol3"), callback_data="buy_vol3"), InlineKeyboardButton(get_txt(lang, "vol2"), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_txt(lang, "vol1"), callback_data="buy_vol1"), InlineKeyboardButton(get_txt(lang, "btn_guide"), callback_data="guide")],
        [InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="restart")]
    ]
    await edit_any(q, get_txt(lang, "main_menu_prompt"), InlineKeyboardMarkup(kb))
    return MENU

async def guide_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = context.user_data["lang"]
    kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]
    await edit_any(q, get_txt(lang, "full_guide"), InlineKeyboardMarkup(kb))
    return MENU

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = context.user_data["lang"]
    if q.data.startswith("buy_"): context.user_data["album"] = q.data.replace("buy_", "")
    kb = [[InlineKeyboardButton(get_txt(lang, "loc_eth"), callback_data="loc_ok"), InlineKeyboardButton(get_txt(lang, "loc_intl"), callback_data="loc_no")],
          [InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]
    await edit_any(q, get_txt(lang, "ask_loc_text"), InlineKeyboardMarkup(kb))
    return LOCATION

async def payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = context.user_data["lang"]
    if q.data == "loc_no":
        kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]
        await edit_any(q, get_txt(lang, "loc_out_unavailable"), InlineKeyboardMarkup(kb))
        return LOCATION
    album = context.user_data["album"]
    price = "300" if album == "vol4" else "100"
    kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]
    await edit_any(q, get_txt(lang, "payment_instructions", album_title=album.upper(), price=price), InlineKeyboardMarkup(kb))
    return PAYMENT

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "ti")
    album = context.user_data.get("album", "vol1")
    user_id = update.effective_user.id
    admin_kb = [[InlineKeyboardButton("✅ Approve", callback_data=f"adm_app_{user_id}_{album}_{lang}"),
                 InlineKeyboardButton("❌ Reject", callback_data=f"adm_rej_{user_id}_{lang}")]]
    admin_msg = f"🔔 <b>ሓድሽ ክፍሊት</b>\n👤 ተጠቃሚ: {update.effective_user.first_name}\n💿 ኣልበም: {album.upper()}"
    if update.message.photo:
        await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, caption=admin_msg, reply_markup=InlineKeyboardMarkup(admin_kb), parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(ADMIN_ID, f"{admin_msg}\n📄 {update.message.text}", reply_markup=InlineKeyboardMarkup(admin_kb), parse_mode=ParseMode.HTML)
    await update.message.reply_text(get_txt(lang, "proof_received_msg"), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

# ───────────── ADMIN INDEPENDENT HANDLERS ─────────────

async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    kb = [[InlineKeyboardButton("📊 ጸብጻብ (Stats)", callback_data="adm_stats")],
          [InlineKeyboardButton("📢 መልእኽቲ ስደድ (Broadcast)", callback_data="adm_broadcast")]]
    await update.message.reply_text("<b>Admin Dashboard</b>", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)

async def reset_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM sales")
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    await update.message.reply_text("✅ ኩሉ ዳታ ናብ ዜሮ ተመሊሱ ኣሎ።")

async def admin_callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if update.effective_user.id != ADMIN_ID: return
    
    if q.data == "adm_stats":
        await q.answer()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT album, COUNT(*), SUM(price) FROM sales GROUP BY album")
        stats = c.fetchall()
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        conn.close()
        txt = f"<b>📊 ጸብጻብ</b>\n👤 ጠቕላላ ተጠቀምቲ: {total_users}\n\n"
        for s in stats: txt += f"💿 {s[0].upper()}: {s[1]} መሸጣ ({s[2]} ብር)\n"
        await q.message.reply_text(txt, parse_mode=ParseMode.HTML)
        
    elif q.data == "adm_broadcast":
        await q.answer()
        await q.message.reply_text("<b>በጃኹም መልእኽቲ ወይ ስእሊ ምስ ጽሑፍ ስደዱ (Broadcast)፦</b>", parse_mode=ParseMode.HTML)
        context.user_data["admin_state"] = "BROADCASTING"

async def broadcast_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only process if admin is in broadcasting state
    if update.effective_user.id != ADMIN_ID or context.user_data.get("admin_state") != "BROADCASTING":
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = c.fetchall()
    conn.close()
    
    count = 0
    for u in users:
        try:
            if update.message.photo:
                await context.bot.send_photo(chat_id=u[0], photo=update.message.photo[-1].file_id, caption=update.message.caption, parse_mode=ParseMode.HTML)
            elif update.message.text:
                await context.bot.send_message(chat_id=u[0], text=update.message.text, parse_mode=ParseMode.HTML)
            count += 1
        except: continue
        
    context.user_data["admin_state"] = None # Reset state
    await update.message.reply_text(f"✅ ናብ {count} ሰባት ተላኢኹ።")

async def admin_action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    parts = q.data.split("_")
    action, user_id, album, lang = parts[1], int(parts[2]), parts[3], parts[4]
    if action == "app":
        try:
            invite_link = await context.bot.create_chat_invite_link(chat_id=CHANNEL_IDS.get(album), member_limit=1)
            record_sale(user_id, album)
            await context.bot.send_message(chat_id=user_id, text=f"✅ <b>ክፍሊት ተረጋጊጹ!</b>\n\nእነሆ ሊንክ: {invite_link.invite_link}", parse_mode=ParseMode.HTML)
            await q.edit_message_caption(caption=q.message.caption + "\n✅ Approved", parse_mode=ParseMode.HTML)
        except Exception as e: await q.message.reply_text(f"Error: {str(e)}")
    elif action == "rej":
        await context.bot.send_message(chat_id=user_id, text="❌ <b>ክፍሊት ኣይተጸደቐን።</b>", parse_mode=ParseMode.HTML)
        await q.edit_message_caption(caption=q.message.caption + "\n❌ Rejected", parse_mode=ParseMode.HTML)

# ───────────── MAIN ─────────────

def main():
    app = Application.builder().token(TOKEN).build()
    
    # 1. Independent Admin Handlers (Priority)
    app.add_handler(CommandHandler("admin", admin_cmd))
    app.add_handler(CommandHandler("reset_database", reset_database))
    app.add_handler(CallbackQueryHandler(admin_callback_router, pattern="^adm_(stats|broadcast)"))
    app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, broadcast_msg_handler), group=1)
    
    # 2. Main User Conversation
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start_cmd), CallbackQueryHandler(start_cmd, pattern="restart")],
        states={
            SELECT_LANG: [CallbackQueryHandler(welcome_handler, "^l_")],
            GREETING: [CallbackQueryHandler(menu_handler, "^go_menu$")],
            MENU: [CallbackQueryHandler(guide_handler, "^guide$"), CallbackQueryHandler(location_handler, "^buy_"), CallbackQueryHandler(start_cmd, "^restart$")],
            LOCATION: [CallbackQueryHandler(payment_handler, "^loc_"), CallbackQueryHandler(menu_handler, "^go_menu$")],
            PAYMENT: [MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), proof_handler), CallbackQueryHandler(menu_handler, "^go_menu$")]
        },
        fallbacks=[CommandHandler("start", start_cmd)]
    )
    
    app.add_handler(CallbackQueryHandler(admin_action_callback, pattern="^adm_(app|rej)"))
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__": main()