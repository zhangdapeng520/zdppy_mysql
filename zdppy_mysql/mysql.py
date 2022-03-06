from zdppy_log import Log
from .libs import aiomysql
import asyncio
import time
from .exceptions import ConnectError
from typing import Tuple, Any, List, Union
from .libs import pymysql
from .sql import get_add_sql, get_add_many_sql, get_sql_delete_by_id, get_sql_delete_by_ids, get_sql_update_by_id, \
    get_sql_update_by_ids, get_sql_find_by_id, get_sql_find_by_ids, get_sql_find_by_page


class Mysql:
    """
    同步的MySQL
    """

    def __init__(self,
                 log_file_path: str = "logs/zdppy/zdopy_async_mysql.log",
                 host: str = "127.0.0.1",
                 port: int = 3306,
                 user: str = 'root',
                 password: str = 'root',
                 db: str = 'test',
                 charset: str = 'utf8'
                 ):
        # 初始化日志
        self.log = Log(log_file_path)

        # 初始化连接
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    def get_connection(self):
        """
        初始化，获取数据库连接池
        :return:
        """

        try:
            self.log.info("开始连接MySQL数据库")
            conn = pymysql.connect(host=self.host,
                                   port=self.port,
                                   user=self.user,
                                   password=self.password,
                                   db=self.db,
                                   charset=self.charset,
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
            self.log.info("连接MySQL数据库成功")
            return conn
        except Exception as e:
            self.log.error(f"mysql数据库连接失败：{e}")
            return False

    def executemany(self, sql, values):
        """
        执行批量插入
        :param sql:
        :param values:
        :return:
        """
        # 获取数据库连接对象
        conn = self.get_connection()

        # 从连接池获取连接
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
                cur.executemany(sql, values)
                conn.commit()

                # 获取结果
                result = cur.rowcount

                # 释放连接
                conn.close()
                cur.close()

                # 返回结果
                return result

    def execute(self, sql, params):
        """
        执行SQL语句
        :param sql:
        :param params:
        :return:
        """

        # 获取数据库连接对象
        conn = self.get_connection()

        # 从连接池获取连接
        result = 0
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
                self.log.info(f"execute执行SQL语句：sql={sql} params={params}")
                cur.execute(sql, params)
                result = cur.rowcount
            conn.commit()
        return result

    def executes(self, sqls):
        """
        执行SQL语句
        :param sqls:
        :return:
        """

        # 获取数据库连接对象
        conn = self.get_connection()

        # 受影响的函数
        count = 0

        # 从连接池获取连接
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
                for sql in sqls:
                    try:
                        self.log.info(f"execute执行SQL语句：sql={sql[0]}, params={sql[1]}")
                        cur.execute(sql[0], sql[1])
                    except Exception as e:
                        conn.rollback()
                        count = 0
                        self.log.error(f"执行SQL语句{sql[0]}失败，事务回滚：{e}")
                    count += cur.rowcount
            conn.commit()

        # 返回sql执行后影响的行数
        return count

    def fetchone(self, sql: str, args: Tuple = None):
        """
        执行SQL语句
        :param sql:
        :param args:
        :return:
        """

        # 获取数据库连接对象
        conn = self.get_connection()

        # 从连接池获取连接
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
                # 执行sql语句
                cur.execute(sql, args)

                # 获取查询结果
                result = cur.fetchone()

            # 提交事务
            conn.commit()

        # 返回查询结果
        return result

    def fetchall(self, sql: str, args: Tuple = None):
        """
        执行SQL语句
        :param sql:
        :param args:
        :return:
        """

        # 获取数据库连接对象
        conn = self.get_connection()

        # 从连接池获取连接
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
                # 执行sql语句
                cur.execute(sql, args)

                # 获取查询结果
                result = cur.fetchall()

            # 提交事务
            conn.commit()

        # 返回查询结果
        return result

    def add(self, table, columns, values):
        """
        增加数据
        :return:
        """
        sql = get_add_sql(table, columns)
        print(sql)
        return self.execute(sql, values)

    def add_many(self, table: str, columns: List[str], values: List[List]):
        """
        批量增加数据
        :return:
        """
        sql = get_add_many_sql(table, columns, len(values))
        values = tuple((i for k in values for i in k))  # 将参数展开为一维的元组
        return self.execute(sql, values)

    def delete_by_id(self, table: str, id: int):
        """
        根据id删除数据
        :return:
        """
        sql = get_sql_delete_by_id(table)
        return self.execute(sql, (id,))

    def delete_by_ids(self, table: str, ids: Tuple):
        """
        根据id列表删除
        :return:
        """
        sql = get_sql_delete_by_ids(table, len(ids))
        return self.execute(sql, ids)

    def update_by_id(self, table: str, columns: List[str], values: List[Any], id: int):
        """
        根据id修改数据
        :return:
        """
        sql = get_sql_update_by_id(table, columns)
        values.append(id)
        return self.execute(sql, tuple(values))

    def update_by_ids(self, table: str, columns: List[str], values: List[Any], ids: List[int]):
        """
        根据id列表修改数据
        :return:
        """
        sql = get_sql_update_by_ids(table, columns, len(ids))
        values.extend(ids)
        return self.execute(sql, tuple(values))

    def find_by_id(self, table: str, columns: Union[List[str], None], id: int):
        """
        根据id查询数据
        :return:
        """
        sql = get_sql_find_by_id(table, columns)
        return self.fetchone(sql, (id,))

    def find_by_ids(self, table: str, columns: Union[List[str], None], ids: Tuple):
        """
        根据id列表查询数据
        :return:
        """
        sql = get_sql_find_by_ids(table, columns, len(ids))
        return self.fetchall(sql, ids)

    def find_by_page(self, table: str, columns: Union[List[str], None],
                     page: int = 1,
                     size: int = 20,
                     asc_columns: List[str] = None,
                     desc_columns: List[str] = None):
        """
        根据分页查询数据
        :return:
        """
        sql = get_sql_find_by_page(table, columns, page, size, asc_columns, desc_columns)
        return self.fetchall(sql)
