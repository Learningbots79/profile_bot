from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import save_data, load_data, delete_data

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "confirm":
        if all(k in context.user_data for k in ("name", "age", "phone")):
            save_data(user_id, {
                "name": context.user_data["name"],
                "age": context.user_data["age"],
                "phone": context.user_data["phone"]
            })
            await query.edit_message_text("✅ Your data has been saved!")
        else:
            await query.edit_message_text("⚠️ Something is missing. Please send /start again.")
        context.user_data.clear()

    elif data == "cancel":
        await query.edit_message_text("❌ Cancelled.")
        context.user_data.clear()

    elif data.startswith("edit_"):
        field = data.split("_")[1]
        context.user_data["step"] = f"edit_{field}"
        await query.message.reply_text(f"✏️ Send new {field}")
        await query.delete_message()

    elif data == "delete_confirm":
        delete_data(user_id)
        await query.edit_message_text("🗑️ Your data has been deleted.")

    elif data == "delete_cancel":
        await query.edit_message_text("❌ Deletion cancelled.")
