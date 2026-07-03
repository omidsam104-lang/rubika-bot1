from datetime import datetime

TOKEN = "BIBDIH0MUOMDTRTXIWQGFYSNKUJJJRCVJSDBUOGCYYJUXBTVRNPDSBETNPJDOQIT"

CHANNEL = "@mtatank"
OFFICIAL = "@metatank"
EDU = "@mtatankamuzesh"

def game_mode():

    hour = datetime.now().hour

    if 0 <= hour < 6:
        return "🎮 گیم مود: 2 به 2"

    elif 6 <= hour < 12:
        return "🎮 گیم مود: 3 نفره"

    elif 12 <= hour < 18:
        return "🎮 گیم مود: 4 نفره"

    else:
        return "🎮 گیم مود: 5 نفره"


def answer(text):

    text = text.strip()

    if text in ["استارت", "/start"]:
        return """
🎮 ربات متاتانک

دستورات:

📢 کانال ما
🏆 کانال رسمی
📚 کانال آموزشی
🎮 گیم مود
"""

    elif text == "گیم مود":
        return game_mode()

    elif text == "کانال ما":
        return f"📢 {CHANNEL}"

    elif text == "کانال رسمی":
        return f"🏆 {OFFICIAL}"

    elif text == "کانال آموزشی":
        return f"📚 {EDU}"

    return "❌ دستور ناشناخته"


print("🔥 ربات متاتانک آماده است")
