from datetime import datetime
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
    # 从t_brief_news中获取所有create_time大于昨天9:10分的brief_news
    brief_news_list = globle_db.get_after_time(BriefNews, int(datetime.now().timestamp()) - 86400 * 2)
    # 遍历所有brief_news，先进行分类，


if __name__ == '__main__':
    # 定时每天9:10执行brief_news_synthesis
    scheduler = BlockingScheduler()
    scheduler.add_jobstore(jobstores['default'])
    scheduler.add_job(brief_news_synthesis, CronTrigger(hour=9, minute=10), id='brief_news_synthesis',
                      replace_existing=True)
