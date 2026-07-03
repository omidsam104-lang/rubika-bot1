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
    app.run(
        host="0.0.0.0",
        port=10000
    )

Thread(
    target=run_web,
    daemon=True
).start()

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

━━━━━━━━━━━━━━

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
╔════════════╗
🎮 META TANK BOT
╚════════════╝

✨ به ربات متاتانک خوش آمدید

📢 کانال ما
🏆 کانال رسمی
📚 کانال آموزشی
🎮 گیم مود
📊 آمار بازی
ℹ️ درباره ما
🎮 درباره بازی

━━━━━━━━━━

🤖 وضعیت: آنلاین 🟢
⚡ نسخه: 2.0

━━━━━━━━━━
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
    except:
        pass

# =====================================
# MAIN BOT
# =====================================

last_offset = None
processed = set()

print("🔥 META TANK BOT STARTED")

while True:

    try:

        payload = {
            "limit": 20
        }

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

            uid = str(update)

            if uid in processed:
                continue

            processed.add(uid)

            if len(processed) > 1000:
                processed.clear()

            chat_id = update["chat_id"]

            text = str(
                update["new_message"].get(
                    "text",
                    ""
                )
            ).strip()

            print("MESSAGE:", text)

            answer = None

            # START
            if text in [
                "/start",
                "استارت",
                "شروع"
            ]:

                users.add(chat_id)
                answer = START_MESSAGE

            # GAME MODE
            elif text in [
                "/game",
                "گیم مود",
                "گیم‌مود"
            ]:

                game_requests += 1
                answer = get_game_mode()

            # CHANNELS
            elif text in [
                "/channels",
                "کانال ما",
                "کانال رسمی",
                "کانال آموزشی"
            ]:

                answer = """
📢 کانال ها

📢 کانال ما:
@mtatank

🏆 کانال رسمی:
@metatank

📚 کانال آموزشی:
@mtatankamuzesh
"""

            # ABOUT
            elif text in [
                "/about",
                "درباره ما"
            ]:

                answer = """
📞 گزارش باگ:
@ELXELX240

💡 ارتباط:
@ll24llll
"""

            # GAME INFO
            elif text in [
                "/metatank",
                "درباره بازی"
            ]:

                answer = """
🎮 MetaTank

متاتانک یک بازی
آنلاین تانکی است.
"""

            # STATS
            elif text in [
                "/stats",
                "آمار بازی"
            ]:

                answer = f"""
📊 آمار

👥 کاربران:
{len(users)}

🎮 درخواست گیم مود:
{game_requests}

⚡ نسخه:
2.0
"""

            if answer:
                send(chat_id, answer)

        time.sleep(1)

    except Exception as e:

        print("ERROR:", e)

        traceback.print_exc()

        time.sleep(5)
