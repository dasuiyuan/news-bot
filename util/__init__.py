import os
from pathlib import Path


def init_env():
    if os.environ.get("NEWS_BOT_ROOT") is None:
        # 为os.environ["NEWS_BOT_ROOT"]设置相对路径为当前路径的上两层
        os.environ["NEWS_BOT_ROOT"] = str(Path(os.environ.get("NEWS_BOT_ROOT", "..")).resolve())