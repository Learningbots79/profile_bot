# Credit: Project by LearningBot79
# GitHub: https://github.com/Learningbots79
# Telegram Channel: https://t.me/learningbots79

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import is_admin, admin_only, get_arg
from shortener import shortern_url
from database import save_data, load_data, delete_data, load_all_users

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://files.catbox.moe/zdo9v5.jpg"
    caption = (

        "👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀ ʙᴏᴛ ᴛʜᴀᴛ’ꜱ sᴛɪʟʟ ʙᴇɪɴɢ ʙᴜɪʟᴛ...\n\n"
        "※ ᴄᴜʀʀᴇɴᴛ ꜰᴇᴀᴛᴜʀᴇꜱ:\n"
        "• sᴀᴠᴇ ʏᴏᴜʀ ᴘʀᴏꜰɪʟᴇ (ɴᴀᴍᴇ, ᴀɢᴇ, ᴘʜᴏɴᴇ)\n"
        "• ᴇᴅɪᴛ ʏᴏᴜʀ ɪɴꜰᴏ ᴀɴʏᴛɪᴍᴇ\n"
        "• ꜱʜᴏʀᴛᴇɴ ʟɪɴᴋꜱ ᴇᴀꜱɪʟʏ\n\n"
        "ᴍᴏʀᴇ ꜰᴇᴀᴛᴜʀᴇꜱ ᴄᴏᴍɪɴɢ...\n"
        "ꜱɪʟᴇɴᴛʟʏ. ᴅᴀɪʟʏ.\n\n"
        "ᴍᴀᴅᴇ ᴡɪᴛʜ 💌\n"
        "ᴄʀᴇᴅɪᴛ ɢᴏᴇꜱ ᴛᴏ ʏᴀꜱʜ."
    )
    kb = [
        [
            InlineKeyboardButton("Add details 📄", callback_data="start1_command"),
            InlineKeyboardButton("Update details", callback_data="update_profile")
        ],
        [
            InlineKeyboardButton("View Profile", callback_data="view_profile"),
            InlineKeyboardButton("Link Shorten", callback_data="short_command")
        ]
    ]
    await update.message.reply_photo(
        photo=url,
        caption=caption,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(kb)
    )



# start saving details
async def start1_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    context.user_data.clear()
    context.user_data["step"] = "name"
    await message.reply_text("👋 Hey! What's your name?")

# /view command
async def view_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    message = update.message or update.callback_query.message

    if query:
        await query.answer(cache_time=0)


    data = load_data(update.effective_user.id)
    if data:
        await message.reply_text(
            f"🧾 Your Profile:\n"
            f"Name: {data.get('name')}\n"
            f"Age: {data.get('age')}\n"
            f"Phone: {data.get('phone')}"
        )
    else:
        await message.reply_text("🚫 No profile found. Use /start to create one.")

# /edit command
async def update_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    data = load_data(update.effective_user.id)
    if data:
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Edit Name", callback_data="edit_name"),
                InlineKeyboardButton("Edit Age", callback_data="edit_age")
            ],
            [InlineKeyboardButton("Edit Phone", callback_data="edit_phone")]
        ])
        await message.reply_text("✏️ Choose what you want to edit:", reply_markup=kb)
    else:
        await message.reply_text("🚫 No data to edit. Use /start first.")

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

# Broadcast command
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("Access Denied ❌")

    message = get_arg(context)
    if not message:
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

# Admin-only: list all users
@admin_only
async def all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://files.catbox.moe/9hj4st.jpg"
    kb = [
        [
            InlineKeyboardButton("HELLO BOSS", callback_data="boss")
        ]
    ]
    data = load_all_users()
    if not data:
        await update.message.reply_text("No users found.")

    msg = "All users:\n\n"
    for uid, info in data.items():
        msg += f"ID: {uid}\n"
        msg += f"Name: {info.get('name')}\n"
        msg += f"Age: {info.get('age')}\n"
        msg += f"Phone: {info.get('phone')}\n\n"
    await update.message.reply_photo(
        photo=url,
        caption=msg,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(kb)
    )

# /search command
async def search_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /search <name>")

    name = " ".join(context.args).lower()
    users = load_all_users()

    results = []
    for uid, info in users.items():
        if name in info.get("name", "").lower():
            results.append(f"{info['name']} (ID: {uid})")

    if results:
        await update.message.reply_text("🔍 Found:\n" + "\n".join(results))
    else:
        await update.message.reply_text("No user found.")

# /short command
async def short_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    if not context.args:
        return await message.reply_text("Usage: `/short <URL>`", parse_mode="Markdown")

    long_url = context.args[0]
    await message.reply_text("🔗 Shortening your URL...")

    short_url = shortern_url(long_url)
    await message.reply_text(f"✅ Short URL:\n{short_url}")
