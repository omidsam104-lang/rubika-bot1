import asyncio
from rubika_bot_api.api import Robot
from rubika_bot_api import filters

TOKEN = "BIBDIH0MUOMDTRTXIWQGFYSNKUJJJRCVJSDBUOGCYYJUXBTVRNPDSBETNPJDOQIT"

bot = Robot(token=TOKEN)

users = set()
game_requests = 0


def get_game_mode():
    return """
🎮 برنامه کامل گیم مود متاتانک

🕔 17:30 ➜ 🔥 ۵ نفره
🕢 19:30 ➜ 👥 ۲ به ۲
🕤 21:30 ➜ 👤 ۳ نفره
🕦 23:30 ➜ ⚔️ ۳ به ۳

🕜 01:30 ➜ 🔥 ۵ نفره
🕞 03:30 ➜ 👥 ۲ به ۲
🕠 05:30 ➜ 👤 ۳ نفره
🕢 07:30 ➜ ⚔️ ۳ به ۳

🕘 09:30 ➜ 🔥 ۵ نفره
🕦 11:30 ➜ 👥 ۲ به ۲
🕜 13:30 ➜ 👤 ۳ نفره
🕞 15:30 ➜ ⚔️ ۳ به ۳

━━━━━━━━━━━━━━
♻️ برنامه هر روز تکرار می‌شود
━━━━━━━━━━━━━━
"""


@bot.on_message(filters=filters.pv)
async def on_message(bot, message):

    global game_requests

    text = (message.text or "").strip()

    if text == "/start":
        users.add(message.chat_id)

        await message.reply(
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
⚡ نسخه: 3.0"""
        )

    elif text == "/game":
        game_requests += 1
        await message.reply(get_game_mode())

    elif text == "/channels":
        await message.reply(
            """📢 کانال های متاتانک

🏆 کانال رسمی
@metatank

📚 کانال آموزشی
@mtatankamuzesh

🎮 کانال ما
@mtatank"""
        )

    elif text == "/about":
        await message.reply(
            """ℹ️ درباره ما

📞 گزارش باگ:
@ELXELX240

💡 ارتباط:
@ll24llll"""
        )

    elif text == "/metatank":
        await message.reply(
            """🎮 MetaTank

متاتانک یک بازی آنلاین
تانکی است که بازیکنان
در آن مبارزه می‌کنند."""
        )

    elif text == "/stats":
        await message.reply(
            f"""📊 آمار ربات

👥 کاربران: {len(users)}

🎮 درخواست گیم مود:
{game_requests}

⚡ نسخه: 3.0"""
        )

    elif text == "/help":
        await message.reply(
            "/start\n/game\n/channels\n/about\n/metatank\n/stats\n/help"
        )


if __name__ == "__main__":
    print("META TANK BOT STARTED...")
    asyncio.run(bot.run())
