import requests
import time
from datetime import datetime, timedelta

TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

last_event_id = None


def get_game_mode():
    now = datetime.now()

    start = now.replace(
        hour=19,
        minute=30,
        second=0,
        microsecond=0
    )

    if now < start:
        start -= timedelta(days=1)

    modes = [
        "🎮 گیم مود فعلی: ۲ به ۲",
        "🎮 گیم مود فعلی: ۳ نفره",
        "🎮 گیم مود فعلی: ۳ به ۳",
        "🎮 گیم مود فعلی: ۵ نفره"
    ]

    elapsed_minutes = int(
        (now - start).total_seconds() // 60
    )

    index = (elapsed_minutes // 120) % len(modes)

    return modes[index]


print("🤖 Rubika Game Mode Bot Started")

while True:
    try:
        response = requests.post(
            API_URL + "getUpdates",
            json={
                "limit": 10
            },
            timeout=20
        )

        result = response.json()

        print("API:", result)

        if "data" in result:
            for update in result["data"]:

                if update.get("event_id"):
                    last_event_id = update["event_id"]

                message = update.get("message")
                if not message:
                    continue

                chat_id = message.get("chat_id")
                text = message.get("text", "").strip()

                print("پیام:", text)

                if text in [
                    "گیم مود",
                    "گیم‌مود",
                    "gamemode",
                    "/game"
                ]:

                    answer = get_game_mode()

                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": answer
                        },
                        timeout=20
                    )

                    print("ارسال شد:", answer)

        time.sleep(2)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
