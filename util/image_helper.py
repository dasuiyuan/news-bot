# -*- coding: utf-8 -*-
# @Time: 2025/1/21 9:48
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

from util import init_env

init_env()
import os
import imgkit

if __name__ == "__main__":
    # 初始文字
    print("Hello World!")
    options = {
        'width': 900,  # 设置宽度
        'height': 1215,  # 设置高度
        'enable-javascript': '',  # 启用JavaScript
        # 'exclude-from-outline': ''
    }
    img_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "template", "test.png")
    html_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "template", "test.html")
    imgkit.from_file(html_path, img_path, options=options)
    # from html2image import Html2Image
    #
    # # 创建Html2Image对象
    # hti = Html2Image()
    #
    # # 设置输出图片的大小（可选）
    # result = hti.screenshot(url="https://www.baidu.com/", save_as='dassss.png', size=(900, 1200))
    # print(result)
