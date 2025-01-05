import requests
from bs4 import BeautifulSoup
from util.log_util import logger

# URL to scrape
ROOT_URL = "https://www.latepost.com"

# Custom headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def get_news_letter() -> dict:
    """
    晚点—新闻早知道
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

        newsletter_list = soup.find_all('div', class_='Newsletter-li')

        if newsletter_list is None:
            logger.warning("没找到新闻标签")
            return None

        item = newsletter_list[0]
        # 从item中提取herf路径
        href = item.find('a')['href']
        # 将href和root_url拼接为完整URL
        url = ROOT_URL + href

        # 发送GET请求获取新闻详情页面
        brief_response = requests.get(url, headers=HEADERS)
        if brief_response.status_code == 200:
            brief_soup = BeautifulSoup(brief_response.text, 'html.parser')
            # 获取id=select-main的div
            news_div = brief_soup.find('div', id='select-main')

            if news_div:
                # 获取id=select-main的div中的所有p标签
                p_tags = news_div.find_all('p')
                # 依次遍历p标签，如果p标签内部存在class=ql-bg的span标签，则将span标签中的内容作为标题，并将后续所有p标签内容作为内容，直到遇到下一个p标签
                news_content = None
                for p in p_tags:
                    if p.find('span', class_='ql-bg'):
                        news_content = []
                        all_news[p.get_text(strip=True)] = news_content
                        continue
                    content = p.get_text(strip=True)
                    if content != "":
                        news_content.append(content)
            else:
                logger.warning("未找到指定的div标签。")
        else:
            logger.warning(f"访问brief news失败: {brief_response}")
    except Exception as e:
        logger.warning(f"访问latepost失败: {e}")

    return all_news


if __name__ == "__main__":
    # 晚点-新闻早知道
    all_news = get_news_letter()
    for title, content in all_news.items():
        print(f"【{title}】")
        for line in content:
            print(line)
