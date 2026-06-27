```python
from datetime import datetime

def get_game_mode():
    now = datetime.now()

    # زمان شروع: 19:30
    start_time = now.replace(hour=19, minute=30, second=0, microsecond=0)

    game_modes = [
        "🎮 گیم مود فعلی: ۲ به ۲",
        "🎮 گیم مود فعلی: ۳ نفره",
        "🎮 گیم مود فعلی: ۳ به ۳",
        "🎮 گیم مود فعلی: ۵ نفره"
    ]

    # اگر قبل از 19:30 باشد، یک روز به عقب برگرد
    if now < start_time:
        from datetime import timedelta
        start_time -= timedelta(days=1)

    # محاسبه تعداد بازه‌های 2 ساعته
    elapsed_minutes = (now - start_time).total_seconds() // 60
    index = int(elapsed_minutes // 120) % len(game_modes)

    return game_modes[index]


# نمایش گیم مود فعلی
print(get_game_mode())
```
