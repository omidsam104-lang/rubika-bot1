import requests
import time
from flask import Flask
from threading import Thread

# توکن ربات
TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# -------------------
# سرور برای Render
# -------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "MetaTank Bot Online"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web, daemon=True).start()

print("🤖 MetaTank Bot Started")

last_event_id = None

while True:
    try:
        payload = {"limit": 10}

        if last_event_id:
            payload["start_id"] = last_event_id

        response = requests.post(
            API_URL + "getUpdates",
            json=payload,
            timeout=20
        )

        result = response.json()
        print(result)

        if "data" in result:

            updates = result["data"]

            for update in updates:

                if not isinstance(update, dict):
                    continue

                # ذخیره آخرین شناسه
                if "event_id" in update:
                    last_event_id = update["event_id"]

                # فقط پیام‌های جدید
                if update.get("type") != "NewMessage":
                    continue

                if "new_message" not in update:
                    continue

                chat_id = update["chat_id"]
                text = str(
                    update["new_message"].get("text", "")
                ).strip()

                print("پیام:", text)

                answer = None

                if text == "/start":
                    answer = (
                        "🎮 به ربات MetaTank خوش آمدید\n\n"
                        "📢 کانال ما\n"
                        "🏆 کانال رسمی\n"
                        "📚 کانال آموزشی\n"
                        "ℹ️ درباره ما\n"
                        "🎮 درباره بازی"
                    )

                elif text == "کانال ما":
                    answer = "📢 کانال ما:\n@mtatank"

                elif text == "کانال رسمی":
                    answer = "🏆 کانال رسمی:\n@metatank"

                elif text == "کانال آموزشی":
                    answer = "📚 کانال آموزشی:\n@mtatankamuzesh"

                elif text == "درباره ما":
                    answer = (
                        "📞 برای سوال و گزارش باگ:\n"
                        "@ELXELX240\n\n"
                        "💡 برای ایده و ارتباط با ادمین:\n"
                        "@ll24llll"
                    )

                elif text == "درباره بازی":
                    answer = (
                        "🎮 MetaTank\n\n"
                        "متاتانک یک بازی تانکی آنلاین است که "
                        "بازیکنان در آن با تانک‌های مختلف "
                        "مبارزه می‌کنند و مهارت‌های خود را "
                        "ارتقا می‌دهند."
                    )

                if answer:
                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": answer
                        },
                        timeout=20
                    )

        time.sleep(2)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
