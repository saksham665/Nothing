import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# === BOT TOKEN ===
BOT_TOKEN = "84960353ku6FkOcs5eRwvvX7BvTdo3H6ahLI"

# === INTERNAL APIs ===
TRUECALL1"
FULLDET"

BOT_SIGNATURE = "\n\nBot by : Saksham 😎"


# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "**Welcome to TrueInfo Bot 🔍**\n\n"
        "Send me any 10-digit Indian mobile number (with or without +91)\n"
        "Example: `7007544138`" + BOT_SIGNATURE,
        parse_mode=ParseMode.MARKDOWN,
    )


# === Handle Number Search ===
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = update.message.text.strip()

    if num.startswith("+91"):
        num = num.replace("+91", "")
    num = "".join(filter(str.isdigit, num))

    if len(num) != 10:
        await update.message.reply_text("❌ Please send a valid 10-digit Indian number." + BOT_SIGNATURE)
        return

    await update.message.chat.send_action(action=ChatAction.TYPING)

    try:
        res = requests.get(TRUECALLER_API + num, timeout=10)
        data = res.json()
    except Exception:
        await update.message.reply_text("⚠️ Error fetching data from source." + BOT_SIGNATURE)
        return

    name = data.get("name", "Unknown")
    carrier = data.get("carrier", "Unknown")
    location = data.get("location", "Unknown")

    msg = (
        f"**Number:** +91{num}\n"
        f"**Country:** India 🇮🇳\n"
        f"**🔍 TrueCaller Says:**\n"
        f"**Name:** {name}\n"
        f"**Carrier:** {carrier}\n"
        f"**Location:** {location}\n\n"
        f"**🔍 Unknown Says:**\n"
        f"**Name:** {name}\n"
        f"[WhatsApp](https://wa.me/+91{num}) | [Telegram](https://t.me/+91{num})"
        + BOT_SIGNATURE
    )

    keyboard = [[InlineKeyboardButton("📜 Full Details", callback_data=f"full_{num}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


# === Handle "Full Details" Button ===
async def full_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    num = query.data.replace("full_", "")

    await query.message.chat.send_action(action=ChatAction.TYPING)

    try:
        res = requests.get(FULLDETAILS_API + num, timeout=10)
        data = res.json()
        pretty_json = json.dumps(data, indent=2, ensure_ascii=False)

        await query.message.reply_text(
            f"```json\n{pretty_json}\n```" + BOT_SIGNATURE,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception:
        await query.message.reply_text("⚠️ Error fetching full details." + BOT_SIGNATURE)


# === Main Function ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    app.add_handler(CallbackQueryHandler(full_details))
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
