import os
import random
import image_generate
from process.po.history_po import HistoryNews
from datetime import datetime, timedelta
from util.llm_util import chat_qwen
from spider.po.news_po import BriefNews
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from util.storage.sqlite_sqlalchemy import globle_db
from util.log_util import logger
from process import prompt
from publish.xiaohongshu import NewsPublishPackage, NewsItem, publish_news

jobstores = {
    'default': SQLAlchemyJobStore(engine=globle_db.get_engine(), tablename='apscheduler_jobs_daily')
}


def brief_news_synthesis(count: int = 5, type_filter: list = None):
    # 1、提取最新新闻
    # 从t_brief_news中获取所有create_time大于昨天9:10分的brief_news
    yesterday_9_10 = datetime.now() - timedelta(days=1)
    yesterday_9_10 = yesterday_9_10.replace(hour=11, minute=00, second=0, microsecond=0)
    type_filter = type_filter if type_filter else ['AI技术类', 'AI产品类', 'AI商业类']
    brief_news_list: list[BriefNews] = globle_db.get_after_time(BriefNews, int(yesterday_9_10.timestamp()), type_filter)

    # 2、筛选新闻
    # 遍历所有brief_news，提取出5篇文章，36kr和latepost各一篇，aibase取3篇。如果前两个媒体不够两篇，用aibase。aibase内部根据popularity倒序
    # 筛选不是aibase的brief_news
    not_aibase_list = [_ for _ in brief_news_list if _.web_site != 'aibase']
    if len(not_aibase_list) >= 2:
        not_aibase_list = random.sample(not_aibase_list, 2)
    aibase_list = [_ for _ in brief_news_list if _.web_site == 'aibase']
    sorted_aibase_list: list[BriefNews] = sorted(aibase_list, key=lambda x: x.popularity, reverse=True)
    candidate_aibase_list = sorted_aibase_list[:count - len(not_aibase_list)]
    candidate_list = candidate_aibase_list + not_aibase_list
    backup_aibase_list = sorted_aibase_list[count - len(not_aibase_list):]

    # 3、生成图片
    img_folder = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "image",
                              datetime.now().strftime("%Y-%m-%d"))
    # 生成封面
    img_cover_file = image_generate.generate_cover(img_folder)

    # 生成新闻内容
    emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
    final_list = []
    img_content_file_list = []
    news_items = []
    for idx, brief in enumerate(candidate_list):
        try:
            file_path, summary = image_generate.generate_news_content(brief, img_folder, idx)
            img_content_file_list.append(file_path)
            final_list.append(brief)
            news_items.append(
                NewsItem(title=f"{emoji_list[idx]} {brief.title}",
                         content=summary.replace("</li><li>", "\n").replace("<li>", "").replace("</li>", "").replace(
                             "<br>", "\n")))
        except Exception as e:
            logger.error(f"{e} 生成新闻内容图片失败，新闻ID：{brief.id} 新闻标题：{brief.title}， 从替补中选择一篇")
            new_brief = backup_aibase_list.pop()
            file_path, summary = image_generate.generate_news_content(new_brief, img_folder, idx)
            img_content_file_list.append(file_path)
            final_list.append(new_brief)
            news_items.append(
                NewsItem(title=f"{emoji_list[idx]} {brief.title}",
                         content=summary.replace("</li><li>", "\n").replace("<li>", "").replace("</li>", "").replace(
                             "<br>", "\n")))
            continue

    # 加入历史
    for n in final_list:
        add_history(n)

    # 生成新闻标题
    img_title_file = image_generate.generate_news_title(final_list, img_folder)

    # 4、发布
    pub_files = [img_cover_file, img_title_file] + img_content_file_list
    logger.info(f"封面：{img_cover_file} 标题：{img_title_file} 内容：{img_content_file_list}")
    title = f"AI科技每日新鲜事！{datetime.now().strftime('%Y.%m.%d')}"
    news_package = NewsPublishPackage(title=title, items=news_items, files=pub_files)
    publish_news(news_package)


def news_summarize(brief_news: BriefNews):
    response = chat_qwen().complete(
        prompt.PROMPT_NEWS_SUMMARIZE.format(length=39, title=brief_news.title, content=brief_news.content))
    return response.text


def add_history(brief_news: BriefNews):
    his_news: HistoryNews = HistoryNews(title=brief_news.title, type='daily', pub_time='', content='')
    globle_db.add(his_news)


def is_published(brief_news: BriefNews):
    with globle_db.get_session() as session:
        his_news: HistoryNews = session.query(HistoryNews).filter(HistoryNews.type == 'daily',
                                                                  BriefNews.title == brief_news.title).limit(1).first()
        return his_news is not None


if __name__ == '__main__':
    # 定时每天7:30执行brief_news_synthesis
    # scheduler = BlockingScheduler()
    # scheduler.add_jobstore(jobstores['default'])
    # scheduler.add_job(brief_news_synthesis, CronTrigger(hour=7, minute=30), id='brief_news_synthesis',
    # replace_existing=True)
    # scheduler.start()

    brief_news_synthesis()
