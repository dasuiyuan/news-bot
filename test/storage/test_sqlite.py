import os
from pathlib import Path

# 为os.environ["NEWS_BOT_ROOT"]设置相对路径为当前路径的上两层
os.environ["NEWS_BOT_ROOT"] = str(Path(os.environ.get("NEWS_BOT_ROOT", "../..")).resolve())

from util.storage.sqlite_sqlalchemy import globle_db
from datetime import datetime
from spider.po.news_po import BriefNews

if __name__ == '__main__':
    ts = int(datetime.strptime('2025-04-14 01:00', "%Y-%m-%d %H:%M").timestamp())
    result = globle_db.get_after_time(BriefNews, timestamp=ts)
    print(result)
