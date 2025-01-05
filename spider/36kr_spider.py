import requests
from bs4 import BeautifulSoup
from util.log_util import logger

# URL to scrape
ROOT_URL = "https://www.36kr.com/"

# Custom headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def get_news_flashes() -> dict:
    """
    36kr—新闻快讯
    :return:
    """
    all_news = {}
    try:
        # Send GET request
        response = requests.get(ROOT_URL, headers=HEADERS)
        # Check if request was successful
        if response.status_code != 200:
            logger.warning("访问latepost失败")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')

        newsflash_list = soup.find('div', class_='newsflash-catalog-flow-list')

        if newsflash_list is None:
            logger.warning("没找到新闻标签")
            return None
        flow_item_list = newsflash_list.find_all('div', class_='flow-item')
        for item in flow_item_list:
            pass

    except Exception as e:
        logger.warning(f"访问latepost失败: {e}")

    return all_news


if __name__ == "__main__":
    # 晚点-新闻早知道
    all_news = get_latepost_brief_news()
    for title, content in all_news.items():
        print(f"【{title}】")
        for line in content:
            print(line)
