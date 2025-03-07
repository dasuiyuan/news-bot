from util.llm_util import chat_deepseek, chat_qwen, chat_glm, chat_ali_bailian
from process import prompt
from util.storage.sqlite_sqlalchemy import globle_db, SQLiteDB
from spider.po.news_po import BriefNews
from datetime import datetime, timedelta
import json
import os
from process import image_generate
from util.log_util import logger
from publish.xiaohongshu import NewsPublishPackage, NewsItem, publish_news


def weekly_integrate():
    db = globle_db
    yesterday_9_10 = datetime.now() - timedelta(days=6)
    yesterday_9_10 = yesterday_9_10.replace(hour=9, minute=10, second=0, microsecond=0)
    type_filter = ['AI技术类', 'AI产品类', 'AI商业类', '其他科技类']
    # 从aibase中安popular倒序取出10篇，再从其他来源中分别取出10篇
    with db.get_session() as session:
        aibase_news_list: list[BriefNews] = session.query(BriefNews).filter(BriefNews.web_site == 'aibase',
                                                                            BriefNews.create_time >= int(
                                                                                yesterday_9_10.timestamp()),
                                                                            BriefNews.type.in_(type_filter)).order_by(
            BriefNews.popularity.desc()).limit(10).all()

        latepost_news_list: list[BriefNews] = session.query(BriefNews).filter(BriefNews.web_site == 'latepost',
                                                                              BriefNews.create_time >= int(
                                                                                  yesterday_9_10.timestamp()),
                                                                              BriefNews.type.in_(type_filter)).limit(
            10).all()

        kr36_news_list: list[BriefNews] = session.query(BriefNews).filter(BriefNews.web_site == '36kr',
                                                                          BriefNews.create_time >= int(
                                                                              yesterday_9_10.timestamp()),
                                                                          BriefNews.type.in_(type_filter)).limit(
            10).all()
    weekly_news = aibase_news_list + latepost_news_list + kr36_news_list

    news_str = ""
    for idx, news in enumerate(weekly_news):
        news_str += f"新闻{idx + 1}：{news.title}\n{news.content}\n"

    response = chat_ali_bailian().complete(
        prompt.PROMPT_WEEKLY_INTEGRATE.format(news=news_str))

    return response.text


def generate_weekly_news():
    weekly_news_str = weekly_integrate()
    weekly_news = json.loads(weekly_news_str.replace("```json", "").replace("```", ""))
    img_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "image",
                            datetime.now().strftime("%Y-%m-%d"))

    # 本周封面
    cover_file = image_generate.generate_cover_weekly(img_path)

    # 本周关键词
    keywords_file, keywords_text = image_generate.generate_keywords_weekly(weekly_news["hot-words"], img_path)
    # 本周最热
    # 根据公司名称获取新闻
    with globle_db.get_session() as session:
        brief_company: BriefNews = session.query(BriefNews).filter(BriefNews.web_site == 'aibase',
                                                                   BriefNews.title.like('%' + weekly_news[
                                                                       "hot-company"][
                                                                       "company"] + '%')).limit(
            1).first()

    hot_file, hot_text = image_generate.generate_hot_weekly(weekly_news["hot-company"], weekly_news["hot-tech"],
                                                            img_path,
                                                            brief_company.image)
    # 未来预测
    pre_file, pre_text = image_generate.generate_prediction_weekly(weekly_news["prediction"], img_path)

    news_items = []
    news_items.append(NewsItem(title="1️⃣ 本周关键词", content=keywords_text))
    news_items.append(NewsItem(title="2️⃣ 本周最热", content=hot_text))
    news_items.append(NewsItem(title="3️⃣ 未来预测", content=pre_text))

    # 4、发布
    pub_files = [cover_file, keywords_file, hot_file, pre_file]
    logger.info(f"封面：{cover_file} 关键词：{keywords_file} 热门：{hot_file} 预测：{pre_file}")
    title = "AI科技本周回顾！"
    news_package = NewsPublishPackage(title=title, items=news_items, files=pub_files)
    publish_news(news_package)


if __name__ == '__main__':
    generate_weekly_news()
