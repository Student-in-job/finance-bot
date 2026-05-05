from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from database import init_db
from handlers import handle_message, auth_command, report_command, list_cats_command, new_cat_command, delete_cat_command
import os
import time
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    print("Connecting to Database...")
    init_db()
    print("Database connected and initialized.")
    
    print("Initializing Telegram Bot...")
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("auth", auth_command))
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(CommandHandler("list_cats", list_cats_command))
    app.add_handler(CommandHandler("new_cat", new_cat_command))
    app.add_handler(CommandHandler("delete_cat", delete_cat_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Telegram Bot initialized.")
    
    print("Bot is starting...")
    time.sleep(1)
    app.run_polling(poll_interval=1.0)
