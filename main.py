# main.py
import logging, requests, asyncio, os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler
)

# Get token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

SESSION, CSRF, REPORT_REASON, SLEEP_TIME = range(4)
user_data = {}
report_tasks = {}

logging.basicConfig(level=logging.INFO)

reason_labels = {
    "📛 Spam": "1",
    "🙍‍♂️ Self Injury": "2",
    "💊 Drugs": "3",
    "🩱 Nudity": "4",
    "🔪 Violence": "5",
    "🧨 Hate Speech": "6",
    "😡 Harassment": "7",
    "🎭 Impersonation (Insta)": "8",
    "🏢 Impersonation (Business)": "9",
    "🚘 Impersonation (Other)": "10",
    "🔞 Underage (<13)": "11",
    "🔫 Gun Sales": "12",
    "🧨 Violence (Type 1)": "13",
    "💣 Violence (Type 4)": "14"
}

# 🧠 All your async bot functions remain unchanged...
# (I'll skip pasting them here to keep the message short – same as your original code)

# --- Copy all functions from your original file below here ---

# Main function (updated)
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    login_conv = ConversationHandler(
        entry_points=[CommandHandler("login", login)],
        states={
            SESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_session)],
            CSRF: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_csrf)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    report_conv = ConversationHandler(
        entry_points=[CommandHandler("report", report)],
        states={
            REPORT_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_reason)],
            SLEEP_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_sleep_time)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(login_conv)
    app.add_handler(report_conv)
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("cancel", cancel))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
