# -*- coding: utf-8 -*-
# @Time: 2025/1/21 9:48
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
import os
import imgkit
from datetime import datetime
from util import init_env
from spider.po.news_po import BriefNews

init_env()

img_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "image")
template_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "template")


def html_to_image(html_content, img_file):
    options = {
        'width': 900,  # 设置宽度
        'height': 1215,  # 设置高度
        'enable-javascript': '',  # 启用JavaScript
    }
    imgkit.from_string(html_content, img_file, options=options)


def generate_cover():
    image_file = os.path.join(img_path, "brief_cover.png")
    html_file = os.path.join(template_path, "brief_cover.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_str_list = f.readlines()
        html_content = "".join(html_str_list).replace("{{today}}", datetime.now().strftime("%Y-%m-%d"))
        html_to_image(html_content, image_file)


def generate_news_title(brief_news: BriefNews):
    image_file = os.path.join(img_path, f"brief_{brief_news.id}.png")


def generate_news_content(brief_news: BriefNews):
    image_file = os.path.join(img_path, f"brief_{brief_news.id}.png")


if __name__ == "__main__":
    generate_cover()
