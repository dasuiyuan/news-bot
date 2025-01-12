from spider.spider_latepost import get_news_letter
from spider.spider_36kr import get_news_flashes
from spider.po.news_po import BriefNews
from util.storage.sqlite_sqlalchemy import SQLiteDB
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore, BaseJobStore

db = SQLiteDB("sqlite:////Users/suiyuan/personal/news-bot/code/news-bot/spider/data/news_bot.db")
jobstores = {
    'default': SQLAlchemyJobStore(engine=db.get_engine(), tablename='apscheduler_jobs')
}


def get_latepost_brief_news():
    """
    每天早上9:00执行，get_news_letter，然后插入到表t_brief_news内
    """
    all_brief_news = get_news_letter()
    db.add_all(all_brief_news)


def get_36kr_brief_news():
    """
    每隔3个小时执行，get_news_flashes，然后插入到表t_brief_news内
    """
    all_brief_news = get_news_flashes()
    db.add_all(all_brief_news)

if __name__ == '__main__':
    scheduler = BlockingScheduler(jobstores=jobstores)
    # 每天早上9:00执行，get_latepost_brief_news
    scheduler.add_job(get_latepost_brief_news, CronTrigger(hour=9, minute=0), id='get_latepost_brief_news',
                      replace_existing=True)
    # 每隔3个小时执行，get_36kr_brief_news，每天6点到22点执行
    scheduler.add_job(get_36kr_brief_news, CronTrigger(hour='6-22/3'), id='get_36kr_brief_news',
                      replace_existing=True)
    scheduler.start()
