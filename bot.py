import os
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

    # 🔥 CRITICAL: STAY IN MENU
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

# ───────────── PROOF ─────────────

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    await update.message.reply_text(
        get_txt(lang, "proof_received_msg"),
        parse_mode=ParseMode.HTML
    )

    return ConversationHandler.END

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
            ]
        },
        fallbacks=[CommandHandler("start", start_cmd)]
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
