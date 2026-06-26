from datetime import datetime, timedelta

def get_game_mode():
    now = datetime.now()
    start_time = now.replace(hour=17, minute=30, second=0, microsecond=0)  # زمان شروع دقیقاً 17:30
    interval = 120  # ۲ ساعت به دقیقه

    modes = [
        "گیم مود ۲ ساعته ۳به۳",
        "گیم مود ۲ ساعته ۵نفره",
        "گیم مود ۲ ساعته ۲به۲",
        "گیم مود ۲ ساعته ۳نفره"
    ]

    # اگر الان قبل از 17:30 باشه، هنوز شروع نکردیم
    if now < start_time:
        return "در حال حاضر فعال نیست، صبر کنید تا ساعت 17:30"

    # محاسبه زمان از شروع
    elapsed_minutes = (now - start_time).total_seconds() // 60  # زمان گذشته به دقیقه
    index = int(elapsed_minutes // interval) % len(modes)
    
    return modes[index]

print("گیم مود فعلی:")
print(get_game_mode())
