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
from util.llm_util import chat_deepseek, chat_glm
from process import prompt
from spider.po.news_po import BriefNews
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
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


def html_to_image_selenium(html_content, img_file, id, width=768, height=1024):
    # 设置 Chrome 选项
    options = Options()
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速

    # 初始化 WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 保存 HTML 文件
        html_path = os.path.join(tmp_path, f"tmp_{id}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # 加载 HTML 文件
        driver.get(f"file://{html_path}")

        # 等待页面加载完成
        time.sleep(3)  # 根据需要调整等待时间

        # 截图并保存
        driver.save_screenshot(img_file)
        print(f"Screenshot saved as {img_file}")
    finally:
        # 关闭浏览器
        driver.quit()


def generate_cover():
    image_file = os.path.join(img_path, "brief_cover.png")
    html_file = os.path.join(template_path, "brief_cover.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_str_list = f.readlines()
        html_content = "".join(html_str_list).replace("{{today}}", datetime.now().strftime("%Y.%m.%d"))
        html_to_image_selenium(html_content, image_file, 'cover', 800, 1190)
    return image_file


def generate_news_title(brief_news_list: list[BriefNews]):
    image_file = os.path.join(img_path, "brief_title.png")
    html_file = os.path.join(template_path, "brief_title.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_str_list = f.readlines()
        html_content = "".join(html_str_list)
        for idx, news in enumerate(brief_news_list):
            title = news.title
            html_content = html_content.replace(f"第{idx + 1}个新闻", title)
        html_to_image_selenium(html_content, image_file, 'title', 790, 1180)
    return image_file


def generate_news_content(brief_news: BriefNews):
    image_file = os.path.join(img_path, f"brief_content_{brief_news.id}.png")
    html_file = os.path.join(template_path, "brief_content.html")
    with open(html_file, "r", encoding="utf-8") as f:
        html_str_list = f.readlines()
        html_content = "".join(html_str_list)
        html_content = html_content.replace("$news_title$", brief_news.title)
        # 将图片的blob存储到tmp下
        news_img_file = os.path.join(tmp_path, "img_default.png")
        if brief_news.image is not None:
            with open(os.path.join(tmp_path, f"img_{brief_news.id}.png"), "wb") as f:
                f.write(brief_news.image)
            news_img_file = os.path.join(tmp_path, f"img_{brief_news.id}.png")
        html_content = html_content.replace("$news_img$", news_img_file)
        # llm总结50个字
        response = chat_glm().complete(
            prompt.PROMPT_NEWS_SUMMARIZE.format(length=50, title=brief_news.title, content=brief_news.content))
        summary = response.text
        html_content = html_content.replace("$news_content$", summary)
        html_to_image_selenium(html_content, image_file, brief_news.id, 768 + 50, 1024 + 150)
    return image_file


if __name__ == "__main__":
    # generate_cover()
    # generate_news_title(BriefNews(id=1))
    # generate_news_content(BriefNews(id=1))
    pass
