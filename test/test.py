from datetime import datetime, timedelta

print((datetime.now() - timedelta(days=1)).year)

# 输出昨天9点10分的时间戳

print((datetime.now() - timedelta(days=1)))

yesterday_9_10 = datetime.now() - timedelta(days=1)
yesterday_9_10 = yesterday_9_10.replace(hour=9, minute=10, second=0, microsecond=0)
print(yesterday_9_10.strftime("%Y-%m-%d %H:%M"))
