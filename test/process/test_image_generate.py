from process import image_generate
from spider.po.news_po import BriefNews
from . import init_env

init_env()
from util.storage.sqlite_sqlalchemy import globle_db


def test_generate_news_title():
    with globle_db.get_session() as session:
        briefs = session.query(BriefNews).limit(5).all()
        for brief in briefs:
            image_generate.generate_news_title(brief)


if __name__ == '__main__':
    test_generate_news_title()
