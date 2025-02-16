import os
import time
import json
import traceback
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from util.spider_util import get_user_agent
from pydantic import BaseModel
from datetime import datetime

from publish.liulanqi import COOKING_PATH, get_map4, get_publish_date

XIAOHONGSHU_COOKING = os.path.join(COOKING_PATH, "xiaohongshu.json")


class NewsPublishPackage(BaseModel):
    title: str
    content: str = None
    files: list[str]


def xiaohongshu_login(driver):
    if (os.path.exists(XIAOHONGSHU_COOKING)):
        print("cookies存在")
        with open(XIAOHONGSHU_COOKING) as f:
            cookies = json.loads(f.read())
            driver.get("https://creator.xiaohongshu.com/creator/post")
            driver.implicitly_wait(10)
            driver.delete_all_cookies()
            time.sleep(8)
            # 遍历cook
            print("加载cookie")
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie["expiry"]
                # 添加cook
                driver.add_cookie(cookie)
            time.sleep(5)
            # 刷新
            print("开始刷新")
            driver.refresh()
            driver.get("https://creator.xiaohongshu.com/publish/publish")
            time.sleep(10)
    else:
        print("cookies不存在")
        driver.get('https://creator.xiaohongshu.com/creator/post')
        # driver.find_element(
        #     "xpath", '//*[@placeholder="请输入手机号"]').send_keys("")
        # # driver.find_element(
        # #     "xpath", '//*[@placeholder="请输入密码"]').send_keys("")
        # driver.find_element("xpath", '//button[text()="登录"]').click()
        print("等待登录")
        time.sleep(60)
        print("登录完毕")
        cookies = driver.get_cookies()
        with open(XIAOHONGSHU_COOKING, 'w') as f:
            f.write(json.dumps(cookies))
        print(cookies)
        time.sleep(1)


def publish_xiaohongshu(driver, mp4, index):
    time.sleep(3)
    driver.find_element("xpath", '//*[text()="发布笔记"]').click()
    print("开始上传文件", mp4[0])
    time.sleep(3)
    # ### 上传视频
    vidoe = driver.find_element("xpath", '//input[@type="file"]')
    vidoe.send_keys(mp4[0])

    # 填写标题
    content = mp4[1].replace('.mp4', '')
    driver.find_element(
        "xpath", '//*[@placeholder="填写标题，可能会有更多赞哦～"]').send_keys(content)

    time.sleep(1)
    # 填写描述
    content_clink = driver.find_element(
        "xpath", '//*[@placeholder="填写更全面的描述信息，让更多的人看到你吧！"]')
    content_clink.send_keys(content)

    time.sleep(3)
    # #虐文推荐 #知乎小说 #知乎文
    for label in ["#虐文", "#知乎文", "#小说推荐", "#知乎小说", "#爽文"]:
        content_clink.send_keys(label)
        time.sleep(1)
        data_indexs = driver.find_elements(
            "class name", "publish-topic-item")
        try:
            for data_index in data_indexs:
                if (label in data_index.text):
                    print("点击标签", label)
                    data_index.click()
                    break
        except Exception:
            traceback.print_exc()
        time.sleep(1)

    # 定时发布
    dingshi = driver.find_elements(
        "xpath", '//*[@class="css-1v54vzp"]')
    time.sleep(4)
    print("点击定时发布")
    dingshi[3].click()
    time.sleep(5)
    input_data = driver.find_element("xpath", '//*[@placeholder="请选择日期"]')
    input_data.send_keys(Keys.CONTROL, 'a')  # 全选
    # input_data.send_keys(Keys.DELETE)
    input_data.send_keys(get_publish_date(content, index))
    time.sleep(3)
    # driver.find_element("xpath", '//*[text()="确定"]').click()

    # 等待视频上传完成
    while True:
        time.sleep(10)
        try:
            driver.find_element("xpath",
                                '//*[@id="publish-container"]/div/div[2]/div[2]/div[6]/div/div/div[1]//*[contains(text(),"重新上传")]')
            break;
        except Exception as e:
            traceback.print_exc()
            print("视频还在上传中···")

    print("视频已上传完成！")
    time.sleep(3)
    # 发布
    driver.find_element("xpath", '//*[text()="发布"]').click()
    print("视频发布完成！")
    time.sleep(10)


def publish_pictures(driver, news_package: NewsPublishPackage):
    time.sleep(3)
    driver.find_element("xpath", '//*[text()=" 发布笔记 "]').click()
    print("点击发布笔记")
    time.sleep(1)
    # 切换tab上传图文
    driver.find_element("xpath", '//*[text()="上传图文"]').click()
    print("切换到上传图文")
    time.sleep(1)
    # ### 上传文件
    vidoe = driver.find_element("xpath", '//input[@type="file"]')
    vidoe.send_keys("\n".join(news_package.files))

    # 填写标题
    title = news_package.title
    title_tag = (driver.find_element(
        "xpath", '//*[@placeholder="填写标题会有更多赞哦～"]'))
    title_tag.send_keys(title)

    time.sleep(1)
    # 填写正文
    content = news_package.content
    content_tag = driver.find_element(
        "xpath", '//*[@data-placeholder="输入正文描述，真诚有价值的分享予人温暖"]')
    if news_package.content is not None:
        content_tag.send_keys(content)

    time.sleep(3)
    # #虐文推荐 #知乎小说 #知乎文
    for label in ["#ai", "#新闻", "#科技", "#科技新闻", "#AI新闻", "#人工智能", "#大模型"]:
        content_tag.send_keys(label)
        time.sleep(1)
        try:
            label_tag = driver.find_element("xpath", f"//span[@class='item-name' and text()='{label}']")
            print("点击标签", label)
            label_tag.click()
        except Exception:
            traceback.print_exc()
    time.sleep(1)

    # 发布
    driver.find_element("xpath", '//*[text()="发布"]').click()
    print("发布完成！")
    time.sleep(10)


# # 定时发布
# dingshi = driver.find_elements(
#     "xpath", '//*[@class="css-1v54vzp"]')
# time.sleep(4)
# print("点击定时发布")
# dingshi[3].click()
# time.sleep(5)
# input_data = driver.find_element("xpath", '//*[@placeholder="请选择日期"]')
# input_data.send_keys(Keys.CONTROL, 'a')  # 全选
# # input_data.send_keys(Keys.DELETE)
# input_data.send_keys(get_publish_date(title, index))
# time.sleep(3)
# # driver.find_element("xpath", '//*[text()="确定"]').click()
#
# # 等待视频上传完成
# while True:
#     time.sleep(10)
#     try:
#         driver.find_element("xpath",
#                             '//*[@id="publish-container"]/div/div[2]/div[2]/div[6]/div/div/div[1]//*[contains(text(),"重新上传")]')
#         break;
#     except Exception as e:
#         traceback.print_exc()
#         print("视频还在上传中···")
#
# print("视频已上传完成！")
# time.sleep(3)


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])
    chrome_options.add_argument(f'user-agent={get_user_agent()}')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")

    # 初始化 WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def publish_news(news_package: NewsPublishPackage):
    driver = get_driver()
    xiaohongshu_login(driver=driver)
    publish_pictures(driver, news_package)


if __name__ == "__main__":
    title = f"AI科技每日新鲜事！{datetime.now().strftime('%Y.%m.%d')}"
    files = [r"D:\3-code\mini\news-bot\data\image\2025-02-16\00_brief_cover.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-16\01_brief_title.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-16\1_brief_content_161.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-16\2_brief_content_165.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-16\3_brief_content_163.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-16\4_brief_content_174.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-16\5_brief_content_148.png"]

    news_package = NewsPublishPackage(title=title, files=files)
    publish_news(news_package)
