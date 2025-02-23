from util.llm_util import chat_deepseek, chat_qwen, chat_glm, chat_ali_bailian
from process import prompt
from util.storage.sqlite_sqlalchemy import globle_db, SQLiteDB
from spider.po.news_po import BriefNews
from datetime import datetime, timedelta


def weekly_keywords(brief_news_list):
    news_str = ""
    for idx, news in enumerate(brief_news_list):
        news_str += f"新闻{idx + 1}：{news.title}\n{news.content}\n"

    response = chat_glm().complete(
        prompt.PROMPT_WEEKLY_KEYWORDS.format(news=news_str))
    print(response)


def weekly_company(brief_news_list):
    news_str = ""
    for idx, news in enumerate(brief_news_list):
        news_str += f"新闻{idx + 1}：{news.title}\n{news.content}\n"

    response = chat_glm().complete(
        prompt.PROMPT_WEEKLY_HOT_COMPANY.format(news=news_str))
    print(response)


def weekly_tech(brief_news_list):
    news_str = ""
    for idx, news in enumerate(brief_news_list):
        news_str += f"新闻{idx + 1}：{news.title}\n{news.content}\n"

    response = chat_glm().complete(
        prompt.PROMPT_WEEKLY_HOT_TEACH.format(news=news_str))
    print(response)


def weekly_prediction(brief_news_list):
    news_str = ""
    for idx, news in enumerate(brief_news_list):
        news_str += f"新闻{idx + 1}：{news.title}\n{news.content}\n"

    response = chat_glm().complete(
        prompt.PROMPT_WEEKLY_PREDICTION.format(news=news_str))
    print(response)


def weekly_integrate(brief_news_list):
    news_str = ""
    for idx, news in enumerate(brief_news_list):
        news_str += f"新闻{idx + 1}：{news.title}\n{news.content}\n"

    response = chat_ali_bailian().complete(
        prompt.PROMPT_WEEKLY_INTEGRATE.format(news=news_str))
    print(response.text)


if __name__ == '__main__':
    db = SQLiteDB(f"sqlite:///D:\\3-code\mini\\news-bot\\data\\news_bot.db")
    yesterday_9_10 = datetime.now() - timedelta(weeks=1)
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
    weekly_integrate(weekly_news)
