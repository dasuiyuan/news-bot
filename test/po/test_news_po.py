from spider.po.news_po import BriefNews
from util.storage.sqlite_sqlalchemy import SQLiteDB

if __name__ == '__main__':
    # 初始化数据库工具类
    db = SQLiteDB("sqlite:////Users/suiyuan/personal/news-bot/code/news-bot/spider/data/news_bot.db")

    # db.create_tables()
    #
    # db.add_all([
    #     BriefNews(title="title1", content="content1", web_site="web_site1", source="source1", url="url1", time=1),
    #     BriefNews(title="title2", content="content2", web_site="web_site2", source="source2", url="url2", time=2),
    #     BriefNews(title="title3", content="content3", web_site="web_site3", source="source3", url="url3", time=3),
    # ])

    news_obj: BriefNews = db.get(BriefNews, 1)
    print(news_obj)

    with db.get_session() as session:
        news_obj = session.query(BriefNews).filter(BriefNews.content == 'content2').first()
        print(news_obj.content)
