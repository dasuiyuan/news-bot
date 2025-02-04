from test.process import init_env

init_env()
import os
from datetime import datetime
from process import image_generate
from spider.po.news_po import BriefNews
from util.storage.sqlite_sqlalchemy import globle_db


def test_generate_news_title():
    with globle_db.get_session() as session:
        briefs = session.query(BriefNews).filter(BriefNews.type not in ['其他类']).limit(5).all()
        image_generate.generate_news_title(briefs)


def test_generate_news_content():
    with globle_db.get_session() as session:
        brief = session.query(BriefNews).filter(BriefNews.image.isnot(None)).limit(1).first()
        image_generate.generate_news_content(brief)


if __name__ == '__main__':
    img_folder = img_path = os.path.join(os.environ.get("NEWS_BOT_ROOT"), "data", "image",
                                         datetime.now().strftime("%Y-%m-%d"))
    # image_generate.generate_cover()
    # test_generate_news_title()
    test_generate_news_content()
