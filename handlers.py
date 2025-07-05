# Credit: Project by LearningBot79
# GitHub: https://github.com/Learningbots79
# Telegram Channel: https://t.me/learningbots79

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import is_admin, admin_only
from database import save_data, load_data, delete_data, load_all_users

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = "name"
    await update.message.reply_text("👋 Hey! What's your name?")

# /view command
async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data(update.effective_user.id)
    if data:
        await update.message.reply_text(
            f"🧾 Your Profile:\n"
            f"Name: {data.get('name')}\n"
            f"Age: {data.get('age')}\n"
            f"Phone: {data.get('phone')}"
        )
    else:
        await update.message.reply_text("🚫 No profile found. Use /start to create one.")

# /edit command
async def edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data(update.effective_user.id)
    if data:
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Edit Name", callback_data="edit_name"),
                InlineKeyboardButton("Edit Age", callback_data="edit_age")
            ],
            [InlineKeyboardButton("Edit Phone", callback_data="edit_phone")]
        ])
        await update.message.reply_text("✏️ Choose what you want to edit:", reply_markup=kb)
    else:
        await update.message.reply_text("🚫 No data to edit. Use /start first.")

# Handle button callbacks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data.startswith("edit_"):
        field = query.data.split("_")[1]
        context.user_data["step"] = f"edit_{field}"
        await query.message.reply_text(f"✏️ Send new {field}:")
        await query.delete_message()

    elif query.data == "confirm":
        if all(k in context.user_data for k in ("name", "age", "phone")):
            save_data(uid, {
                "name": context.user_data["name"],
                "age": context.user_data["age"],
                "phone": context.user_data["phone"]
            })
            await query.edit_message_text("✅ Your data has been saved.")
        else:
            await query.edit_message_text("⚠️ Data missing! Please restart with /start")
        context.user_data.clear()

    elif query.data == "cancel":
        await query.edit_message_text("❌ Cancelled.")
        context.user_data.clear()

# Handle user input
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step")

    if step == "name":
        context.user_data["name"] = update.message.text
        context.user_data["step"] = "age"
        await update.message.reply_text("📅 Great! Now enter your age:")

    elif step == "age":
        context.user_data["age"] = update.message.text
        context.user_data["step"] = "phone"
        await update.message.reply_text("📱 Now enter your phone number:")

    elif step == "phone":
        context.user_data["phone"] = update.message.text
        context.user_data["step"] = "confirm"
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel")
            ]
        ])
        await update.message.reply_text(
            f"✨ Please confirm your data:\n"
            f"Name: {context.user_data['name']}\n"
            f"Age: {context.user_data['age']}\n"
            f"Phone: {context.user_data['phone']}",
            reply_markup=kb
        )

    elif step and step.startswith("edit_"):
        field = step.replace("edit_", "")
        new_value = update.message.text
        data = load_data(update.effective_user.id)
        if data:
            data[field] = new_value
            save_data(update.effective_user.id, data)
            await update.message.reply_text(f"✅ {field.capitalize()} updated!")
        else:
            await update.message.reply_text("⚠️ No data found.")
        context.user_data.clear()

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("Acces Denied")

        users = load_all_users()
        if not users:
            return await update.message.reply_text("NO user found")

        text = "ALL Users :\n"
        for uid, data in users.items():
            text += f"- {data.get('name', 'No Name')} (ID: {uid})\n"

            await update.message.reply_text(text)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("Access Denied ❌")

    if not context.args:
        return await update.message.reply_text("Usage: /broadcast <your message>")

    message = " ".join(context.args)
    users = load_all_users()

    count = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=message)
            count += 1
        except:
            continue

    await update.message.reply_text(f"✅ Message sent to {count} users.")


# ADNIN ONLY

@admin_only
async def all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_all_users()
    if not data:
        await update.message.reply_text("No users found.")
        return

    msg = "All user:\n\n"
    for uid, info in data.items():
        msg += f"ID: {id}\n"
        msg += f"Name: {info.get('name')}\n"
        msg += f"Age: {info.get('age')}\n"
        msg += f"Phone: {info.get('phone')}\n"
    await update.message.reply_text(msg)

# Credit: Project by LearningBot79
# GitHub: https://github.com/Learningbots79
# Telegram Channel: https://t.me/learningbots79