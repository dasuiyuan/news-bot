# -*- coding: utf-8 -*-
# @Time: 2024/8/27 14:59
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
from util.llm_util import chat_deepseek

if __name__ == '__main__':
    client = chat_deepseek()
    response = client.complete("你是谁？")
    print(response)
