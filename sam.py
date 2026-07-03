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
# WEB SERVER
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
# START
# =====================================

START_MESSAGE = """
🎮 به ربات متاتانک خوش آمدید

دستورات:

🎮 گیم مود
📢 کانال ما
🏆 کانال رسمی
📚 کانال آموزشی
"""

# =====================================
# GAME MODE
# =====================================

GAME_MODE = """
🎮 جدول گیم مود متاتانک

🕐 01:30 → 🔥 5 نفره
🕒 03:30 → 👥 2 به 2
🕔 05:30 → 👤 3 نفره
🕖 07:30 → ⚔️ 3 به 3

🕘 09:30 → 🔥 5 نفره
🕚 11:30 → 👥 2 به 2
🕐 13:30 → 👤 3 نفره
🕒 15:30 → ⚔️ 3 به 3

🕔 17:30 → 🔥 5 نفره
🕖 19:30 → 👥 2 به 2
🕘 21:30 → 👤 3 نفره
🕚 23:30 → ⚔️ 3 به 3

♻️ سپس دوباره تکرار می‌شود.
"""

# =====================================
# SEND
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
        print(e)

# =====================================
# BOT
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

        # ضد JSON ERROR
        if not response.text.strip():
            time.sleep(2)
            continue

        try:
            result = response.json()
        except:
            print("JSON ERROR")
            print(response.text)
            time.sleep(5)
            continue

        if "data" not in result:
            time.sleep(2)
            continue

        data = result["data"]

        if data.get("next_offset_id"):
            last_offset = data["next_offset_id"]

        updates = data.get(
            "updates",
            []
        )

        for update in updates:

            uid = str(update)

            # ضد اسپم
            if uid in processed:
                continue

            processed.add(uid)

            if len(processed) > 100:
                processed.clear()

            if update.get("type") != "NewMessage":
                continue

            chat_id = update["chat_id"]

            text = str(
                update["new_message"].get(
                    "text",
                    ""
                )
            ).strip()

            print(text)

            answer = None

            if text in [
                "/start",
                "استارت"
            ]:

                answer = START_MESSAGE

            elif text == "گیم مود":

                answer = GAME_MODE

            elif text == "کانال ما":

                answer = """
📢 کانال ما

@mtatank
"""

            elif text == "کانال رسمی":

                answer = """
🏆 کانال رسمی

@metatank
"""

            elif text == "کانال آموزشی":

                answer = """
📚 کانال آموزشی

@mtatankamuzesh
"""

            if answer:
                send(
                    chat_id,
                    answer
                )

        time.sleep(2)

    except Exception as e:

        print(e)

        traceback.print_exc()

        time.sleep(5)
