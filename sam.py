import requests
import time
from flask import Flask
from threading import Thread

# توکن ربات
TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"

API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# --------------------
# سرور برای Render
# --------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "MetaTank Bot Online"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

# --------------------
# ربات
# --------------------
last_event_id = None

print("MetaTank Bot Started")

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

        if "data" in result:
            for update in result["data"]:

                last_event_id = update.get("event_id")

                if "message" not in update:
                    continue

                message = update["message"]
                chat_id = message.get("chat_id")
                text = message.get("text", "").strip()

                print(text)

                answer = None

                if text == "/start":
                    answer = """
🎮 به ربات MetaTank خوش آمدید

📢 کانال ما
🏆 کانال رسمی
📚 کانال آموزشی
ℹ️ درباره ما
🎮 درباره بازی
"""

                elif text == "کانال ما":
                    answer = "📢 کانال ما:\n@mtatank"

                elif text == "کانال رسمی":
                    answer = "🏆 کانال رسمی:\n@metatank"

                elif text == "کانال آموزشی":
                    answer = "📚 کانال آموزشی:\n@mtatankamuzesh"

                elif text == "درباره ما":
                    answer = """
📞 برای سوالات و گزارش باگ:
@ELXELX240

💡 برای ایده‌ها و ارتباط با ادمین:
@ll24llll
"""

                elif text == "درباره بازی":
                    answer = """
🎮 MetaTank

متاتانک یک بازی تانکی آنلاین است که بازیکنان در آن با استفاده از تانک‌های مختلف به نبرد می‌پردازند، مراحل و چالش‌ها را پشت سر می‌گذارند و مهارت‌های خود را ارتقا می‌دهند.
"""

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
