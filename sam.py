import time
import requests

TOKEN = "BIBDIH0ALVYLUZEPQNKQSTGGWYWLYBESCODHFEBDXAASBSVLIIOEOWPUNMEYXPJB"

URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

last_id = None

while True:
    try:
        data = {
            "limit": 10
        }

        if last_id:
            data["start_id"] = last_id

        r = requests.post(URL + "getUpdates", json=data)
        result = r.json()

        if result.get("data"):
            for update in result["data"]:
                last_id = update.get("event_id")

                text = update["message"].get("text", "")
                chat_id = update["message"]["chat_id"]

                if text == "گیم مود":
                    requests.post(
                        URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": "🎮 گیم مود فعلی:\n🔥 نبرد ۳ نفره"
                        }
                    )

        time.sleep(3)

    except Exception as e:
        print(e)
        time.sleep(5)
