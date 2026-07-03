import requests
import time
import traceback
from flask import Flask
from threading import Thread

# =====================================
# TOKEN
# =====================================
TOKEN = "BIBDIH0MUOMDTRTXIWQGFYSNKUJJJRCVJSDBUOGCYYJUXBTVRNPDSBETNPJDOQIT"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# =====================================
# WEB SERVER FOR RENDER
# =====================================
app = Flask(__name__)

@app.route("/")
def home():
    return "META TANK BOT ONLINE"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web, daemon=True).start()

# =====================================
# STATISTICS
# =====================================
users = set()
game_requests = 0

# =====================================
# GAME MODE
# =====================================
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

# =====================================
# START MESSAGE
# =====================================
START_MESSAGE = """
🎮 META TANK BOT

✨ به ربات متاتانک خوش آمدید

دستورات:

/start
/game
/channels
/about
/metatank
/stats
/help

🟢 وضعیت: آنلاین
⚡ نسخه: 3.0
"""

# =====================================
# SEND MESSAGE
# =====================================
def send(chat_id, text):
    try:
        requests.post(
            API_URL + "sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=20
        )
    except Exception as e:
        print("SEND ERROR:", e)

# =====================================
# MAIN BOT
# =====================================
last_offset = None

print("🔥 META TANK BOT STARTED")

while True:
    try:
        payload = {"limit": 20}

        if last_offset:
            payload["offset_id"] = last_offset

        response = requests.post(
            API_URL + "getUpdates",
            json=payload,
            timeout=20
        )

        result = response.json()

        if "data" not in result:
            time.sleep(1)
            continue

        data = result["data"]

        if data.get("next_offset_id"):
            last_offset = data["next_offset_id"]

        updates = data.get("updates", [])

        for update in updates:

            if update.get("type") != "NewMessage":
                continue

            chat_id = update["chat_id"]
            text = str(
                update["new_message"].get("text", "")
            ).strip()

            print("MESSAGE:", text)

            answer = None

            if text == "/start":
                users.add(chat_id)
                answer = START_MESSAGE

            elif text == "/game":
                game_requests += 1
                answer = get_game_mode()

            elif text == "/channels":
                answer = """
📢 کانال های متاتانک

🏆 کانال رسمی
@metatank

📚 کانال آموزشی
@mtatankamuzesh

🎮 کانال ما
@mtatank
"""

            elif text == "/about":
                answer = """
📞 گزارش باگ:
@ELXELX240

💡 ارتباط:
@ll24llll
"""

            elif text == "/metatank":
                answer = """
🎮 MetaTank

متاتانک یک بازی آنلاین
تانکی است.
"""

            elif text == "/stats":
                answer = f"""
📊 آمار ربات

👥 کاربران:
{len(users)}

🎮 درخواست گیم مود:
{game_requests}

⚡ نسخه: 3.0
"""

            elif text == "/help":
                answer = """
/start
/game
/channels
/about
/metatank
/stats
/help
"""

            # فقط به دستورات معتبر پاسخ بده
            if answer:
                send(chat_id, answer)

        time.sleep(1)

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        time.sleep(5)
