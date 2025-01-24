# -*- coding: utf-8 -*-
# @Time: 2025/1/21 9:48
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

from util import init_env

init_env()
import os
import imgkit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def html_to_image(html_path, output_path, width=768, height=1024):
    # 设置 Chrome 选项
    options = Options()
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速

    # 初始化 WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 加载 HTML 文件
        driver.get(f"file://{html_path}")

        # 等待页面加载完成
        time.sleep(2)  # 根据需要调整等待时间

        # 截图并保存
        driver.save_screenshot(output_path)
        print(f"Screenshot saved as {output_path}")
    finally:
        # 关闭浏览器
        driver.quit()


if __name__ == "__main__":
    # 初始文字
    print("Hello World!")
    from selenium import webdriver

    driver = webdriver.Chrome()
    driver.get("https://www.baidu.com/")

    # options = {
    #     'width': 900,  # 设置宽度
    #     'height': 1215,  # 设置高度
    #     'enable-javascript': '',  # 启用JavaScript
    #     # 'exclude-from-outline': ''
    # }
    img_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "template", "test1.png")
    html_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "template", "test.html")

    html_to_image(html_path, img_path)

    # imgkit.from_file(html_path, img_path, options=options)
    # from html2image import Html2Image
    #
    # # 创建Html2Image对象
    # hti = Html2Image()
    #
    # # 设置输出图片的大小（可选）
    # result = hti.screenshot(url="https://www.baidu.com/", save_as='dassss.png', size=(900, 1200))
    # print(result)
