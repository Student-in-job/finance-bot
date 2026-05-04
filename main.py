from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from database import init_db
from handlers import handle_message, auth_command, report_command
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("auth", auth_command))
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is starting...")
    app.run_polling()
