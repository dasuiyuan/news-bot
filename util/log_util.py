# -*- coding: utf-8 -*-
# @Time: 2024/11/21 17:29
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

import sys
import logging
from loguru import logger
from settings import LOG_FILE

# 配置 logger
logger.remove()  # 移除默认的控制台输出
logger.add(sys.stderr, level="INFO", format="{time} - {level} - {message}")

# 添加文件输出，自动轮转
logger.add(LOG_FILE, rotation="500 MB", level="INFO", format="{time} - {level} - {message}")


# 捕获标准库 logging 的日志
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 获取对应的 Loguru 日志级别
        level = logger.level(record.levelname).name
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# 设置标准库日志的基础配置
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# 导出 logger
__all__ = ["logger"]
