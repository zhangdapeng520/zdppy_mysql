from zdppy_log import Log
import aiomysql
import asyncio
import time
from .exceptions import ConnectError
from typing import Tuple, Any
import pymysql


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
                self.log.info(f"execute执行SQL语句：sql={sql}, params={params}")
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


class AsyncMysql:
    """
    异步的MySQL
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
        self.conn = None
        self.pool = None

    async def get_pool(self):
        """
        初始化，获取数据库连接池
        :return:
        """

        try:
            self.log.info("开始连接MySQL数据库")
            pool = await aiomysql.create_pool(host=self.host,
                                              port=self.port,
                                              user=self.user,
                                              password=self.password,
                                              db=self.db,
                                              charset=self.charset
                                              )
            self.log.info("连接MySQL数据库成功")
            return pool
        except asyncio.CancelledError:
            raise asyncio.CancelledError
        except Exception as ex:
            self.log.error(f"mysql数据库连接失败：{ex.args[0]}")
            return False

    async def executemany(self, sql, values):
        # 获取数据库连接对象
        pool = None
        if self.pool is None or self.pool is False:
            pool = await self.get_pool()
            self.pool = pool

        # 从连接池获取连接
        async with pool.acquire() as conn:
            # 执行SQL语句
            async with conn.cursor() as cur:
                await cur.executemany(sql, values)
                await conn.commit()

                # 获取结果
                result = cur.rowcount

                # 释放连接
                conn.close()
                await cur.close()

                # 返回结果
                return result

    async def execute(self, sql, *params):
        """
        执行SQL语句
        :param sql:
        :param params:
        :return:
        """

        # 获取数据库连接对象
        pool = None
        if self.pool is None or self.pool is False:
            pool = await self.get_pool()
            self.pool = pool

        # 从连接池获取连接
        async with pool.acquire() as conn:
            # 执行SQL语句
            async with conn.cursor() as cur:
                await cur.execute(sql, params)
                await conn.commit()

                # 释放连接
                conn.close()

                # 返回sql执行后影响的行数
                return cur.rowcount

    async def executes(self, sqls):
        """
        执行SQL语句
        :param sqls:
        :return:
        """

        # 获取数据库连接对象
        pool = None
        if self.pool is None or self.pool is False:
            pool = await self.get_pool()
            self.pool = pool

        # 受影响的函数
        count = 0

        # 从连接池获取连接
        async with pool.acquire() as conn:
            # 执行SQL语句
            async with conn.cursor() as cur:
                for sql in sqls:
                    try:
                        await cur.execute(sql[0], sql[1])
                    except Exception as e:
                        await conn.rollback()
                        count = 0
                        self.log.error(f"执行SQL语句{sql[0]}失败，事务回滚：{e}")
                    count += cur.rowcount
                await conn.commit()

                # 释放连接
                conn.close()

                # 返回sql执行后影响的行数
                return count

    async def fetchone(self, sql: str, args: Tuple = None):
        """
        执行SQL语句
        :param sql:
        :param args:
        :return:
        """

        # 获取数据库连接对象
        pool = None
        if self.pool is None or self.pool is False:
            pool = await self.get_pool()
            self.pool = pool

        # 从连接池获取连接
        async with pool.acquire() as conn:
            # 执行SQL语句
            async with conn.cursor() as cur:
                # 执行sql语句
                await cur.execute(sql, args)
                await conn.commit()

                # 获取查询结果
                result = await cur.fetchone()

                # 释放连接
                conn.close()
                await cur.close()

                # 返回查询结果
                return result

    async def fetchall(self, sql: str, args: Tuple = None):
        """
        执行SQL语句
        :param sql:
        :param args:
        :return:
        """

        # 获取数据库连接对象
        pool = None
        if self.pool is None or self.pool is False:
            pool = await self.get_pool()
            self.pool = pool

        # 从连接池获取连接
        async with pool.acquire() as conn:
            # 执行SQL语句
            async with conn.cursor() as cur:
                # 执行sql语句
                await cur.execute(sql, args)
                await conn.commit()

                # 获取查询结果
                result = await cur.fetchall()

                # 释放连接
                conn.close()
                await cur.close()

                # 返回查询结果
                return result

    async def close(self):
        if self.pool is None or self.pool is False:
            self.log.warning("pool不存在，不需要关闭")
        else:
            self.pool.close()
            await self.pool.wait_closed()
            self.log.info("连接池已关闭！")

    def __del__(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                self.log.error(e)
            finally:
                del self.conn
