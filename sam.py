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
                if text in ["کانال ما", "کانال", "/channel"]:
                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": "📢 کانال ما:\n@mtatank"
                        }
                    )

                # کانال رسمی
                elif text == "کانال رسمی":
                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": "⭐ کانال رسمی:\n@metatank"
                        }
                    )

                # کانال آموزشی
                elif text == "کانال آموزشی":
                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": "📚 کانال آموزشی:\n@mtatankamuzesh"
                        }
                    )

                # درباره ما
                elif text == "درباره ما":
                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text":
                                "📞 ارتباط با ما\n\n"
                                "🔹 برای سوالات و گزارش باگ:\n"
                                "@ELXELX240\n\n"
                                "🔹 برای ایده و ارتباط با ادمین:\n"
                                "@ll24llll"
                        }
                    )

                # درباره بازی
                elif text == "درباره بازی":
                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text":
                                "🎮 متاتانک یک بازی تانکی آنلاین و رقابتی است.\n\n"
                                "⚔️ نبردهای چندنفره\n"
                                "🏆 رقابت با بازیکنان\n"
                                "🔧 ارتقای تجهیزات\n"
                                "🧠 نیازمند مهارت و استراتژی"
                        }
                    )

                # استارت
                elif text in ["/start", "شروع", "استارت"]:
                    requests.post(
                        API_URL + "sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text":
                                "🤖 به ربات MetaTank خوش آمدید.\n\n"
                                "دستورات:\n"
                                "• کانال ما\n"
                                "• کانال رسمی\n"
                                "• کانال آموزشی\n"
                                "• درباره ما\n"
                                "• درباره بازی"
                        }
                    )

        time.sleep(2)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
