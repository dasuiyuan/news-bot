from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Type, List, Optional, Dict, Any
from settings import geoi_settings

Base = declarative_base()


class SQLiteDB:
    def __init__(self, db_url: str = "sqlite:///example.db"):
        """
        初始化 SQLite 数据库工具类
        :param db_url: SQLite 数据库连接 URL
        """
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        """
        创建所有定义的表
        """
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """
        删除所有定义的表
        """
        Base.metadata.drop_all(self.engine)

    def get_engine(self) -> create_engine:
        """
        获取数据库引擎
        :return: SQLAlchemy Engine 实例
        """
        return self.engine

    def get_session(self) -> Session:
        """
        获取数据库会话
        :return: SQLAlchemy Session 实例
        """
        return self.SessionLocal()

    def add(self, obj: Base) -> None:
        """
        添加一条记录
        :param obj: 数据库模型实例
        """
        with self.get_session() as session:
            session.add(obj)
            session.commit()

    def add_all(self, objs: List[Base]) -> None:
        """
        批量添加记录
        :param objs: 数据库模型实例列表
        """
        with self.get_session() as session:
            session.add_all(objs)
            session.commit()

    def get(self, model: Type[Base], obj_id: int) -> Optional[Base]:
        """
        根据 ID 获取一条记录
        :param model: 数据库模型类
        :param obj_id: 主键 ID
        :return: 查询到的记录或 None
        """
        with self.get_session() as session:
            return session.query(model).get(obj_id)

    def get_all(self, model: Type[Base]) -> List[Base]:
        """
        获取所有记录
        :param model: 数据库模型类
        :return: 所有记录的列表
        """
        with self.get_session() as session:
            return session.query(model).all()

    def update(self, model: Type[Base], obj_id: int, updates: Dict[str, Any]) -> Optional[Base]:
        """
        更新一条记录
        :param model: 数据库模型类
        :param obj_id: 主键 ID
        :param updates: 要更新的字段和值
        :return: 更新后的记录或 None
        """
        with self.get_session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                for key, value in updates.items():
                    setattr(obj, key, value)
                session.commit()
                session.refresh(obj)
            return obj

    def delete(self, model: Type[Base], obj_id: int) -> None:
        """
        删除一条记录
        :param model: 数据库模型类
        :param obj_id: 主键 ID
        """
        with self.get_session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                session.delete(obj)
                session.commit()


globle_db = SQLiteDB(f"sqlite:///{geoi_settings.DB_PATH}")
