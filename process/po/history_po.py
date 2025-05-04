from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, BLOB
from util.storage.sqlite_sqlalchemy import Base, SQLiteDB


class HistoryNews(Base):
    __tablename__ = "t_history_news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    pub_time = Column(String, nullable=False)


if __name__ == '__main__':
    print("")
