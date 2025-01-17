from . import init_env

init_env()

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from util.log_util import logger
from spider.po.news_po import BriefNews
from util.storage.sqlite_sqlalchemy import globle_db
from util.spider_util import get_user_agent

# URL to scrape
ROOT_URL = "https://www.36kr.com"

WEB_SITE = "36kr"


def get_news_flashes() -> list[BriefNews]:
    """
    36kr—新闻快讯
    :return:
    """
    headers = {
        "User-Agent": get_user_agent()
    }

    all_news = []
    try:
        # Send GET request
        response = requests.get(f"{ROOT_URL}/newsflashes", headers=headers)
        # Check if request was successful
        if response.status_code != 200:
            logger.warning("访问36kr失败")
            return all_news
        soup = BeautifulSoup(response.text, 'html.parser')

        newsflash_list = soup.find('div', class_='newsflash-catalog-flow-list')

        if newsflash_list is None:
            logger.warning("没找到新闻标签")
            return None
        flow_item_list = newsflash_list.find_all('div', class_='flow-item')
        for item in flow_item_list:
            title_elem = item.find('a', class_='item-title')
            # 获取title_elem的href
            href = title_elem['href']
            title = title_elem.text.strip()
            if _has_same_news(title):
                continue
            news_url = ROOT_URL + href
            content = item.find('div', class_='item-desc').find('span').text.strip()
            time_relate = item.find('div', class_='item-other').find('span', class_='time').get_text(strip=True)
            timestamp = _time_relate_to_timestamp(time_relate)

            # 通过子页面获取具体时间，目前因为子页面返回的body为空，所以暂时用当前时间来计算
            # brief_response = requests.get(news_url, headers=headers)
            # if brief_response.status_code != 200:
            #     logger.warning(f"访问新闻失败 {news_url}")
            #     continue
            # brief_soup = BeautifulSoup(brief_response.text, 'html.parser')
            # time_str = brief_soup.find('div', class_='item-other').find('span', class_='time').get_text(strip=True)
            # time_format = "%Y年%m月%d日 %H:%M"
            # dt_object = datetime.strptime(time_str, time_format)
            # timestamp = int(dt_object.timestamp())
            # content = brief_soup.find('div', class_='item-desc').find('pre', class_='pre-item-des').get_text(strip=True)

            brief_news = BriefNews(
                title=title,
                url=news_url,
                time=timestamp,
                content=content,
                source=WEB_SITE,
                create_time=int(datetime.now().timestamp())
            )
            all_news.append(brief_news)

        # 插入数据库
        globle_db.add_all(all_news)
        logger.info(f"已爬取到{len(all_news)}条新闻")
    except Exception as e:
        logger.warning(f"访问36kr失败: {e}")

    return all_news


def _has_same_news(title: str):
    with globle_db.get_session() as session:
        news_obj = session.query(BriefNews).filter(BriefNews.title == title,
                                                   BriefNews.web_site == WEB_SITE).first()
        return news_obj is not None


def _time_relate_to_timestamp(time_relate: str) -> int:
    if time_relate.endswith('小时前'):
        hours = int(time_relate[:-3])
        return int((datetime.now() - timedelta(hours=hours)).timestamp())
    elif time_relate.endswith('分钟前'):
        minutes = int(time_relate[:-3])
        return int((datetime.now() - timedelta(minutes=minutes)).timestamp())
    elif time_relate.endswith('秒前'):
        seconds = int(time_relate[:-3])
        return int((datetime.now() - timedelta(seconds=seconds)).timestamp())


if __name__ == "__main__":
    # 晚点-新闻早知道
    all_news = get_news_flashes()
    if all_news is not None and len(all_news) > 0:
        for title, content in all_news.items():
            print(f"【{title}】")
            print(content)
