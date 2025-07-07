import os
import json

DATA_FILE = "data.json"

def save_data(user_id, user_data):
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)
        except json.JSONDecodeError:
            all_data = {}
    else:
        all_data = {}

    all_data[str(user_id)] = user_data
    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

def load_data(user_id):
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)
            return all_data.get(str(user_id))
        except json.JSONDecodeError:
            return None
    return None

def delete_data(user_id):
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)
        except json.JSONDecodeError:
            all_data = {}
    else:
        all_data = {}

    all_data.pop(str(user_id), None)
    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

def load_all_users():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def get_user(user_id):
    return load_all_users().get(str(user_id))

# Credit: Project by LearningBot79
# GitHub: https://github.com/Learningbots79
# Telegram Channel: https://t.me/learningbots79