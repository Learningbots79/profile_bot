# Credit: Project by LearningBot79
# GitHub: https://github.com/Learningbots79
# Telegram Channel: https://t.me/learningbots79

import os
import sys
import asyncio
from dotenv import load_dotenv
from LearningBots import plugins
from LearningBots.plugins.image import image_button
from LearningBots.plugins.referral import my_referral
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    filters, ContextTypes
)
from handlers import (
    start_command,
    start1_command,
    view_profile,
    update_profile,
    button_handler,
    handle_message,
    broadcast,
    search_user,
    all_users,
    short_command,
    handle_all_text_inputs
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
    app.add_handler(CommandHandler("edit", update_profile))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("all_users", all_users))
    app.add_handler(CommandHandler("search", search_user))
    app.add_handler(CommandHandler("short", short_command))
    app.add_handler(CommandHandler("image", image_button))
    app.add_handler(CommandHandler("my_referral", my_referral))

    # Button callback handlers (for buttons in /start)
    app.add_handler(CallbackQueryHandler(view_profile,  pattern="^view_profile$"))
    app.add_handler(CallbackQueryHandler(update_profile, pattern="^update_profile$"))
    app.add_handler(CallbackQueryHandler(short_command,  pattern="^short_command$"))
    app.add_handler(CallbackQueryHandler(start_command,   pattern="^start_command$"))
    app.add_handler(CallbackQueryHandler(start1_command, pattern="^start1_command$"))
    app.add_handler(CallbackQueryHandler(image_button, pattern="^image_button$"))
    app.add_handler(CallbackQueryHandler(my_referral, pattern="^my_referral$"))

    app.add_handler(CallbackQueryHandler(button_handler))


    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_text_inputs))


    print("✅ Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())


