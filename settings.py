# -*- coding: utf-8 -*-
# @Time: 2024/11/21 18:30
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

if os.environ.get("ENV") is None:
    os.environ["ENV"] = "dev"

# 系统根目录，必须通过环境变量设置。如未设置则自动使用当前目录。
NEWS_BOT_ROOT = Path(os.environ.get("NEWS_BOT_ROOT", ".")).resolve()

LOG_DIR = NEWS_BOT_ROOT / "logs"

LOG_FILE = LOG_DIR / "news_bot.log"


class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str = "sk-aa41acca1bf1472f83a6e64d4ef6e6bf"
    DEEPSEEK_API_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    QWEN_MODEL: str = "qwen-32b"
    QWEN_API_KEY: str = "4e903a0c42c63f21f0e304c8104de72a"
    QWEN_API_URL: str = "https://ai-api-gateway-cn-north-1.jdcloud.com/api/predict/qwen2-32b/v1"

    GLM_MODEL: str = "glm-4-plus"
    GLM_API_KEY: str = "0b1d50483da246849c179ec9accb9adc.rkcd7DanD0miqTiA"

    XINFERENCE_EMBEDDING_MODEL: str = "bge-m3"
    XINFERENCE_API_URL: str = "http://11.51.202.60:9997"

    DB_PATH: str = str(NEWS_BOT_ROOT / "data" / "news_bot.db")

    model_config = SettingsConfigDict(
        env_file=NEWS_BOT_ROOT / "config" / "application_{}.env".format(os.environ.get("ENV")),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="allow"
    )


geoi_settings = Settings()
print(f"NEWS_BOT_ROOT：{NEWS_BOT_ROOT.resolve()}")
print(f"GLM_API_KEY:【{geoi_settings.GLM_API_KEY}】")
print(f"GLM_MODEL:【{geoi_settings.GLM_MODEL}】")

if __name__ == '__main__':
    print(NEWS_BOT_ROOT)
    print(LOG_DIR)
    print(LOG_FILE)
