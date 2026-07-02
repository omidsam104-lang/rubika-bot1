import requests
import time
import traceback
from datetime import datetime
from flask import Flask
from threading import Thread

# ==========================
# TOKEN
# ==========================

TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"

API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# ==========================
# RENDER WEB SERVER
# ==========================

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

# ==========================
# DATABASE
# ==========================

users = set()
game_requests = 0
last_offset = None
handled_messages = set()

# ==========================
# START MESSAGE
# ==========================

START_MESSAGE = """
╔══════════════╗
🎮 META TANK BOT
╚══════════════╝

✨ به ربات META TANK خوش آمدید

دستورات:

/game
/channels
/about
/metatank
/stats
/help

━━━━━━━━━━━━━━
🤖 وضعیت: آنلاین 🟢
⚡ نسخه: 2.1
━━━━━━━━━━━━━━
"""

# ==========================
# GAME MODE
# ==========================

def get_game_mode():

    schedule = [
        ("17:30", "🔥 ۵ نفره"),
        ("19:30", "👥 ۲ به ۲"),
        ("21:30", "👤 ۳ نفره"),
        ("23:30", "⚔️ ۳ به ۳"),
    ]

    now = datetime.now().strftime("%H:%M")

    text = "🎮 برنامه گیم مود متاتانک\n\n"

    for hour, mode in schedule:

        if hour <= now:
            current = mode

        text += f"🕒 {hour} ➜ {mode}\n"

    text += "\n"
    text += f"🟢 گیم مود فعلی:\n{current}"

    return text

# ==========================
# SEND MESSAGE
# ==========================

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

# ==========================
# BOT
# ==========================

print("🔥 META TANK BOT v2.1 STARTED")

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

        updates = data.get(
            "updates",
            []
        )

        if data.get("next_offset_id"):
            last_offset = data["next_offset_id"]

        for update in updates:

            if update.get("type") != "NewMessage":
                continue

            message_id = str(
                update.get(
                    "message_id",
                    ""
                )
            )

            if message_id in handled_messages:
                continue

            handled_messages.add(
                message_id
            )

            if len(
                handled_messages
            ) > 500:
                handled_messages.clear()

            chat_id = update[
                "chat_id"
            ]

            text = str(
                update[
                    "new_message"
                ].get(
                    "text",
                    ""
                )
            ).strip()

            print(
                "MESSAGE:",
                text
            )

            users.add(
                chat_id
            )

            answer = None

            # ===================
            # START
            # ===================

            if text == "/start":

                answer = START_MESSAGE

            # ===================
            # HELP
            # ===================

            elif text == "/help":

                answer = """
📚 راهنما

/start
/game
/channels
/about
/metatank
/stats
"""

            # ===================
            # GAME
            # ===================

            elif text in [
                "/game",
                "گیم مود",
                "گیم‌مود"
            ]:

                game_requests += 1

                answer = get_game_mode()

            # ===================
            # CHANNELS
            # ===================

            elif text == "/channels":

                answer = """
📢 کانال ما:
@mtatank

🏆 کانال رسمی:
@metatank

📚 کانال آموزشی:
@mtatankamuzesh
"""

            # ===================
            # ABOUT
            # ===================

            elif text == "/about":

                answer = """
📞 گزارش باگ:
@ELXELX240

💡 ارتباط:
@ll24llll
"""

            # ===================
            # METATANK
            # ===================

            elif text == "/metatank":

                answer = """
🎮 MetaTank

متاتانک یک بازی
آنلاین تانکی است.
"""

            # ===================
            # STATS
            # ===================

            elif text == "/stats":

                answer = f"""
📊 آمار

👥 کاربران:
{len(users)}

🎮 درخواست گیم مود:
{game_requests}

⚡ نسخه:
2.1
"""

            # ===================
            # UNKNOWN
            # ===================

            else:

                answer = """
❌ دستور ناشناخته

برای شروع:
/start
"""

            send(
                chat_id,
                answer
            )

        time.sleep(1)

    except Exception as e:

        print(
            "ERROR:",
            e
        )

        traceback.print_exc()

        time.sleep(5)
