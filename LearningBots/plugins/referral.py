from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import telegram.error
import json
import os

DATA_FILE = "referral_data.json"


def save_refer_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_refer_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)


async def my_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    data = load_refer_data()

    
    if user_id not in data:
        data[user_id] = {
            "referrals": [],
            "referred_by": None,
            "rewards": 0
        }
        save_refer_data(data)

 
    my_link = f"https://t.me/{context.bot.username}?start={user_id}"
    referral_count = len(data[user_id]["referrals"])
    reward_count = data[user_id].get("rewards", 0)

    
    text = (
        f"👤 Hello {user.first_name}!\n\n"
        f"🔗 Your Referral Link:\n{my_link}\n\n"
        f"👥 People you invited: {referral_count}\n"
        f"🏆 Total Rupees: {reward_count}\n\n"
        f"Invite more people to unlock more rewards!"
    )

    kb = [
        [
            InlineKeyboardButton("📬 Share Referral Link", switch_inline_query=my_link),
            InlineKeyboardButton("🔙 Back", callback_data="start_command")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(kb)

    
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
        except telegram.error.BadRequest as e:
            if "message is not modified" in str(e).lower() or "no text" in str(e).lower():
                await update.callback_query.message.reply_text(
                    text=text,
                    reply_markup=reply_markup
                )
            else:
                raise
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup
        )
