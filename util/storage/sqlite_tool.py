import sqlite3
import threading
from queue import Queue, Empty
from settings import geoi_settings


class SQLiteConnectionPool:
    def __init__(self, db_name, pool_size=5):
        self.db_name = db_name
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()

        # 初始化连接池
        for _ in range(pool_size):
            self.pool.put(self._create_connection())

    def _create_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def get_connection(self):
        try:
            return self.pool.get_nowait()
        except Empty:
            # 如果池中没有可用连接，创建一个新连接
            return self._create_connection()

    def return_connection(self, conn):
        with self.lock:
            if self.pool.qsize() < self.pool_size:
                self.pool.put(conn)
            else:
                conn.close()

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
        finally:
            self.return_connection(conn)

    def execute_update(self, query, params=()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            self.return_connection(conn)

    def close_all_connections(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            conn.close()


global_pool = SQLiteConnectionPool(geoi_settings.DB_PATH, pool_size=5)

# 使用示例
if __name__ == "__main__":
    pool = SQLiteConnectionPool('example.db', pool_size=5)

    # 创建表
    pool.execute_update('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    # 插入数据
    pool.execute_update('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
    pool.execute_update('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))

    # 查询数据
    users = pool.execute_query('SELECT * FROM users')
    for user in users:
        print(f'ID: {user[0]}, Name: {user[1]}, Age: {user[2]}')

    # 关闭所有连接
    pool.close_all_connections()
