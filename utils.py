import os
from functools import wraps  # ✅
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv

load_dotenv()
ADMIN_IDS = os.getenv("ADMINS", "").split(",")

def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMIN_IDS

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not is_admin(update.effective_user.id):
            return await update.message.reply_text("🚫 Access Denied")
        return await func(update, context, *args, **kwargs)
    return wrapper

def get_arg(context):
    return " ".join(context.args) if context.args else None

def format_user(uid, data):
    return(
        f"Id: {id}\n"
        f"Name : {data.get('name', 'N/A')}\n"
        f"Age : {data.get('age', 'N/A')}\n"
        f"Phone : {data.get('phone', 'N/A')}"
    )