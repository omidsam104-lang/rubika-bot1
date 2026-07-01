import requests
import time
from flask import Flask
from threading import Thread

TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# -------------------
# سرور Render
# -------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "MetaTank Bot Online"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web, daemon=True).start()

# -------------------
# ربات
# -------------------
last_offset = None

print("MetaTank Bot Started")

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
                text = update["new_message"].get("text", "").strip()

                print("پیام:", text)

                answer = None

                if text == "/start":
                    answer = """🎮 به ربات MetaTank خوش آمدید

📢 کانال ما
🏆 کانال رسمی
📚 کانال آموزشی
ℹ️ درباره ما
🎮 درباره بازی"""

                elif text == "کانال ما":
                    answer = "📢 کانال ما:\n@mtatank"

                elif text == "کانال رسمی":
                    answer = "🏆 کانال رسمی:\n@metatank"

                elif text == "کانال آموزشی":
                    answer = "📚 کانال آموزشی:\n@mtatankamuzesh"

                elif text == "درباره ما":
                    answer = """📞 برای سوالات و گزارش باگ:
@ELXELX240

💡 برای ایده و ارتباط با ادمین:
@ll24llll"""

                elif text == "درباره بازی":
                    answer = """🎮 MetaTank

متاتانک یک بازی تانکی آنلاین است که بازیکنان در آن با تانک‌های مختلف مبارزه می‌کنند و مهارت‌های خود را ارتقا می‌دهند."""

                if answer:
                    r = requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": answer
                        },
                        timeout=20
                    )

                    print("SEND RESULT:")
                    print(r.text)

        time.sleep(2)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
