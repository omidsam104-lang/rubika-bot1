from flask import Flask, request, jsonify

app = Flask(__name__)

def send_message(chat_id, text):
    # این قسمت را با تابع ارسال پیام روبیکا خودت جایگزین کن
    print(f"SEND TO {chat_id}:")
    print(text)

@app.route("/", methods=["GET"])
def home():
    return "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.json

        if not data:
            return jsonify({"ok": True})

        message = data.get("new_message", {})
        chat_id = message.get("object_guid")
        text = str(message.get("text", "")).strip()

        print("TEXT:", repr(text))

        if text == "/start":
            send_message(
                chat_id,
                """🎮 META TANK BOT

✨ به ربات متاتانک خوش آمدید

دستورات:
/game
/channels
/about
/metatank
/stats
/help

🟢 وضعیت: آنلاین
⚡ نسخه: 2.1"""
            )

        elif text == "/game":
            send_message(
                chat_id,
                """🎮 گیم مود متاتانک

🟢 برنامه امروز:

🔥 ۵ نفره
🕔 ساعت 17:30

👥 ۲ به ۲
🕢 ساعت 19:30

⚔️ اسکواد
🕘 ساعت 21:00"""
            )

        elif text == "/channels":
            send_message(
                chat_id,
                """📢 کانال‌های متاتانک

🏆 کانال رسمی
📚 کانال آموزشی
🎮 کانال گیم مود"""
            )

        elif text == "/about":
            send_message(
                chat_id,
                """ℹ️ درباره متاتانک

🎮 ربات مدیریت گیم مود
⚡ نسخه: 2.1"""
            )

        elif text == "/metatank":
            send_message(
                chat_id,
                "🎮 به دنیای META TANK خوش آمدید!"
            )

        elif text == "/stats":
            send_message(
                chat_id,
                """📊 آمار بازی

👥 بازیکنان: 1250
🎮 مسابقات: 340
🏆 فصل: 7"""
            )

        elif text == "/help":
            send_message(
                chat_id,
                """❓ راهنما

/start
/game
/channels
/about
/metatank
/stats
/help"""
            )

        return jsonify({"ok": True})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"ok": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
