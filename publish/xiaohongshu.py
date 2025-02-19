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


class NewsItem(BaseModel):
    title: str
    content: str


class NewsPublishPackage(BaseModel):
    title: str
    items: list[NewsItem]
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
    content = ""
    for item in news_package.items:
        content += f"{item.title}\n{item.content}\n\n"
    content_tag = driver.find_element(
        "xpath", '//*[@data-placeholder="输入正文描述，真诚有价值的分享予人温暖"]')
    JS_ADD_TEXT_TO_INPUT = """
      var elm = arguments[0], txt = arguments[1];
      elm.value += txt;
      elm.dispatchEvent(new Event('change'));
    """
    driver.execute_script(JS_ADD_TEXT_TO_INPUT, content_tag, content)
    # content_tag.send_keys(content)

    time.sleep(3)
    # 打标签
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
    files = [r"D:\3-code\mini\news-bot\data\image\2025-02-19\00_brief_cover.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-19\01_brief_title.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-19\1_brief_content_238.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-19\2_brief_content_248.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-19\3_brief_content_257.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-19\4_brief_content_241.png",
             r"D:\3-code\mini\news-bot\data\image\2025-02-19\5_brief_content_258.png"]
    items = [NewsItem(title="1️⃣ AI才女罗福莉已到新岗位上班 此前曾被雷军千万年薪挖角",
                      content="<li>🌟 AI才女罗福莉开启新职业旅程，具体公司暂保密</li><li>🔥 95后曾获雷军千万年薪挖角，小米力邀加入推动AI研究</li><li>🎓 北大硕士背景，曾发表8篇顶会论文</li><li>🏢 从阿里巴巴达摩院到DeepSeek，深度参与MoE大模型研发</li><li>💡 DeepSeek-V2发布，罗福莉称赞其中文处理能力国内领先</li><li>💰 性价比超GPT4，被誉为“性价比之王”</li>"),
             NewsItem(title="2️⃣ 月之暗面推出kimi-latest：可第一时间体验kimi最新模型",
                      content="<li>🌙【月之暗面】发布新品：kimi-latest模型，为开发者带来前沿AI体验！</li><li>🚀 更新亮点：紧跟Kimi智能助手最新进展，128k上下文长度，支持图片理解、自动缓存🔧</li><li>💼 应用场景：适合大模型聊天应用，如ChatWise、ChatBox，提供相似体验</li><li>🔍 特别提醒：moonshot-v1仍适用于意图识别或结构化数据提取</li><li>📞 申请尝鲜：Kimi k1.5长思考模型API，填写申请表，等待邮件通知</li><li>🌟 未来展望：月之暗面科技致力于AI开放平台发展，推动技术革新与应用</li>"),
             NewsItem(title="3️⃣ 马斯克推出超级智能聊天机器人 Grok 3，号称 “地球上最聪明的 AI”",
                      content="<li>🚀 马斯克发布 Grok3，自诩“最聪明AI”</li><li>🔥 Grok3家族强大，Grok3mini快速解答</li><li>💡 数学、科学、代码领域表现卓越</li><li>🤖 Colossus超级计算机加速开发，训练达2亿GPU小时</li><li>🔍 新增“推理”功能，提升复杂任务处理能力</li><li>🔎 DeepSearch功能：快速互联网信息摘要回应</li><li>📣 SuperGrok订阅服务，即将推出语音模式</li><li>🌟 未来开源Grok2，扩大开发者生态</li>"),
             NewsItem(title="4️⃣ 李彦宏：百度文库AI功能月活用户达9400万，订阅收入同比增长21%",
                      content='<li>🌟 Paytm 应用内上线 AI 智能搜索工具——Perplexity，"问 AI" 助用户快速获取信息。</li><li>👨‍💼 Paytm CEO Vijay Shekhar Sharma 大赞 Perplexity AI，显示对 AI 技术的重视。</li><li>🌍 Perplexity 积极拓展印度市场，CEO Aravind Srinivas 社交媒体广发英雄帖。</li><li>💸 Srinivas 个人投资百万美元助力印度 AI 发展，设高额奖金激励团队。</li><li>🔍 Perplexity "深度研究" 功能免费开放，助力用户处理专业级任务。</li>'),
             NewsItem(title="5️⃣ 特斯拉自动驾驶可能会延迟进入中国。",
                      content="<li>🌟 理想同学App大升级！接入DeepSeek R1🔍与V3模型</li><li>🧠 深度思考+联网搜索，能力飙升</li><li>📚 涵盖多领域知识问答，翻译小能手</li><li>🎨 新增绘画创作，风格多样，创意无限</li><li>📢 每日精选资讯，与AI实时对话，掌握新动态</li>")]

    news_package = NewsPublishPackage(title=title, files=files, items=items)

    publish_news(news_package)
