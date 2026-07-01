import requests
import time

TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

last_event_id = None

print("🤖 MetaTank Bot Started")

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
            for update in result["data"]:

                last_event_id = update.get("event_id")

                if "message" not in update:
                    continue

                message = update["message"]
                chat_id = message.get("chat_id")
                text = message.get("text", "").strip()

                print("پیام:", text)

                # کانال ما
                if text in ["کانال ما", "
