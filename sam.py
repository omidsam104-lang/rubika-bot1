import requests
from flask import Flask, request, jsonify

# ==================================
# تنظیمات ربات
# ==================================
TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

app = Flask(__name__)

# ==================================
# آمار
# ==================================
users = 0
game_requests = 0

# ==================================
# ارسال پیام
# ==================================
def send_message(chat_id, text):

    try:

        r = requests.post(
            API_URL + "sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=20
        )

        print("SEND:", r.text)

    except Exception as e:
        print("SEND ERROR:", e)

# ==================================
# گیم مود
# ==================================
def get_game_mode():

    return """
🎮 برنامه کامل گیم مود متاتانک

🕔 17:30 ➜ 🔥 ۵ نفره
🕢 19:30 ➜ 👥 ۲ به ۲
🕤 21:30 ➜ 👤 ۳ نفره
🕦 23:30 ➜ ⚔️ ۳ به ۳

🕜 01:30 ➜ 🔥 ۵ نفره
🕞 03:30 ➜ 👥 ۲ به ۲
🕠 05:30 ➜ 👤 ۳ نفره
🕢 07:30 ➜ ⚔️ ۳ به ۳

🕘 09:30 ➜ 🔥 ۵ نفره
🕦 11:30 ➜ 👥 ۲ به ۲
🕜 13:30 ➜ 👤 ۳ نفره
🕞 15:30 ➜ ⚔️ ۳ به ۳

━━━━━━━━━━━━━━
♻️ برنامه هر روز تکرار می‌شود
━━━━━━━━━━━━━━
"""

# ==================================
# صفحه اصلی
# ==================================
@app.route("/", methods=["GET"])
def home():
    return "META TANK BOT ONLINE"

# ==================================
# وب هوک
# ==================================
@app.route("/", methods=["POST"])
def webhook():

    global users
    global game_requests

    try:

        data = request.json

        print(data)

        if not data:
            return jsonify({"ok": True})

        message = data.get("new_message", {})

        chat_id = message.get("object_guid")
        text = str(
            message.get("text", "")
        ).strip()

        print("TEXT:", text)

        # ==================
        # START
        # ==================
        if text == "/start":

            users += 1

            send_message(
                chat_id,
                """
🎮 META TANK BOT

✨ به ربات متاتانک خوش آمدید

دستورات:

/game
/channels
/about
/metatank
/stats
/help

🟢 وضعیت: آنلاین
⚡ نسخه: 2.1
"""
            )

        # ==================
        # GAME
        # ==================
        elif text == "/game":

            game_requests += 1

            send_message(
                chat_id,
                get_game_mode()
            )

        # ==================
        # CHANNELS
        # ==================
        elif text == "/channels":

            send_message(
                chat_id,
                """
📢 کانال های متاتانک

🏆 کانال رسمی
@metatank

📚 کانال آموزشی
@mtatankamuzesh

🎮 کانال ما
@mtatank
"""
            )

        # ==================
        # ABOUT
        # ==================
        elif text == "/about":

            send_message(
                chat_id,
                """
ℹ️ درباره ما

📞 گزارش باگ:
@ELXELX240

💡 ارتباط:
@ll24llll
"""
            )

        # ==================
        # GAME INFO
        # ==================
        elif text == "/metatank":

            send_message(
                chat_id,
                """
🎮 MetaTank

متاتانک یک بازی آنلاین
تانکی است که بازیکنان
در آن مبارزه می کنند.
"""
            )

        # ==================
        # STATS
        # ==================
        elif text == "/stats":

            send_message(
                chat_id,
                f"""
📊 آمار ربات

👥 کاربران:
{users}

🎮 درخواست گیم مود:
{game_requests}

⚡ نسخه: 2.1
"""
            )

        # ==================
        # HELP
        # ==================
        elif text == "/help":

            send_message(
                chat_id,
                """
📚 راهنما

/start
/game
/channels
/about
/metatank
/stats
/help
"""
            )

        return jsonify({"ok": True})

    except Exception as e:

        print("ERROR:", e)

        return jsonify({"ok": False})

# ==================================
# RUN
# ==================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
