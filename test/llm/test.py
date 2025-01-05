# -*- coding: utf-8 -*-
# @Time: 2024/12/19 16:20
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
import time


def doBase():
    return doSomething()


def doSomething(stream=False):
    values = [1, 2, 3, "aa"]
    if stream:
        for i in values:
            # 睡眠2s
            time.sleep(2)
            yield i
        return
    return values


if __name__ == '__main__':
    print(doBase())
