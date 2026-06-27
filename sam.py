from datetime import datetime, timedelta
import time


def get_game_mode():
    now = datetime.now()

    # زمان شروع چرخه
    start_time = now.replace(hour=19, minute=30, second=0, microsecond=0)

    game_modes = [
        "🎮 گیم مود فعلی: ۲ به ۲",
        "🎮 گیم مود فعلی: ۳ نفره",
        "🎮 گیم مود فعلی: ۳ به ۳",
        "🎮 گیم مود فعلی: ۵ نفره"
    ]

    # اگر قبل از ساعت ۱۹:۳۰ باشد، یک روز به عقب برگرد
    if now < start_time:
        start_time -= timedelta(days=1)

    # محاسبه زمان سپری‌شده
    elapsed_minutes = (now - start_time).total_seconds() / 60

    # هر ۱۲۰ دقیقه یک گیم مود عوض می‌شود
    index = int(elapsed_minutes // 120) % len(game_modes)

    return game_modes[index]


while True:
    print(get_game_mode())
    time.sleep(60)
