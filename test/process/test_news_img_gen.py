from util.llm_util import img_gen
from process.prompt import PROMPT_NEWS_IMAGE_GENERATE
from util.storage.sqlite_sqlalchemy import SQLiteDB
from spider.po.news_po import BriefNews

if __name__ == '__main__':
    db = SQLiteDB(f"sqlite:///D:\\3-code\mini\\news-bot\data\\news_bot.db")
    with db.get_session() as session:
        news = session.query(BriefNews).filter(
            BriefNews.type.in_(['AI技术类', 'AI产品类'])).limit(1).first()

    prompt = PROMPT_NEWS_IMAGE_GENERATE.format(title=news.title, content=news.content)
    url = img_gen(prompt=prompt, save_path="D:\\3-code\mini\\news-bot\\data\\tmp\\news_img.jpg")
    print(url)
