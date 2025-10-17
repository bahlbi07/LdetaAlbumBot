import logging
import os
import uuid
import requests
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)

# .env ፋይል ንኽንበብ ምግባር
load_dotenv()

# --- ቅጥዕታት (Configurations) ---
# ሚስጢራዊ ሓበሬታ ካብ .env ፋይል ምንባብ
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
PRIVATE_CHANNEL_ID = os.getenv("PRIVATE_CHANNEL_ID")
ALBUM_PRICE = os.getenv("ALBUM_PRICE", "100") # Default to 100 if not set

# --- ናይ Conversation Handler ደረጃታት ---
CHOOSE_LOCATION, CHOOSE_ACTION = range(2)

# --- ሓገዝቲ Functions ---
async def generate_chapa_link(user: dict, price: str, currency: str = "ETB") -> str:
    """ሓደ ናይ ክፍያ መላግቦ ካብ Chapa ዝፈጥር function"""
    tx_ref = f"ldeta-album-{user['id']}-{uuid.uuid4()}"
    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": price,
        "currency": currency,
        "email": f"{user['id']}@telegram.user",
        "first_name": user.get('first_name', 'User'),
        "last_name": user.get('last_name', 'Bot'),
        "tx_ref": tx_ref,
        "callback_url": "https://webhook.site/", # ንመፈተኒ ጥራይ (ክንቅይሮ ኢና)
        "return_url": "https://t.me/your_bot_username", # ተጠቃሚ ምስ ከፈለ ናበይ ከም ዝምለስ
        "customization[title]": "Ldeta Mariam Vol. 4 Album",
        "customization[description]": "Payment for the new album"
    }
    
    try:
        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data["data"]["checkout_url"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Chapa API error: {e}")
    return None

# --- ናይ ቦት ትእዛዛት (Bot Handlers) ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ቦት ምስ ተጀመረ ዝሰርሕ"""
    keyboard = [
        ["🇪🇹 ኣብ ውሽጢ ኢትዮጵያ"],
        ["🌍 ካብ ኢትዮጵያ ወጻኢ"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        f"ሰላም {update.effective_user.first_name}! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ኣበይ ከም ዘለኻ ምረጽ፦",
        reply_markup=reply_markup
    )
    return CHOOSE_LOCATION

async def handle_location_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ተጠቃሚ ቦታኡ ምስ መረጸ ዝሰርሕ"""
    choice = update.message.text
    
    if choice == "🇪🇹 ኣብ ውሽጢ ኢትዮጵያ":
        keyboard = [["✅ ኣልበም ግዛእ"], ["🔙 ናብ መጀመርታ ተመለስ"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            f"ጽቡቕ ምርጫ! ዋጋ ናይ'ዚ ራብዓይ ኣልበም {ALBUM_PRICE} ብር እዩ።\n\nክፍሊት ንምፍጻም 'ኣልበም ግዛእ' ዝብል ጠውቕ።",
            reply_markup=reply_markup
        )
        return CHOOSE_ACTION
        
    elif choice == "🌍 ካብ ኢትዮጵያ ወጻኢ":
        await update.message.reply_text(
            "እዚ ናይ ወጻኢ ክፍያ ኣገልግሎት ኣብዚ እዋን'ዚ ኣይጀመረን። ኣብ ቀረባ እዋን ክንጅምር ኢና።",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    return ConversationHandler.END


async def handle_buy_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """'ኣልበም ግዛእ' ዝብል ምስ ተጠወቐ ዝሰርሕ"""
    choice = update.message.text
    user = update.effective_user

    if choice == "✅ ኣልበም ግዛእ":
        await update.message.reply_text(
            "የመስግነልና! ናይ ክፍያ መላግቦ እናዳለና ስለ ዝኾና በጃኻ ጽንሕ በል።",
            reply_markup=ReplyKeyboardRemove()
        )
        payment_link = await generate_chapa_link(user.to_dict(), ALBUM_PRICE)
        
        if payment_link:
            await update.message.reply_text(
                f"ክፍሊት ንምፍጻም ነዚ ዝስዕብ መላግቦ ተጠቐም:\n\n{payment_link}\n\n"
                "ክፍሊትካ ምስ ኣረጋገጽና፡ ናብቲ መዝሙራት ዘለዎ ቻነል መእተዊ ክንሰደልካ ኢና።"
            )
        else:
            await update.message.reply_text("ይቕሬታ! ኣብዚ እዋን'ዚ ናይ ክፍያ መላግቦ ክፍጠር ኣይተኻእለን። በጃኻ ደሓር ዳግማይ ፈትን።")
        
        return ConversationHandler.END
    
    elif choice == "🔙 ናብ መጀመርታ ተመለስ":
        await start_command(update, context)
        return ConversationHandler.END
        
    return ConversationHandler.END


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ዝኾነ መስርሕ ንምቁራጽ"""
    await update.message.reply_text(
        "መስርሕ ተቋሪጹ ኣሎ። ዳግማይ ንምጅማር /start በል።",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# --- ቀንዲ Function ---
def main() -> None:
    if not all([TELEGRAM_TOKEN, CHAPA_SECRET_KEY, PRIVATE_CHANNEL_ID]):
        print("!!! ጌጋ: ሓደ ካብቶም ሚስጢራዊ ሓበሬታታት (Tokens/Keys) ኣብ .env ፋይል የለን።")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # ንኹሉ መስርሕ ዝቆጻጸር ConversationHandler ምዝገባ
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSE_LOCATION: [MessageHandler(filters.Regex("^(🇪🇹 ኣብ ውሽጢ ኢትዮጵያ|🌍 ካብ ኢትዮጵያ ወጻኢ)$"), handle_location_choice)],
            CHOOSE_ACTION: [MessageHandler(filters.Regex("^(✅ ኣልበም ግዛእ|🔙 ናብ መጀመርታ ተመለስ)$"), handle_buy_choice)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    application.add_handler(conv_handler)

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()