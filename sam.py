import requests
import time
from datetime import datetime, timedelta

TOKEN = "BIBDIH0ALVYLUZEPQNKQSTGGWYWLYBESCODHFEBDXAASBSVLIIOEOWPUNMEYXPJB"
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

    elapsed_minutes = (
        now - start
    ).total_seconds() // 60

    index = int(
        elapsed_minutes // 120
    ) % len(modes)

    return modes[index]


print("🤖 Rubika Bot Started...")

while True:
    try:
        payload = {
            "limit": 10
        }

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
            for update in result["data"]:

                last_event_id = update.get(
                    "event_id"
                )

                if "message" not in update:
                    continue

                message = update["message"]

                chat_id = message.get(
                    "chat_id"
                )

                text = message.get(
                    "text", ""
                ).strip()

                print(
                    "پیام:",
                    text
                )

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
                        },
                        timeout=20
                    )

                    print(
                        "گیم مود ارسال شد"
                    )

        time.sleep(2)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
