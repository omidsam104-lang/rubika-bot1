from datetime import datetime
import time

def get_game_mode():
    now = datetime.now()

    start_time = now.replace(hour=19, minute=30, second=0, microsecond=0)

    game_modes = [
        "🎮 گیم مود فعلی: ۲ به ۲",
        "🎮 گیم مود فعلی: ۳ نفره",
        "🎮 گیم مود فعلی: ۳ به ۳",
        "🎮 گیم مود فعلی: ۵ نفره"
    ]

    if now < start_time:
        from datetime import timedelta
        start_time -= timedelta(days=1)

    elapsed_minutes = (now - start_time).total_seconds() // 60
    index = int(elapsed_minutes // 120) % len(game_modes)

    return game_modes[index]

while True:
    print(get_game_mode())
    time.sleep(60)
