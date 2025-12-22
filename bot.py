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

CHANNELS = {
    'vol4': os.getenv("CHANNEL_ID_VOL_4"),
    'vol3': os.getenv("CHANNEL_ID_VOL_3"),
    'vol2': os.getenv("CHANNEL_ID_VOL_2"),
    'vol1': os.getenv("CHANNEL_ID_VOL_1"),
}

SELECT_LANG, GREETING, MENU, LOCATION, PAYMENT = range(5)

def get_txt(lang, key, **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS['ti']).get(key, key)
    return text.format(**kwargs)

# ───────────────────────── START ─────────────────────────

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    kb = [
        [InlineKeyboardButton("🇪🇹 ትግርኛ", callback_data="l_ti"),
         InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="l_am")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="l_en"),
         InlineKeyboardButton("🇪🇹 Oromoo", callback_data="l_om")],
        [InlineKeyboardButton("🇪🇷/🇪🇹 ሳሆ", callback_data="l_saho")]
    ]

    caption = "Please select your language"

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.delete()

    if POSTER:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=POSTER,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(kb)
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=caption,
            reply_markup=InlineKeyboardMarkup(kb)
        )

    return SELECT_LANG

# ───────────────────────── LANGUAGE ─────────────────────────

async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang

    kb = [[InlineKeyboardButton(get_txt(lang, "btn_continue"), callback_data="go_menu")]]
    text = get_txt(lang, "welcome_text", user_name=update.effective_user.first_name)

    await query.edit_message_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode=ParseMode.HTML
    )

    return GREETING

# ───────────────────────── MENU ─────────────────────────

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data["lang"]

    kb = [
        [InlineKeyboardButton(get_txt(lang, "vol4"), callback_data="buy_vol4")],
        [InlineKeyboardButton(get_txt(lang, "vol3"), callback_data="buy_vol3")],
        [InlineKeyboardButton(get_txt(lang, "vol2"), callback_data="buy_vol2")],
        [InlineKeyboardButton(get_txt(lang, "vol1"), callback_data="buy_vol1")],
        [InlineKeyboardButton(get_txt(lang, "btn_guide"), callback_data="guide")],
        [InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="restart")]
    ]

    await query.edit_message_caption(
        caption=get_txt(lang, "main_menu_prompt"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode=ParseMode.HTML
    )

    return MENU

# ───────────────────────── LOCATION ─────────────────────────

async def location_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data["lang"]

    if query.data.startswith("buy_"):
        context.user_data["album"] = query.data.replace("buy_", "")

    kb = [
        [InlineKeyboardButton(get_txt(lang, "loc_eth"), callback_data="loc_ok")],
        [InlineKeyboardButton(get_txt(lang, "loc_intl"), callback_data="loc_no")],
        [InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]
    ]

    await query.edit_message_caption(
        caption=get_txt(lang, "ask_loc_text"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode=ParseMode.HTML
    )

    return LOCATION

# ───────────────────────── PAYMENT ─────────────────────────

async def payment_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data["lang"]

    if query.data == "loc_no":
        kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]
        await query.edit_message_caption(
            caption=get_txt(lang, "loc_out_unavailable"),
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.HTML
        )
        return LOCATION

    album = context.user_data["album"]
    price = "300" if album == "vol4" else "100"

    kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]

    await query.edit_message_caption(
        caption=get_txt(lang, "payment_instructions",
                        album_title=album.upper(), price=price),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode=ParseMode.HTML
    )

    return PAYMENT

# ───────────────────────── GUIDE ─────────────────────────

async def guide_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data["lang"]
    kb = [[InlineKeyboardButton(get_txt(lang, "btn_back"), callback_data="go_menu")]]

    await query.edit_message_caption(
        caption=get_txt(lang, "full_guide"),
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode=ParseMode.HTML
    )

    return MENU

# ───────────────────────── PROOF ─────────────────────────

async def proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    album = context.user_data["album"]
    user = update.effective_user

    await update.message.reply_text(
        get_txt(lang, "proof_received_msg"),
        parse_mode=ParseMode.HTML
    )

    await context.bot.send_message(
        ADMIN_ID,
        f"🆕 Payment proof\nUser: {user.mention_html()}\nAlbum: {album}",
        parse_mode=ParseMode.HTML
    )

    if update.message.photo:
        await update.message.forward(ADMIN_ID)

    return ConversationHandler.END

# ───────────────────────── MAIN ─────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_cmd),
            CallbackQueryHandler(start_cmd, pattern="restart")
        ],
        states={
            SELECT_LANG: [CallbackQueryHandler(welcome_handler, pattern="^l_")],
            GREETING: [CallbackQueryHandler(main_menu, pattern="go_menu")],
            MENU: [
                CallbackQueryHandler(location_select, pattern="^buy_"),
                CallbackQueryHandler(guide_screen, pattern="guide"),
                CallbackQueryHandler(start_cmd, pattern="restart")
            ],
            LOCATION: [
                CallbackQueryHandler(payment_screen, pattern="^loc_"),
                CallbackQueryHandler(main_menu, pattern="go_menu")
            ],
            PAYMENT: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, proof_handler),
                CallbackQueryHandler(main_menu, pattern="go_menu")
            ]
        },
        fallbacks=[CommandHandler("start", start_cmd)]
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
