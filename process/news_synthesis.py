import os
import random
import image_generate
from datetime import datetime, timedelta
from util.llm_util import chat_deepseek
from spider.po.news_po import BriefNews
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from util.storage.sqlite_sqlalchemy import globle_db
from util.log_util import logger
from process import prompt

jobstores = {
    'default': SQLAlchemyJobStore(engine=globle_db.get_engine(), tablename='apscheduler_jobs')
}


def brief_news_synthesis(count: int = 5, type_filter: list = None):
    # 1、提取最新新闻
    # 从t_brief_news中获取所有create_time大于昨天9:10分的brief_news
    yesterday_9_10 = datetime.now() - timedelta(days=1)
    yesterday_9_10 = yesterday_9_10.replace(hour=9, minute=10, second=0, microsecond=0)
    type_filter = type_filter if type_filter else ['AI技术类', 'AI产品类', 'AI商业类']
    brief_news_list: list[BriefNews] = globle_db.get_after_time(BriefNews, int(yesterday_9_10.timestamp()), type_filter)

    # 2、筛选新闻
    # 遍历所有brief_news，提取出5篇文章，36kr和latepost各一篇，aibase取3篇。如果前两个媒体不够两篇，用aibase。aibase内部根据popularity倒序
    # 筛选不是aibase的brief_news
    not_aibase_list = [_ for _ in brief_news_list if _.web_site != 'aibase']
    if len(not_aibase_list) >= 2:
        not_aibase_list = random.sample(not_aibase_list, 2)
    aibase_list = [_ for _ in brief_news_list if _.web_site == 'aibase']
    sorted_news_list: list[BriefNews] = sorted(aibase_list, key=lambda x: x.popularity, reverse=True)
    candidate_list = sorted_news_list[:count - len(not_aibase_list)] + not_aibase_list

    # 3、生成图片
    img_folder = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "image",
                              datetime.now().strftime("%Y-%m-%d"))
    # 生成封面
    img_cover_file = image_generate.generate_cover(img_folder)

    # 生成新闻标题
    img_title_file = image_generate.generate_news_title(candidate_list, img_folder)

    # 生成新闻内容
    img_content_file_list = []
    for idx, brief in enumerate(candidate_list):
        img_content_file_list.append(image_generate.generate_news_content(brief, img_folder, idx))

    # 4、发布
    logger.info(f"封面：{img_cover_file} 标题：{img_title_file} 内容：{img_content_file_list}")


def news_summarize(brief_news: BriefNews):
    response = chat_deepseek().complete(
        prompt.PROMPT_NEWS_SUMMARIZE.format(length=50, title=brief_news.title, content=brief_news.content))
    return response.text


if __name__ == '__main__':
    # # 定时每天9:10执行brief_news_synthesis
    # scheduler = BlockingScheduler()
    # scheduler.add_jobstore(jobstores['default'])
    # scheduler.add_job(brief_news_synthesis, CronTrigger(hour=9, minute=10), id='brief_news_synthesis',
    #                   replace_existing=True)

    brief_news_synthesis()
