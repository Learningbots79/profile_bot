# Credit: Project by LearningBot79
# GitHub: https://github.com/Learningbots79
# Telegram Channel: https://t.me/learningbots79

import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    filters, ContextTypes
)
from handlers import (
    start_command,
    view_profile,
    edit_profile,
    button_handler,
    handle_message,
    list_users,
    broadcast,
    search_user,
    all_users
)

# Load BOT_TOKEN from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing in .env file")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("view", view_profile))
    app.add_handler(CommandHandler("edit", edit_profile))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("all_users", all_users))
    app.add_handler(CommandHandler("search", search_user))

    # Button callback handler
    app.add_handler(CallbackQueryHandler(button_handler))

    # Message handler for text inputs (name, age, etc.)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())


