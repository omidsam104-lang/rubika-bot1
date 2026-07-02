import requests
import time
import traceback
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# ==================================
# توکن ربات
# ==================================
TOKEN = "BIBDIH0SCWTOUMNTTDUXFMRJSFHLCWVFFAUWITUVUIOJAICHDZFOWYSRYHOFOQLW"
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"

# ==================================
# سرور Render
# ==================================
app = Flask(__name__)

@app.route("/")
def home():
    return "META TANK BOT ONLINE"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web, daemon=True).start()

# ==================================
# گیم مود
# ==================================
def get_game_mode():
    modes = [
        "👥 ۲ به ۲",
        "👤 ۳ نفره",
        "⚔️ ۳ به ۳",
        "🔥 ۵ نفره"
    ]

    now = datetime.now()
    start = datetime(now.year, now.month, now.day, 19, 30)

    while start > now:
        start -= timedelta(days=1)

    passed = int((now - start).total_seconds() // 7200)

    current = passed % len(modes)
    nxt = (current + 1) % len(modes)

    current_time = start + timedelta(hours=passed * 2)
    next_time = start + timedelta(hours=(passed + 1) * 2)

    return f"""
🎮 گیم مود متاتانک

🟢 گیم مود فعلی:
{modes[current]}
⏰ ساعت: {current_time.strftime("%H:%M")}

🔜 گیم مود بعدی:
{modes[nxt]}
⏰ ساعت: {next_time.strftime("%H:%M")}
"""

# ==================================
# استارت
# ==================================
START_MESSAGE = """
╔══════════════╗
🎮 META TANK BOT
╚══════════════╝

✨ به ربات META TANK خوش آمدید

📢 کانال ما
🏆 کانال رسمی
📚 کانال آموزشی
🎮 گیم مود
📊 آمار بازی
🏅 رتبه بندی
ℹ️ درباره ما
🎮 درباره بازی

━━━━━━━━━━━━━━
🤖 وضعیت: آنلاین 🟢
⚡ نسخه: 2.0
━━━━━━━━━━━━━━
"""

users = 0
game_requests = 0
last_offset = None

print("🔥 META TANK BOT v2.0 STARTED")

while True:
    try:
        payload = {"limit": 20}

        if last_offset:
            payload["offset_id"] = last_offset

        response = requests.post(
            API_URL + "getUpdates",
            json=payload,
            timeout=20
        )

        result = response.json()

        if "data" not in result:
            time.sleep(1)
            continue

        data = result["data"]

        if data.get("next_offset_id"):
            last_offset = data["next_offset_id"]

        updates = data.get("updates", [])

        for update in updates:

            if update.get("type") != "NewMessage":
                continue

            chat_id = update["chat_id"]
            text = str(
                update["new_message"].get("text", "")
            ).strip()

            print("پیام:", text)

            answer = None

            # /start
            if text == "/start":
                users += 1
                answer = START_MESSAGE

            # /help
            elif text == "/help":
                answer = """
📚 راهنمای ربات

/start → منوی اصلی
/game → گیم مود
/channels → کانال ها
/about → درباره ما
/metatank → درباره بازی
/stats → آمار
"""

            # کانال ها
            elif text == "/channels":
                answer = """
📢 کانال ما:
@mtatank

🏆 کانال رسمی:
@metatank

📚 کانال آموزشی:
@mtatankamuzesh
"""

            # درباره ما
            elif text == "/about":
                answer = """
📞 گزارش باگ:
@ELXELX240

💡 ارتباط با ادمین:
@ll24llll
"""

            # درباره بازی
            elif text == "/metatank":
                answer = """
🎮 MetaTank

متاتانک یک بازی آنلاین تانکی است
که بازیکنان در آن مبارزه کرده و
مهارت های خود را ارتقا می دهند.
"""

            # آمار
            elif text == "/stats":
                answer = f"""
📊 آمار ربات

👥 کاربران:
{users}

🎮 درخواست گیم مود:
{game_requests}

⚡ نسخه: 2.0
"""

            # گیم مود
            elif text in ["/game", "گیم مود", "گیم‌مود"]:
                game_requests += 1
                answer = get_game_mode()

            # دکمه های فارسی
            elif text == "کانال ما":
                answer = "📢 @mtatank"

            elif text == "کانال رسمی":
                answer = "🏆 @metatank"

            elif text == "کانال آموزشی":
                answer = "📚 @mtatankamuzesh"

            elif text == "آمار بازی":
                answer = f"""
👥 کاربران: {users}
🎮 درخواست گیم مود: {game_requests}
"""

            elif text == "رتبه بندی":
                answer = "🏅 این بخش به زودی فعال می‌شود."

            elif text == "درباره ما":
                answer = "@ELXELX240"

            elif text == "درباره بازی":
                answer = "🎮 MetaTank یک بازی آنلاین تانکی است."

            else:
                answer = "❌ دستور ناشناخته\n/start"

            requests.post(
                API_URL + "sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": answer
                },
                timeout=20
            )

        time.sleep(1)

    except Exception as e:
        print("خطا:", e)
        traceback.print_exc()
        time.sleep(5)
