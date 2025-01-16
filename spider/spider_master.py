from spider.spider_latepost import get_news_letter
from spider.spider_36kr import get_news_flashes
from spider.spider_aibase import get_latest_news
from util.storage.sqlite_sqlalchemy import globle_db
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore, BaseJobStore
from util.log_util import logger

jobstores = {
    'default': SQLAlchemyJobStore(engine=globle_db.get_engine(), tablename='apscheduler_jobs')
}


def get_latepost_brief_news():
    """
    每天早上9:00执行，get_news_letter，然后插入到表t_brief_news内
    """
    logger.info('开始爬取最新晚点早知道...')
    get_news_letter()
    logger.info('最新晚点早爬取结束...')


def get_36kr_brief_news():
    """
    每隔3个小时执行，get_news_flashes，然后插入到表t_brief_news内
    """
    logger.info('开始爬取最新36kr快讯...')
    get_news_flashes()
    logger.info('最新36kr快讯爬取结束...')


def get_aibase_brief_news():
    """
    每隔3个小时执行，get_news_flashes，然后插入到表t_brief_news内
    """
    logger.info('开始爬取最新aibase快讯...')
    get_latest_news()
    logger.info('最新aibase快讯爬取结束...')


if __name__ == '__main__':
    scheduler = BlockingScheduler(jobstores=jobstores)

    # # 每天早上9:00执行，get_latepost_brief_news
    # scheduler.add_job(get_latepost_brief_news, CronTrigger(hour=9, minute=0), id='get_latepost_brief_news',
    #                   replace_existing=True)
    # # 每隔3个小时执行，get_36kr_brief_news，每天6点到22点执行
    # scheduler.add_job(get_36kr_brief_news, CronTrigger(hour='6-22/3'), id='get_36kr_brief_news',
    #                   replace_existing=True)

    # 测试
    scheduler.add_job(get_latepost_brief_news, IntervalTrigger(seconds=15), id='get_latepost_brief_news',
                      replace_existing=True)
    # 每隔3个小时执行，get_36kr_brief_news，每天6点到22点执行
    scheduler.add_job(get_36kr_brief_news, IntervalTrigger(seconds=10), id='get_36kr_brief_news',
                      replace_existing=True)
    scheduler.start()
