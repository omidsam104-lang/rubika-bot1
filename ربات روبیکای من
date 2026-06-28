import requests
import time
from datetime import datetime, timedelta

TOKEN = "BIBDIH0ALVYLUZEPQNKQSTGGWYWLYBESCODHFEBDXAASBSVLIIOEOWPUNMEYXPJB"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

last_update_id = None


def get_game_mode():
    now = datetime.now()

    # شروع چرخه از ساعت 19:30
    start = now.replace(
        hour=19,
        minute=30,
        second=0,
        microsecond=0
    )

    # اگر قبل از 19:30 امروز باشیم،
    # چرخه از روز قبل حساب می‌شود
    if now < start:
        start -= timedelta(days=1)

    modes = [
        "🎮 گیم مود فعلی: ۲ به ۲",
        "🎮 گیم مود فعلی: ۳ نفره",
        "🎮 گیم مود فعلی: ۳ به ۳",
        "🎮 گیم مود فعلی: ۵ نفره"
    ]

    # هر 120 دقیقه (2 ساعت) یک گیم مود
    elapsed = (now - start).total_seconds() // 60
    index = int(elapsed // 120) % len(modes)

    return modes[index]


print("🤖 ربات گیم مود فعال شد")

while True:
    try:
        data = {"limit": 10}

        if last_update_id:
            data["start_id"] = last_update_id

        response = requests.post(
            API_URL + "getUpdates",
            json=data,
            timeout=20
        )

        result = response.json()

        if "data" in result:
            for update in result["data"]:

                last_update_id = update.get("event_id")

                if "message" not in update:
                    continue

                chat_id = update["message"]["chat_id"]
                text = update["message"].get("text", "").strip()

                if text in [
                    "گیم مود",
                    "گیم‌مود",
                    "gamemode",
                    "/game"
                ]:

                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": get_game_mode()
                        }
                    )

                    print(
                        f"ارسال شد: {chat_id}"
                    )

        time.sleep(2)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
