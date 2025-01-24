# -*- coding: utf-8 -*-
# @Time: 2025/1/21 9:48
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
import os
import imgkit
from datetime import datetime
from util import init_env

init_env()
from util.llm_util import chat_deepseek
from process import prompt
from spider.po.news_po import BriefNews
from util.storage.sqlite_sqlalchemy import globle_db

img_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "image")
template_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "template")
tmp_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "tmp")


def html_to_image(html_content, img_file):
    options = {
        'width': 768,  # 设置宽度
        'height': 1024,  # 设置高度
        'enable-javascript': '',  # 启用JavaScript
        'enable-local-file-access': ''  # 允许访问本地文件
    }
    imgkit.from_string(html_content, img_file, options=options)


def generate_cover():
    image_file = os.path.join(img_path, "brief_cover.png")
    html_file = os.path.join(template_path, "brief_cover.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_str_list = f.readlines()
        html_content = "".join(html_str_list).replace("{{today}}", datetime.now().strftime("%Y-%m-%d"))
        html_to_image(html_content, image_file)


def generate_news_title(brief_news_list: list[BriefNews]):
    image_file = os.path.join(img_path, "brief_title.png")
    html_file = os.path.join(template_path, "brief_title.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_str_list = f.readlines()
        html_content = "".join(html_str_list)
        for idx, news in enumerate(brief_news_list):
            title = news.title
            html_content = html_content.replace(f"第{idx + 1}个新闻", title)
        html_to_image(html_content, image_file)


def generate_news_content(brief_news: BriefNews):
    image_file = os.path.join(img_path, f"brief_content_{brief_news.id}.png")
    html_file = os.path.join(template_path, "brief_content.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_str_list = f.readlines()
        html_content = "".join(html_str_list)
        # 将图片的blob存储到tmp下
        news_img_file = os.path.join(tmp_path, "img_default.png")
        if brief_news.image is not None:
            with open(os.path.join(tmp_path, f"img_{brief_news.id}.png"), "wb") as f:
                f.write(brief_news.image)
            news_img_file = os.path.join(tmp_path, f"img_{brief_news.id}.png")
        html_content = html_content.replace("$news_img$", news_img_file)
        # llm总结50个字
        response = chat_deepseek().complete(
            prompt.PROMPT_NEWS_SUMMARIZE.format(length=50, title=brief_news.title, content=brief_news.content))
        summary = response.text
        html_content = html_content.replace("$news_content$", summary)
        html_to_image(html_content, image_file)


if __name__ == "__main__":
    # generate_cover()

    generate_news_title(BriefNews(id=1))
