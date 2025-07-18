from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from PIL import Image, ImageFont, ImageDraw
import os

# Image request flow
async def image_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🔙 Back", callback_data="start_command")]]
    reply_markup = InlineKeyboardMarkup(kb)

    await update.callback_query.message.reply_text(
        "🖼️ Send your name:",
        reply_markup=reply_markup
    )

    # Save state to expect name next
    context.user_data["image_name_state"] = True

# Handle name and create image
# Handle name and create image
async def handle_image_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("image_name_state"):
        return

    user_name = update.message.text
    context.user_data["image_name_state"] = False

    try:
        img = Image.open("assets/name_image.jpg").convert("RGB")
    except FileNotFoundError:
        await update.message.reply_text("❌ Background image not found.")
        return

    img = img.resize((600, 600))

    try:
        font = ImageFont.truetype("assets/Poppins-Medium.ttf", size=32)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)


    board_box = (100, 500, 500, 400)  # (left, top, right, bottom)


    bbox = draw.textbbox((0, 0), user_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]


    x = board_box[0] + (board_box[2] - board_box[0] - text_width) // 2
    y = board_box[1] + (board_box[3] - board_box[1] - text_height) // 2

    # Draw name with shadow
    draw.text((x + 2, y + 2), user_name, fill="black", font=font)
    draw.text((x, y), user_name, fill="blue", font=font)

    # Save and send
    img_path = f"assets/{update.effective_user.id}_new_image.jpg"
    img.save(img_path)

    with open(img_path, "rb") as photo:
        await update.message.reply_photo(photo, caption="✅ Here is your name image!")

