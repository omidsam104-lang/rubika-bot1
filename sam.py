from flask import Flask, request
import requests
import threading
import time

TOKEN = "BIBDIH0MUOMDTRTXIWQGFYSNKUJJJRCVJSDBUOGCYYJUXBTVRNPDSBETNPJDOQIT"

app = Flask(__name__)

# تنظیمات کانال‌ها
CHANNEL = "@mtatank"
OFFICIAL_CHANNEL = "@metatank"
EDU_CHANNEL = "@mtatankamuzesh"

# گیم مودها (24 ساعته)
GAME_MODES = [
    ("2 به 2", "11:30"),
    ("3 نفره", "13:30"),
    ("4 نفره", "15:30"),
    ("2 به 2", "17:30"),
    ("3 نفره", "19:30"),
    ("4 نفره", "21:30"),
]

def send_message(chat_id, text):
    url = "https://messengerg2c56.iranlms.ir/"
    data = {
        "api_version": "5",
        "auth": TOKEN,
        "method": "sendMessage",
        "data": {
            "object_guid": chat_id,
            "text": text
        }
    }
    try:
        requests.post(url, json=data)
    except:
        pass

def get_current_mode():
    current_hour = time.localtime().tm_hour
    for mode, t in GAME_MODES:
        hour = int(t.split(":")[0])
        if current_hour < hour:
            return mode, t

    return GAME_MODES[0]

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return "ربات روشن است"

    try:
        data = request.json

        chat_id = data["data"]["author_object_guid"]
        text = data["data"]["text"].strip()

        # استارت
        if text in ["/start", "استارت"]:
            send_message(
                chat_id,
                "🎮 سلام!\n\n"
                "دستورهای ربات:\n"
                "• گیم مود\n"
                "• کانال ما\n"
                "• کانال رسمی\n"
                "• کانال آموزشی"
            )

        # گیم مود
        elif text == "گیم مود":
            mode, hour = get_current_mode()
            send_message(
                chat_id,
                f"🎮 گیم مود متاتانک\n\n"
                f"🟢 گیم مود فعلی:\n"
                f"👥 {mode}\n"
                f"⏰ ساعت: {hour}"
            )

        # کانال‌ها
        elif text == "کانال ما":
            send_message(chat_id, f"📢 کانال ما:\n{CHANNEL}")

        elif text == "کانال رسمی":
            send_message(chat_id, f"🏆 کانال رسمی:\n{OFFICIAL_CHANNEL}")

        elif text == "کانال آموزشی":
            send_message(chat_id, f"📚 کانال آموزشی:\n{EDU_CHANNEL}")

    except Exception as e:
        print(e)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
