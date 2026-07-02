import requests
import time
import traceback
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# =====================================
# TOKEN
# =====================================

TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"

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

users = 0
game_requests = 0

# =====================================
# GAME MODE
# =====================================

def get_game_mode():

    modes = [
        "🔥 ۵ نفره",
        "👥 ۲ به ۲",
        "👤 ۳ نفره",
        "⚔️ ۳ به ۳"
    ]

    now = datetime.now()

    base = datetime(
        now.year,
        now.month,
        now.day,
        17,
        30
    )

    if now < base:
        base -= timedelta(days=1)

    passed = int(
        (now - base).total_seconds() // 7200
    )

    current = passed % 4
    nxt = (current + 1) % 4

    current_time = (
        base +
        timedelta(hours=passed * 2)
    )

    next_time = (
        current_time +
        timedelta(hours=2)
    )

    return f"""
🎮 گیم مود متاتانک

🟢 گیم مود فعلی:
{modes[current]}
⏰ ساعت: {current_time.strftime("%H:%M")}

🔜 گیم مود بعدی:
{modes[nxt]}
⏰ ساعت: {next_time.strftime("%H:%M")}
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
🏅 رتبه بندی
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

        updates = data.get(
            "updates",
            []
        )

        for update in updates:

            if update.get("type") != "NewMessage":
                continue

            chat_id = update["chat_id"]

            text = str(
                update["new_message"].get(
                    "text",
                    ""
                )
            ).strip()

            print("MESSAGE:", text)

            answer = None

            # =================
            # START
            # =================

            if text == "/start":

                users += 1

                answer = START_MESSAGE

            # =================
            # HELP
            # =================

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

            # =================
            # GAME
            # =================

            elif text in [
                "/game",
                "گیم مود",
                "گیم‌مود"
            ]:

                game_requests += 1

                answer = get_game_mode()

            # =================
            # CHANNELS
            # =================

            elif text == "/channels":

                answer = """
📢 کانال ها

📢 کانال ما:
@mtatank

🏆 کانال رسمی:
@metatank

📚 کانال آموزشی:
@mtatankamuzesh
"""

            # =================
            # ABOUT
            # =================

            elif text == "/about":

                answer = """
📞 گزارش باگ:
@ELXELX240

💡 ارتباط:
@ll24llll
"""

            # =================
            # METATANK
            # =================

            elif text == "/metatank":

                answer = """
🎮 MetaTank

متاتانک یک بازی
آنلاین تانکی است.
"""

            # =================
            # STATS
            # =================

            elif text == "/stats":

                answer = f"""
📊 آمار

👥 کاربران:
{users}

🎮 درخواست گیم مود:
{game_requests}

⚡ نسخه:
2.0
"""

            # =================
            # UNKNOWN
            # =================

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
