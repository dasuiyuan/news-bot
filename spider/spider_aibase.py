from . import init_env

init_env()
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from spider.po.news_po import BriefNews
from util.log_util import logger
from util.storage.sqlite_sqlalchemy import globle_db
from util.spider_util import get_user_agent

# URL to scrape
ROOT_URL = "https://www.aibase.com/zh/news"

SINGLE_ROOT_URL = "https://www.aibase.com"

WEB_SITE = "aibase"

NEWS_LIST_CLASS = "flex group justify-between md:flex-row flex-col-reverse hover:bg-[#F0F3FA] rounded-lg md:p-4 py-2 px-0 group"


def get_latest_news() -> list[BriefNews]:
    """
    晚点—新闻早知道
    :return:
    """

    all_news = []
    try:
        # Custom headers to mimic a browser request
        headers = {
            "User-Agent": get_user_agent()
        }
        # Send GET request
        response = requests.get(ROOT_URL, headers=headers)
        # Check if request was successful
        if response.status_code != 200:
            logger.warning(f"访问{WEB_SITE}失败")
            return all_news
        soup = BeautifulSoup(response.text, 'html.parser')

        newsletter_list = soup.find_all('a',
                                        class_=NEWS_LIST_CLASS)

        if newsletter_list is None:
            logger.warning("没找到新闻标签")
            return all_news
        for newsletter in newsletter_list:
            url = SINGLE_ROOT_URL + newsletter['href']
            # 发送GET请求获取新闻详情页面
            brief_response = requests.get(url, headers=headers)
            if brief_response.status_code != 200:
                logger.warning(f"访问{newsletter.find('h3').text}失败: {brief_response}")
                continue

            soup_single = BeautifulSoup(brief_response.text, 'html.parser')

            single_news_root = soup_single.find('div', class_='px-4 flex flex-col mt-8 md:mt-16')
            # 获取新闻标题
            title = newsletter.find('h3').text
            # 获取新闻时间
            sim_title_elem = single_news_root.find('div', class_='flex items-center flex-wrap text-sm text-surface-500')
            sim_title_spans = sim_title_elem.find_all('span')
            time = sim_title_spans[-1].text
            timestamp = int(datetime.strptime(time, "%Y年%m月%d号 %H:%M").timestamp())
            # 获取新闻热度
            pop_elem = single_news_root.find('div', attrs={"aria-label": "views"})
            pop = int(pop_elem.find('span').text)
            # 获取新闻内容
            content_elem = single_news_root.find('div',
                                                 class_='leading-8 text-[#242424] post-content mt-12 text-lg space-y-7')
            p_list = content_elem.find_all('p')
            content = ''
            for p_elem in p_list:
                if p_elem.text.strip() != "":
                    content += p_elem.text.strip() + '\n'
            brief_news = BriefNews(title=title, content=content, time=timestamp, popularity=pop,
                                   web_site=WEB_SITE, url=url, create_time=int(datetime.now().timestamp()))
            all_news.append(brief_news)
        # 插入数据库
        globle_db.add_all(all_news)
        logger.info(f"已爬取到{len(all_news)}条新闻")
    except Exception as e:
        logger.warning(f"访问{WEB_SITE}失败: {e}")
    return all_news


def _has_same_brief_news(url: str, timestamp: int):
    with globle_db.get_session() as session:
        news_obj = session.query(BriefNews).filter(BriefNews.url == url,
                                                   BriefNews.time == timestamp, BriefNews.web_site == WEB_SITE).first()
        return news_obj is not None


if __name__ == "__main__":
    # 晚点-新闻早知道
    all_news = get_latest_news()
    for news in all_news:
        print(f"【{news.title}】")
        print(f"{news.content}")