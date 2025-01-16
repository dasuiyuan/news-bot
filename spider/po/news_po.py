from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text
from util.storage.sqlite_sqlalchemy import Base, SQLiteDB


class BriefNews(Base):
    __tablename__ = "t_brief_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    web_site = Column(String, nullable=True)
    type = Column(String, nullable=False)
    popularity = Column(Integer, nullable=True)
    source = Column(String, nullable=True)
    url = Column(String, nullable=True)
    time = Column(BigInteger, nullable=False)
    create_time = Column(BigInteger, nullable=False)


if __name__ == '__main__':
    print("")
