# -*- coding: utf-8 -*-
# @Time: 2024/8/27 14:59
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
from zhipuai import ZhipuAI

if __name__ == '__main__':
    client = ZhipuAI(api_key="0168e5e6e2ef53bd42e77903f3851303.GgdjBoxIUgj1HBA5")
    response = client.chat.completions.create(
        model="glm-4-0520",
        messages=[{"role": "user", "content": "今天星期几"}, ], stream=True,
    )
    print(response)
