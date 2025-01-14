import requests
from datetime import datetime
from bs4 import BeautifulSoup
from spider.po.news_po import BriefNews
from util.log_util import logger
from util.storage.sqlite_sqlalchemy import globle_db
from util.spider_util import get_user_agent

# URL to scrape
ROOT_URL = "https://www.latepost.com"

WEB_SITE = "latepost"


def get_news_letter() -> list[BriefNews]:
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
            logger.warning("访问latepost失败")
            return all_news
        soup = BeautifulSoup(response.text, 'html.parser')

        newsletter_list = soup.find_all('div', class_='Newsletter-li')

        if newsletter_list is None:
            logger.warning("没找到新闻标签")
            return all_news

        item = newsletter_list[0]
        # 从item中提取herf路径
        href = item.find('a')['href']
        # 将href和root_url拼接为完整URL
        url = ROOT_URL + href
        # 获取新闻集的标题
        collection_title = item.find('span', class_='Newsletter-li-title').text.strip()

        # 发送GET请求获取新闻详情页面
        brief_response = requests.get(url, headers=headers)
        if brief_response.status_code == 200:
            brief_soup = BeautifulSoup(brief_response.text, 'html.parser')
            # 获取时间
            time_div = brief_soup.find('div', class_='article-header-date')
            time_str = time_div.text
            # 获取当前年份
            current_year = datetime.now().year
            # 定义时间格式
            time_format = "%m月%d日 %H:%M"
            # 将时间字符串转换为datetime对象，假设为当前年份
            dt_object = datetime.strptime(f"{current_year}年{time_str}", f"%Y年{time_format}")
            # 将datetime对象转换为时间戳
            timestamp = int(dt_object.timestamp())

            # 判断是否已经爬取过相同新闻
            if _has_same_brief_news(url, timestamp):
                logger.warning(f"已爬取过该新闻:{collection_title} {url} {time_str}")
                return all_news

            # 获取id=select-main的div
            news_div = brief_soup.find('div', id='select-main')
            if news_div:
                # 获取id=select-main的div中的所有p标签
                p_tags = news_div.find_all('p')
                # 依次遍历p标签，如果p标签内部存在class=ql-bg的span标签，则将span标签中的内容作为标题，并将后续所有p标签内容作为内容，直到遇到下一个p标签
                brief_news = None
                for p in p_tags:
                    if p.find('span', class_='ql-bg'):
                        if brief_news is not None:
                            all_news.append(brief_news)
                        brief_news = BriefNews(title=p.get_text(strip=True), content="", time=timestamp,
                                               web_site=WEB_SITE, url=url)
                        continue
                    content = p.get_text(strip=True)
                    if content != "":
                        brief_news.content += content
                all_news.append(brief_news)
            else:
                logger.warning("未找到指定的div标签。")
        else:
            logger.warning(f"访问brief news失败: {brief_response}")

        # 插入数据库
        globle_db.add_all(all_news)
        logger.info(f"已爬取到{len(all_news)}条新闻")
    except Exception as e:
        logger.warning(f"访问latepost失败: {e}")
    return all_news


def _has_same_brief_news(url: str, timestamp: int):
    with globle_db.get_session() as session:
        news_obj = session.query(BriefNews).filter(BriefNews.url == url,
                                                   BriefNews.time == timestamp, BriefNews.web_site == WEB_SITE).first()
        return news_obj is not None


if __name__ == "__main__":
    # 晚点-新闻早知道
    all_news = get_news_letter()
    for news in all_news:
        print(f"【{news.title}】")
        print(f"{news.content}")
