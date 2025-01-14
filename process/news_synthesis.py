from util.storage.sqlite_sqlalchemy import globle_db
from spider.po.news_po import BriefNews
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from util.storage.sqlite_sqlalchemy import globle_db

jobstores = {
    'default': SQLAlchemyJobStore(engine=globle_db.get_engine(), tablename='apscheduler_jobs')
}


def brief_news_synthesis(news_list):
    with globle_db.get_session() as session:
        for news in news_list:
            brief_news = session.query(BriefNews).filter(BriefNews.url == news.url,
                                                         BriefNews.web_site == news.web_site).first()
            if brief_news is None:
                session.add(news)
            else:
                brief_news.title = news.title
                brief_news.time = news.time


if __name__ == '__main__':
    # 定时每天9:10执行brief_news_synthesis
    scheduler = BlockingScheduler()
    scheduler.add_jobstore(jobstores['default'])
    scheduler.add_job(brief_news_synthesis, CronTrigger(hour=9, minute=10), id='brief_news_synthesis',
                      replace_existing=True)
