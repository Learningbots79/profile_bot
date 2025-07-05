import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_IDS = os.getenv("ADMINS", "").split(",")


# to check admin or not but we have to define there also somthing
def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMIN_IDS

# upgraded version of admin check
def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not is_admin(update.effective_user.id):
            return await update.message.reply_text("Access Denied")
        return await func(update, context, *args, **kwargs)
    return wrapper