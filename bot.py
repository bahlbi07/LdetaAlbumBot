import os
import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, ContextTypes, filters
)
from translations import TRANSLATIONS

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_CHAT_ID"))
POSTER = os.getenv("ALBUM_ART_FILE_ID")

SELECT_LANG, GREETING, MENU, LOCATION, PAYMENT = range(5)
# ንኣድሚን ምኽንያት ንምጽሓፍ ዘድሊ ስቴት
ADMIN_REASON = 100 

# ───────────── HELPERS ─────────────

def get_txt(lang, key, **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS["ti"]).get(key, key)
    return text.format(**kwargs)

async def edit_any(query, text, keyboard):
    msg = query.message
    if msg.photo:
        await query.edit_message_caption(
            caption=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    else:
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

# ───────────── START ─────────────

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"),
         InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"),
         InlineKeyboardButton("🇪🇹 Oromoo", callback_data="l_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="l_saho")]
    ]

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.delete()

    if POSTER:
        await context.bot.send_photo(
            update.effective_chat.id,
            POSTER,
            caption="Please select your language",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    else:
        await context.bot.send_message(
            update.effective_chat.id,
            "Please select your language",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    return SELECT_LANG

# ───────────── LANGUAGE ─────────────

async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = q.data.split("_")[1]
    context.user_data["lang"] = lang

    kb = [[InlineKeyboardButton(get_txt(lang, "btn_continue"), callback_data="go_menu")]]

    await edit_any(
        q,
        get_txt(lang, "welcome_text", user_name=update.effective_user.first_name),
        InlineKeyboardMarkup(kb)
    )

    return GREETING

# ───────────── MENU ─────────────

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = context.user_data["lang"]

    kb = [
        [InlineKeyboardButton(get_txt(lang, "vol4"), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_txt(lang, "vol3"), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_txt(lang, "vol2"), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_txt(lang, "vol1"), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_txt(lang, "btn_guide"), callback_data="guide")],
        [InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="restart")]
    ]

    await edit_any(
        q,
        get_txt(lang, "main_menu_prompt"),
        InlineKeyboardMarkup(kb)
    )

    return MENU

# ───────────── HOW TO BUY (FIXED) ─────────────

async def guide_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = context.user_data["lang"]

    kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]

    await edit_any(
        q,
        get_txt(lang, "full_guide"),
        InlineKeyboardMarkup(kb)
    )

    return MENU

# ───────────── LOCATION ─────────────

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    lang = context.user_data["lang"]

    if q.data.startswith("buy_"):
        context.user_data["album"] = q.data.replace("buy_", "")

    kb = [
        [InlineKeyboardButton(get_txt(lang, "loc_eth"), callback_data="loc_ok")],
        [InlineKeyboardButton(get_txt(lang, "loc_intl"), callback_data="loc_no")],
        [InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]
    ]

    await edit_any(
        q,
        get_txt(lang, "ask_loc_text"),
        InlineKeyboardMarkup(kb)
    )

    return LOCATION

# ───────────── PAYMENT ─────────────

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

    await edit_any(
        q,
        get_txt(lang, "payment_instructions",
                album_title=album.upper(), price=price),
        InlineKeyboardMarkup(kb)
    )

    return PAYMENT

# ───────────── PROOF (UPDATED) ─────────────

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "ti")
    album = context.user_data.get("album", "unknown")
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    # ናብ ኣድሚን መልእኽቲ ምስ Approve/Reject መጠወቒታት ምስዳድ
    admin_kb = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"adm_approve_{user_id}_{album}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"adm_reject_{user_id}_{album}")
        ]
    ]
    
    admin_msg = f"🔔 **ሓድሽ ክፍሊት ተላኢኹ**\n\n👤 ተጠቃሚ: {user_name} (ID: {user_id})\n💿 ኣልበም: {album.upper()}"
    
    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=admin_msg,
            reply_markup=InlineKeyboardMarkup(admin_kb),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"{admin_msg}\n\n📄 ጽሑፍ: {update.message.text}",
            reply_markup=InlineKeyboardMarkup(admin_kb),
            parse_mode=ParseMode.MARKDOWN
        )

    await update.message.reply_text(
        get_txt(lang, "proof_received_msg"),
        parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END

# ───────────── ADMIN ACTIONS (NEW) ─────────────

async def admin_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split("_")
    action = data[1] # approve or reject
    target_user_id = data[2]
    album = data[3]
    
    context.bot_data[f"admin_action_{ADMIN_ID}"] = {
        "action": action,
        "user_id": target_user_id,
        "album": album
    }
    
    await query.message.reply_text(
        f"በጃኹም ነቲ {action} ዝገበርኩሉ **ምኽንያት** ጽሓፉ (ንተጠቃሚ ዝለኣኽ መልእኽቲ):",
        parse_mode=ParseMode.MARKDOWN
    )
    return ADMIN_REASON

async def admin_reason_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_data = context.bot_data.get(f"admin_action_{ADMIN_ID}")
    if not admin_data:
        return ConversationHandler.END
    
    reason = update.message.text
    user_id = int(admin_data["user_id"])
    action = admin_data["action"]
    album = admin_data["album"]
    
    if action == "approve":
        msg = f"✅ **ክፍሊትኩም ተጸዲቑ ኣሎ!**\n\nምኽንያት: {reason}\n\nየቐንየልና!"
        # እንተድኣ Vol 4 ኮይኑ ድሕሪ 3 መዓልቲ ፊድባክ ክሓትት Job ንሰርዓሉ
        if album.lower() == "vol4":
            context.job_queue.run_once(
                send_feedback_request, 
                when=3 * 24 * 60 * 60, # 3 መዓልቲ (ብሰከንድ)
                chat_id=user_id,
                name=f"feedback_{user_id}"
            )
    else:
        msg = f"❌ **ክፍሊትኩም ኣይተጸደቐን**\n\nምኽንያት: {reason}\n\nበጃኹም ዳግም ፈትኑ ወይ ንኣድሚን ኣዘራርቡ።"

    try:
        await context.bot.send_message(chat_id=user_id, text=msg, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text("✅ መልእኽቲ ናብቲ ተጠቃሚ ብትኽክል ተላኢኹ ኣሎ።")
    except Exception as e:
        await update.message.reply_text(f"❌ መልእኽቲ ክለኣኽ ኣይከኣለን: {str(e)}")
    
    return ConversationHandler.END

# ───────────── FEEDBACK JOB (NEW) ─────────────

async def send_feedback_request(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    feedback_text = (
        "ሰላም፡ ቅድሚ 3 መዓልቲ ነቲ **Vol 4 'እየሱስ'** ዝብል ኣልበም ገዚእኩም ኔርኩም። "
        "ብዛዕባ እቲ ኣልበም ዘለኩም ሓሳብን ርኢቶን (Feedback) እንተሰዲድካልና ብጣዕሚ ንሕጎስ። የቐንየልና!"
    )
    await context.bot.send_message(chat_id=job.chat_id, text=feedback_text)

# ───────────── MAIN ─────────────

def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_cmd),
            CallbackQueryHandler(start_cmd, pattern="restart")
        ],
        states={
            SELECT_LANG: [CallbackQueryHandler(welcome_handler, "^l_")],
            GREETING: [CallbackQueryHandler(menu_handler, "^go_menu$")],
            MENU: [
                CallbackQueryHandler(guide_handler, "^guide$"),
                CallbackQueryHandler(location_handler, "^buy_"),
                CallbackQueryHandler(menu_handler, "^go_menu$"),
                CallbackQueryHandler(start_cmd, "^restart$")
            ],
            LOCATION: [
                CallbackQueryHandler(payment_handler, "^loc_"),
                CallbackQueryHandler(menu_handler, "^go_menu$")
            ],
            PAYMENT: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, proof_handler),
                CallbackQueryHandler(menu_handler, "^go_menu$")
            ],
            # ንኣድሚን ጥራይ ዝሰርሕ state
            ADMIN_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_reason_handler)]
        },
        fallbacks=[CommandHandler("start", start_cmd)]
    )

    # ኣድሚን Approve/Reject ምስ ጠወቐ ዝሰርሕ Handler
    app.add_handler(CallbackQueryHandler(admin_button_click, pattern="^adm_"))
    app.add_handler(conv)
    
    app.run_polling()

if __name__ == "__main__":
    main()