import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode, ChatAction
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, ContextTypes, filters, PicklePersistence
)
from translations import TRANSLATIONS

# ፕሮፌሽናል Logging ንምክትታል
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_CHAT_ID"))
POSTER = os.getenv("ALBUM_ART_FILE_ID")

CHANNEL_IDS = {
    "vol1": -1003548469381,
    "vol2": -1003540162347,
    "vol3": -1003582450486,
    "vol4": -1003606695407
}

SELECT_LANG, GREETING, MENU, LOCATION, PAYMENT = range(5)

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
    # Professional Touch: Send 'Typing' action
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
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
            caption="<b>Welcome!</b>\nPlease select your language / በጃኹም ቋንቋ ምረጹ",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.HTML
        )
    else:
        await context.bot.send_message(
            update.effective_chat.id,
            "<b>Welcome!</b>\nPlease select your language / በጃኹም ቋንቋ ምረጹ",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.HTML
        )

    return SELECT_LANG

# ───────────── LANGUAGE ─────────────

async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = q.data.split("_")[1]
    context.user_data["lang"] = lang

    kb = [[InlineKeyboardButton(get_txt(lang, "btn_continue"), callback_data="go_menu")]]
    await edit_any(q, get_txt(lang, "welcome_text", user_name=update.effective_user.first_name), InlineKeyboardMarkup(kb))
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
    await edit_any(q, get_txt(lang, "main_menu_prompt"), InlineKeyboardMarkup(kb))
    return MENU

# ───────────── GUIDE ─────────────

async def guide_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = context.user_data["lang"]
    kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]
    await edit_any(q, get_txt(lang, "full_guide"), InlineKeyboardMarkup(kb))
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
    await edit_any(q, get_txt(lang, "ask_loc_text"), InlineKeyboardMarkup(kb))
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

    # Modern: Store the message ID to update it later
    context.user_data["payment_msg_id"] = q.message.message_id
    
    await edit_any(q, get_txt(lang, "payment_instructions", album_title=album.upper(), price=price), InlineKeyboardMarkup(kb))
    return PAYMENT

# ───────────── PROOF ─────────────

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "ti")
    album = context.user_data.get("album", "vol1")
    user_id = update.effective_user.id
    user_mention = update.effective_user.mention_html()

    # 1. Update the user's view (Modern: Clean the instructions)
    if "payment_msg_id" in context.user_data:
        try:
            await context.bot.edit_message_caption(
                chat_id=update.effective_chat.id,
                message_id=context.user_data["payment_msg_id"],
                caption=get_txt(lang, "proof_received_msg"),
                parse_mode=ParseMode.HTML
            )
        except:
            await update.message.reply_text(get_txt(lang, "proof_received_msg"), parse_mode=ParseMode.HTML)

    # 2. Notify Admin with more info
    admin_kb = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"adm_app_{user_id}_{album}_{lang}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"adm_rej_{user_id}_{lang}")
    ]]
    
    admin_msg = (
        f"<b>🚀 New Payment Received</b>\n\n"
        f"👤 <b>User:</b> {user_mention}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"💿 <b>Album:</b> {album.upper()}"
    )
    
    if update.message.photo:
        await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, caption=admin_msg, reply_markup=InlineKeyboardMarkup(admin_kb), parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(ADMIN_ID, f"{admin_msg}\n📄 <b>Text Proof:</b>\n{update.message.text}", reply_markup=InlineKeyboardMarkup(admin_kb), parse_mode=ParseMode.HTML)

    return ConversationHandler.END

# ───────────── ADMIN ACTIONS (PRO) ─────────────

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # Security: Only the real admin can trigger this
    if update.effective_user.id != ADMIN_ID:
        await query.answer("Access Denied.", show_alert=True)
        return

    await query.answer()
    parts = query.data.split("_")
    action, user_id, lang = parts[1], int(parts[2]), parts[-1]
    
    msgs = {
        "ti": {"ok": "እቲ ዝሰደድኩምዎ ስክሪን ሻት ኣረጋጊፅና ኣለና። ✅\nእነሆ ናይቲ ቻናል መላግቦ:", "no": "ክረጋገፅ ኣይከኣለን እሞ በጃኦም ደጊሞም ይፈትኑ። ❌"},
        "am": {"ok": "የላኩትን ደረሰኝ አረጋግጠናል። ✅\nየቻናሉ ሊንክ ይኸው፦", "no": "መረጋገጥ ስላልቻለ እባክዎ ደግመው ይሞክሩ። ❌"},
        "en": {"ok": "Your payment has been verified. ✅\nHere is your access link:", "no": "Verification failed. Please try again. ❌"},
        "om": {"ok": "Nagaheen keessan mirkanaa'eera. ✅\nLiinkii chaanaalii kunoo:", "no": "Mirkanaa'uu hin dandeenye, maaloo irra deebi'ii yaali. ❌"},
        "saho": {"ok": "ጋራይነህ ናነ! ✅\nቶይ ቻናልህ ድብዶ (Link) ታነ:", "no": "ክረጋገፅ ኣይከኣለን እሞ በጃኦም ደጊሞም ይፈትኑ። ❌"}
    }
    
    t_msg = msgs.get(lang, msgs["ti"])

    if action == "app":
        album = parts[3]
        channel_id = CHANNEL_IDS.get(album)
        try:
            # Generate One-time link
            link = await context.bot.create_chat_invite_link(chat_id=channel_id, member_limit=1)
            await context.bot.send_message(chat_id=user_id, text=f"<b>{t_msg['ok']}</b>\n\n{link.invite_link}", parse_mode=ParseMode.HTML)
            await query.edit_message_caption(caption=query.message.caption + f"\n\n✅ <b>APPROVED & LINK SENT</b>", parse_mode=ParseMode.HTML)
            
            # Vol 4 Feedback Job
            if album == "vol4":
                context.job_queue.run_once(send_feedback_task, when=3*24*60*60, chat_id=user_id, data=lang)
        except Exception as e:
            await query.message.reply_text(f"❌ Error creating link: {str(e)}")
            
    elif action == "rej":
        await context.bot.send_message(chat_id=user_id, text=f"<b>{t_msg['no']}</b>", parse_mode=ParseMode.HTML)
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ <b>REJECTED</b>", parse_mode=ParseMode.HTML)

async def send_feedback_task(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    # Professional Feedback Message
    msg = "ሰላም፡ ቅድሚ 3 መዓልቲ ነቲ <b>Vol 4 'እየሱስ'</b> ዝብል ኣልበም ገዚእኩም ኔርኩም። ብዛዕባ እቲ ኣልበም ዘለኩም ሓሳብን ርኢታን ንኽሰዱልና ብትሕትና ንሓትት። @MezemranLdetaMaryamMekelle"
    await context.bot.send_message(chat_id=job.chat_id, text=msg, parse_mode=ParseMode.HTML)

# ───────────── MAIN ─────────────

def main():
    # Persistence: Saves conversation state even if server restarts
    persistence = PicklePersistence(filepath="bot_persistence_data")

    app = Application.builder().token(TOKEN).persistence(persistence).build()

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
                MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), proof_handler),
                CallbackQueryHandler(menu_handler, "^go_menu$")
            ]
        },
        fallbacks=[CommandHandler("start", start_cmd)],
        name="main_conversation",
        persistent=True
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^adm_"))
    
    # Professional: Clear way to start
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()