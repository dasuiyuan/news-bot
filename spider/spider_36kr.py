import requests
from bs4 import BeautifulSoup
from util.log_util import logger
from .po.news_po import BriefNews
from util.storage.sqlite_sqlalchemy import globle_db

# URL to scrape
ROOT_URL = "https://www.36kr.com/"

# Custom headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def get_news_flashes() -> dict[BriefNews]:
    """
    36kr—新闻快讯
    :return:
    """
    all_news = {}
    try:
        # Send GET request
        response = requests.get(f"{ROOT_URL}/newsflashes", headers=HEADERS)
        # Check if request was successful
        if response.status_code != 200:
            logger.warning("访问36kr失败")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')

        newsflash_list = soup.find('div', class_='newsflash-catalog-flow-list')

        if newsflash_list is None:
            logger.warning("没找到新闻标签")
            return None
        flow_item_list = newsflash_list.find_all('div', class_='flow-item')
        for item in flow_item_list:
            title = item.find('div', class_='newsflash-item').find('a').text.strip()
            content = item.find('div', class_='item-desc').find('span').text.strip()
            all_news[title] = content
    except Exception as e:
        logger.warning(f"访问36kr失败: {e}")

    return all_news


def has_same_news(brief_news: BriefNews):
    with globle_db.get_session() as session:
        news_obj = session.query(BriefNews).filter(BriefNews.title == brief_news.title,
                                                   BriefNews.time == brief_news.time).first()
        return news_obj is not None


if __name__ == "__main__":
    # 晚点-新闻早知道
    all_news = get_news_flashes()
    if all_news is not None:
        for title, content in all_news.items():
            print(f"【{title}】")
            print(content)