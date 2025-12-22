import os
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, ContextTypes, filters
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_CHAT_ID"))
ALBUM_LINK = "https://your-download-link-here"

SELECT_LANG, GREETING, MENU, LOCATION, PAYMENT = range(5)

TRANSLATIONS = {
    "en": {
        "welcome_text": "Welcome {user_name}",
        "btn_continue": "Continue",
        "main_menu_prompt": "Select Album",
        "btn_guide": "How to Buy",
        "btn_back": "⬅ Back",
        "vol4": "Album Vol 4",
        "vol3": "Album Vol 3",
        "vol2": "Album Vol 2",
        "vol1": "Album Vol 1",
        "full_guide": "1. Select Album\n2. Pay\n3. Send Screenshot\n4. Get Link",
        "ask_loc_text": "Where are you?",
        "loc_eth": "Ethiopia",
        "loc_intl": "Outside Ethiopia",
        "payment_instructions": "Send payment screenshot for <b>{album}</b>",
        "proof_received_msg": "Screenshot received. Waiting for approval.",
        "approved_msg": "✅ Approved!\nHere is your link:\n{link}",
        "rejected_msg": "❌ Payment rejected. Please try again."
    }
}

def T(lang, key, **k):
    return TRANSLATIONS[lang][key].format(**k)

async def edit_any(q, text, kb):
    m = q.message
    if m.photo:
        await q.edit_message_caption(text, reply_markup=kb, parse_mode=ParseMode.HTML)
    else:
        await q.edit_message_text(text, reply_markup=kb, parse_mode=ParseMode.HTML)

# ───────── START ─────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    kb = [[InlineKeyboardButton("English", callback_data="l_en")]]
    await update.message.reply_text("Select Language", reply_markup=InlineKeyboardMarkup(kb))
    return SELECT_LANG

# ───────── LANGUAGE ─────────

async def lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data["lang"] = "en"
    kb = [[InlineKeyboardButton(T("en","btn_continue"), callback_data="go_menu")]]
    await edit_any(q, T("en","welcome_text", user_name=q.from_user.first_name), InlineKeyboardMarkup(kb))
    return GREETING

# ───────── MENU ─────────

async def menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = ctx.user_data["lang"]
    kb = [
        [InlineKeyboardButton(T(lang,"vol4"), callback_data="buy_vol4")],
        [InlineKeyboardButton(T(lang,"btn_guide"), callback_data="guide")]
    ]
    await edit_any(q, T(lang,"main_menu_prompt"), InlineKeyboardMarkup(kb))
    return MENU

# ───────── GUIDE ─────────

async def guide(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = ctx.user_data["lang"]
    kb = [[InlineKeyboardButton(T(lang,"btn_back"), callback_data="go_menu")]]
    await edit_any(q, T(lang,"full_guide"), InlineKeyboardMarkup(kb))
    return MENU

# ───────── LOCATION ─────────

async def location(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data["album"] = "VOL 4"
    kb = [
        [InlineKeyboardButton("Ethiopia", callback_data="loc_ok")],
        [InlineKeyboardButton("⬅ Back", callback_data="go_menu")]
    ]
    await edit_any(q, "Confirm location", InlineKeyboardMarkup(kb))
    return LOCATION

# ───────── PAYMENT ─────────

async def payment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    kb = [[InlineKeyboardButton("⬅ Back", callback_data="go_menu")]]
    await edit_any(q, "Send screenshot", InlineKeyboardMarkup(kb))
    return PAYMENT

# ───────── SCREENSHOT HANDLER (FIXED) ─────────

async def screenshot(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data["lang"]
    user = update.effective_user

    file_id = update.message.photo[-1].file_id

    kb = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]

    await ctx.bot.send_photo(
        ADMIN_ID,
        file_id,
        caption=f"Payment from @{user.username or user.first_name}\nID: {user.id}",
        reply_markup=InlineKeyboardMarkup(kb)
    )

    await update.message.reply_text(T(lang,"proof_received_msg"))
    return PAYMENT

# ───────── ADMIN ACTION ─────────

async def admin_action(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    action, user_id = q.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        await ctx.bot.send_message(
            user_id,
            T("en","approved_msg", link=ALBUM_LINK),
            parse_mode=ParseMode.HTML
        )
        await q.edit_message_caption("✅ Approved")
    else:
        await ctx.bot.send_message(user_id, T("en","rejected_msg"))
        await q.edit_message_caption("❌ Rejected")

# ───────── MAIN ─────────

def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_LANG: [CallbackQueryHandler(lang)],
            GREETING: [CallbackQueryHandler(menu, "^go_menu$")],
            MENU: [
                CallbackQueryHandler(guide, "^guide$"),
                CallbackQueryHandler(location, "^buy_"),
                CallbackQueryHandler(menu, "^go_menu$")
            ],
            LOCATION: [CallbackQueryHandler(payment, "^loc_")],
            PAYMENT: [
                MessageHandler(filters.PHOTO, screenshot),
                CallbackQueryHandler(menu, "^go_menu$")
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_action, "^(approve|reject)_"))

    app.run_polling()

if __name__ == "__main__":
    main()
