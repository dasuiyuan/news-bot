import random
from datetime import datetime, timedelta
from util.llm_util import chat_deepseek
from spider.po.news_po import BriefNews
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from util.storage.sqlite_sqlalchemy import globle_db
from process import prompt

jobstores = {
    'default': SQLAlchemyJobStore(engine=globle_db.get_engine(), tablename='apscheduler_jobs')
}


def brief_news_synthesis(count: int = 5, type_filter: list = None):
    # 1、提取最新新闻
    # 从t_brief_news中获取所有create_time大于昨天9:10分的brief_news
    yesterday_9_10 = datetime.now() - timedelta(days=1)
    yesterday_9_10 = yesterday_9_10.replace(hour=9, minute=10, second=0, microsecond=0)
    brief_news_list: list[BriefNews] = globle_db.get_after_time(BriefNews, int(yesterday_9_10.timestamp()), type_filter)

    # 2、筛选并总结
    # 遍历所有brief_news，提取出5篇文章，36kr和latepost各一篇，aibase取3篇。如果前两个媒体不够两篇，用aibase。aibase内部根据popularity倒序
    # 筛选不是aibase的brief_news
    not_aibase_list = [_ for _ in brief_news_list if _.web_site != 'aibase']
    if len(not_aibase_list) >= 2:
        not_aibase_list = random.sample(not_aibase_list, 2)
    aibase_list = [_ for _ in brief_news_list if _.web_site == 'aibase']
    sorted_news_list: list[BriefNews] = sorted(aibase_list, key=lambda x: x.popularity, reverse=True)
    candidate_list = not_aibase_list + sorted_news_list[:count - len(not_aibase_list)]
    # 对candidate_list进行总结
    final_news_list: list[BriefNews] = []
    for brief_news in candidate_list:
        summary = news_summarize(brief_news)
        final_news_list.append(brief_news)
        final_news_list[-1].content = summary

    # 3、生成图片
    # 生成封面

    # 生成新闻图片

    # 4、发布


def news_summarize(brief_news: BriefNews):
    response = chat_deepseek().complete(
        prompt.PROMPT_NEWS_SUMMARIZE.format(length=50, title=brief_news.title, content=brief_news.content))
    return response.text


if __name__ == '__main__':
    # 定时每天9:10执行brief_news_synthesis
    scheduler = BlockingScheduler()
    scheduler.add_jobstore(jobstores['default'])
    scheduler.add_job(brief_news_synthesis, CronTrigger(hour=9, minute=10), id='brief_news_synthesis',
                      replace_existing=True)
