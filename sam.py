import requests
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# =====================
# توکن ربات
# =====================
TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# =====================
# سرور Render
# =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "MetaTank Bot Online"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web, daemon=True).start()

# =====================
# گیم مود
# =====================
def get_game_mode():

    modes = [
        "👥 ۲ به ۲",
        "👤 ۳ نفره",
        "⚔️ ۳ به ۳",
        "🔥 ۵ نفره"
    ]

    now = datetime.now()

    start = now.replace(
        hour=19,
        minute=30,
        second=0,
        microsecond=0
    )

    if now < start:
        start -= timedelta(days=1)

    elapsed = int(
        (now - start).total_seconds() // 7200
    )

    current = elapsed % 4
    nxt = (current + 1) % 4

    current_time = (
        start + timedelta(hours=elapsed * 2)
    ).strftime("%H:%M")

    next_time = (
        start + timedelta(hours=(elapsed + 1) * 2)
    ).strftime("%H:%M")

    return (
        "🎮 گیم مود متاتانک\n\n"
        f"🟢 گیم مود فعلی:\n"
        f"{modes[current]}\n"
        f"⏰ ساعت: {current_time}\n\n"
        f"🔜 گیم مود بعدی:\n"
        f"{modes[nxt]}\n"
        f"⏰ ساعت: {next_time}"
    )

# =====================
# ربات
# =====================
last_offset = None

print("🤖 MetaTank Bot Started")

while True:
    try:

        payload = {}

        if last_offset:
            payload["offset_id"] = last_offset

        response = requests.post(
            API_URL + "getUpdates",
            json=payload,
            timeout=20
        )

        result = response.json()

        print(result)

        if "data" in result:

            data = result["data"]

            if "next_offset_id" in data:
                last_offset = data["next_offset_id"]

            updates = data.get("updates", [])

            for update in updates:

                if update.get("type") != "NewMessage":
                    continue

                chat_id = update["chat_id"]

                text = str(
                    update["new_message"].get(
                        "text", ""
                    )
                ).strip()

                print("پیام:", text)

                answer = None

                # =====================
                # START
                # =====================
                if text == "/start":

                    answer = (
                        "🎮 به ربات META TANK خوش آمدید\n\n"
                        "شما می‌توانید از قابلیت‌های زیر استفاده کنید:\n\n"
                        "📢 کانال ما\n"
                        "🏆 کانال رسمی\n"
                        "📚 کانال آموزشی\n"
                        "🎮 گیم مود\n"
                        "ℹ️ درباره ما\n"
                        "🎮 درباره بازی"
                    )

                # =====================
                # کانال ها
                # =====================
                elif text == "کانال ما":
                    answer = "📢 کانال ما:\n@mtatank"

                elif text == "کانال رسمی":
                    answer = "🏆 کانال رسمی:\n@metatank"

                elif text == "کانال آموزشی":
                    answer = "📚 کانال آموزشی:\n@mtatankamuzesh"

                # =====================
                # گیم مود
                # =====================
                elif text in [
                    "گیم مود",
                    "گیم‌مود",
                    "/game"
                ]:
                    answer = get_game_mode()

                # =====================
                # درباره ما
                # =====================
                elif text == "درباره ما":

                    answer = (
                        "📞 برای سوال و گزارش باگ:\n"
                        "@ELXELX240\n\n"
                        "💡 برای ارتباط با ادمین:\n"
                        "@ll24llll"
                    )

                # =====================
                # درباره بازی
                # =====================
                elif text == "درباره بازی":

                    answer = (
                        "🎮 MetaTank\n\n"
                        "متاتانک یک بازی تانکی آنلاین است "
                        "که بازیکنان در آن با تانک‌های مختلف "
                        "مبارزه می‌کنند و مهارت‌های خود را "
                        "ارتقا می‌دهند."
                    )

                # =====================
                # ارسال
                # =====================
                if answer:

                    r = requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": answer
                        },
                        timeout=20
                    )

                    print("SEND:")
                    print(r.text)

        time.sleep(2)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
