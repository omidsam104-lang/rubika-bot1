import requests
import time
print("شروع فایل")
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
import traceback

# ==================================
# توکن ربات
# ==================================
TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# ==================================
# سرور Render
# ==================================
app = Flask(__name__)

@app.route("/")
def home():
    return "META TANK BOT ONLINE"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web, daemon=True).start()

# ==================================
# گیم مود
# ==================================
def get_game_mode():

    modes = [
        "👥 ۲ به ۲",
        "👤 ۳ نفره",
        "⚔️ ۳ به ۳",
        "🔥 ۵ نفره"
    ]

    now = datetime.now()

    start = datetime(
        now.year,
        now.month,
        now.day,
        19,
        30
    )

    while start > now:
        start -= timedelta(days=1)

    passed = int(
        (now - start).total_seconds() // 7200
    )

    current = passed % len(modes)
    nxt = (current + 1) % len(modes)

    current_time = (
        start +
        timedelta(hours=passed * 2)
    )

    next_time = (
        start +
        timedelta(hours=(passed + 1) * 2)
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

# ==================================
# پیام استارت
# ==================================
START_MESSAGE = """
╔══════════════╗
🎮 META TANK BOT
╚══════════════╝

✨ به ربات META TANK خوش آمدید

شما می‌توانید از قابلیت‌های زیر استفاده کنید:

📢 کانال ما
🏆 کانال رسمی
📚 کانال آموزشی
🎮 گیم مود
📊 آمار بازی
🏅 رتبه بندی
ℹ️ درباره ما
🎮 درباره بازی

━━━━━━━━━━━━━━
🤖 وضعیت: آنلاین 🟢
⚡ نسخه: 2.0
━━━━━━━━━━━━━━
"""

# ==================================
# آمار
# ==================================
users = 0
game_requests = 0

# ==================================
# ربات
# ==================================
last_offset = None

print("🔥 META TANK BOT v2.0 STARTED")

while True:

    try:

        payload = {
            "limit": 20
        }

        if last_offset is not None:
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

        next_offset = data.get(
            "next_offset_id"
        )

        if next_offset:
            last_offset = next_offset

        updates = data.get(
            "updates",
            []
        )

        if not isinstance(
            updates,
            list
        ):
            updates = []

        for update in updates:

            if update.get(
                "type"
            ) != "NewMessage":
                continue

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
                "پیام:",
                text
            )

            answer = None

            # ==================
            # START
            # ==================
            if text == "/start":

                users += 1

                answer = START_MESSAGE

            # ==================
            # کانال ها
            # ==================
            elif text == "کانال ما":

                answer = (
                    "📢 کانال ما:\n"
                    "@mtatank"
                )

            elif text == "کانال رسمی":

                answer = (
                    "🏆 کانال رسمی:\n"
                    "@metatank"
                )

            elif text == "کانال آموزشی":

                answer = (
                    "📚 کانال آموزشی:\n"
                    "@mtatankamuzesh"
                )

            # ==================
            # گیم مود
            # ==================
            elif text in [
                "گیم مود",
                "گیم‌مود",
                "/game"
            ]:

                game_requests += 1

                answer = (
                    get_game_mode()
                )

            # ==================
            # آمار
            # ==================
            elif text == "آمار بازی":

                answer = f"""
📊 آمار ربات

👥 تعداد کاربران:
{users}

🎮 درخواست گیم مود:
{game_requests}
"""

            # ==================
            # رتبه بندی
            # ==================
            elif text == "رتبه بندی":

                answer = """
🏅 رتبه بندی

🚧 این بخش بزودی
فعال خواهد شد.
"""

            # ==================
            # درباره ما
            # ==================
            elif text == "درباره ما":

                answer = """
📞 گزارش باگ:
@ELXELX240

💡 ارتباط با ادمین:
@ll24llll
"""

            # ==================
            # درباره بازی
            # ==================
            elif text == "درباره بازی":

                answer = """
🎮 MetaTank

متاتانک یک بازی آنلاین
تانکی است که بازیکنان
در آن مبارزه کرده و
مهارت های خود را
ارتقا می دهند.
"""

            # ==================
            # دستور ناشناخته
            # ==================
            else:

                answer = (
                    "❌ دستور ناشناخته\n\n"
                    "برای مشاهده منو:\n"
                    "/start"
                )

            r = requests.post(
                API_URL +
                "sendMessage",
                json={
                    "chat_id":
                    chat_id,
                    "text":
                    answer
                },
                timeout=20
            )

            print(
                "SEND:",
                r.text
            )

        time.sleep(1)

    except Exception as e:

        print(
            "خطا:",
            e
        )

        traceback.print_exc()

        time.sleep(5)
