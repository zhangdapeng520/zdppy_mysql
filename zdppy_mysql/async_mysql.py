#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 7:32
# @Author  : 张大鹏
# @Site    : 
# @File    : async_mysql.py
# @Software: PyCharm
from zdppy_log import Log
from .libs import aiomysql
import asyncio
from .exceptions import ConnectError, ParamError
from typing import Tuple, Any, List, Union
from .sql import (
    get_add_sql, get_add_many_sql, get_sql_delete_by_id,
    get_sql_delete_by_ids, get_sql_update_by_id, get_sql_update_by_ids,
    get_sql_find_by_id, get_sql_find_by_ids, get_sql_find_by_page,
    get_create_table_sql)


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

        # 数据库：{数据库名：是否存在}
        self.__databases = {}

        # 表格：{表格名：是否存在}
        self.__tables = {}

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

    async def execute(self, sql, params=None):
        """
        执行SQL语句
        :param sql:要执行的SQL语句
        :param params:要传入的参数
        :return:
        """

        # 获取数据库连接对象
        if self.pool is None or self.pool is False:
            self.pool = await self.get_pool()

        # 从连接池获取连接
        async with self.pool.acquire() as conn:
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
        if self.pool is None or self.pool is False:
            self.pool = await self.get_pool()

        # 从连接池获取连接
        async with self.pool.acquire() as conn:
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
        if self.pool is None or self.pool is False:
            self.pool = await self.get_pool()
            self.log.info(f"初始化数据库连接池成功：{self.pool}")

        # 从连接池获取连接
        async with self.pool.acquire() as conn:
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

    async def add(self, table, columns, values):
        """
        增加数据
        :return:
        """
        sql = get_add_sql(table, columns)
        return await self.execute(sql, values)

    async def add_many(self, table: str, columns: List[str], values: List[List]):
        """
        批量增加数据
        :return:
        """
        sql = get_add_many_sql(table, columns, len(values))
        values = tuple((i for k in values for i in k))  # 将参数展开为一维的元组
        return await self.execute(sql, values)

    async def delete_by_id(self, table: str, id: int):
        """
        根据id删除数据
        :return:
        """
        sql = get_sql_delete_by_id(table)
        return await self.execute(sql, (id,))

    async def delete_by_ids(self, table: str, ids: Tuple):
        """
        根据id列表删除
        :return:
        """
        sql = get_sql_delete_by_ids(table, len(ids))
        return await self.execute(sql, ids)

    async def update_by_id(self, table: str, columns: List[str], values: List[Any], id: int):
        """
        根据id修改数据
        :return:
        """
        sql = get_sql_update_by_id(table, columns)
        values.append(id)
        return await self.execute(sql, tuple(values))

    async def update_by_ids(self, table: str, columns: List[str], values: List[Any], ids: List[int]):
        """
        根据id列表修改数据
        :return:
        """
        sql = get_sql_update_by_ids(table, columns, len(ids))
        values.extend(ids)
        return await self.execute(sql, tuple(values))

    async def find_by_id(self, table: str, columns: Union[List[str], None], id: int):
        """
        根据id查询数据
        :return:
        """
        sql = get_sql_find_by_id(table, columns)
        return await self.fetchone(sql, (id,))

    async def find_by_ids(self, table: str, columns: Union[List[str], None], ids: Tuple):
        """
        根据id列表查询数据
        :return:
        """
        sql = get_sql_find_by_ids(table, columns, len(ids))
        return await self.fetchall(sql, ids)

    async def find_by_page(self, table: str, columns: Union[List[str], None],
                           page: int = 1,
                           size: int = 20,
                           asc_columns: List[str] = None,
                           desc_columns: List[str] = None):
        """
        根据分页查询数据
        :return:
        """
        sql = get_sql_find_by_page(table, columns, page, size, asc_columns, desc_columns)
        return await self.fetchall(sql)

    async def tuple1_to_dict(self, columns: List[str] = None, result: Tuple = None):
        # 校验参数
        if columns is None or len(columns) == 0:
            raise ParamError("columns不能为空")
        if result is None or len(result) == 0:
            raise ParamError("result不能为空")
        if len(columns) != len(result):
            raise ParamError(f"参数长度不一致 columns={len(columns)} result={len(result)}")

        # 封装结果
        d = {}
        for i in range(len(columns)):
            print(columns[i], result[i])
            d[columns[i]] = result[i]
        return d

    async def tuple2_to_dict(self, columns: List[str], result: Tuple):
        # 校验参数
        if columns is None:
            raise ParamError("columns不能None")
        if len(columns) == 0:
            raise ParamError("columns不能为空")
        if len(result) == 0:
            raise ParamError("result不能为空")
        if len(columns) != len(result[0]):
            raise ParamError(f"参数长度不一致 columns={len(columns)} result={len(result[0])}")

        # 封装结果
        results = []
        for r in result:
            d = {}
            for i in range(len(columns)):
                d[columns[i]] = r[i]
            results.append(d)
        return results

    async def show_databases(self):
        """
        查看所有的数据库
        :return:
        """
        sql = "show databases;"
        # 获取数据库连接对象
        if self.pool is None or self.pool is False:
            self.pool = await self.get_pool()

        # 准备响应数据
        result = None

        # 从连接池获取连接
        async with self.pool.acquire() as conn:
            # 执行SQL语句
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()

                # 释放连接
                conn.close()

                # 处理结果
                result = await cur.fetchall()
                if result is not None:
                    result = [database[0] for database in result]

                    # 生成字典
                    flags = [True for _ in result]
                    temp_dict = dict(zip(result, flags))
                    self.log.debug(f"数据库字典：{temp_dict}")

                    # 更新字典
                    self.__databases.update(temp_dict)
        return result

    async def create_database(self, database_name: str):
        """
        创建数据库
        :return:
        """
        # 查看数据库
        if self.__databases is None or len(self.__databases) == 0:
            await self.show_databases()

        # 创建数据库
        if not self.__databases.get(database_name):
            sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
            result = self.execute(sql)
            return result

    async def delete_database(self, database_name: str):
        """
        删除数据库
        :return:
        """
        # 查看数据库
        if self.__databases is None or len(self.__databases) == 0:
            await self.show_databases()

        # 删除数据库
        if self.__databases.get(database_name):
            sql = f"DROP DATABASE IF EXISTS {database_name};"
            result = await self.execute(sql)
            del self.__databases[database_name]
            return result

    async def create_table(self, table: str, id_column=None, columns: List = None, open_engine=True):
        """
        创建表格
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            await self.show_tables()

        # 创建表格
        if not self.__tables.get(table):
            # 获取创建表格的SQL语句
            s = get_create_table_sql(table, id_column, columns, open_engine)
            self.log.debug(f"创建表格的SQL语句：{s}")

            # 创建表格
            result = await self.execute(s)

            # 返回结果
            return result

    async def show_tables(self):
        """
        查看所有的表格
        :return:
        """
        sql = "show tables;"

        # 获取数据库连接对象
        if self.pool is None or self.pool is False:
            self.pool = await self.get_pool()

        # 准备响应数据
        result = None

        # 从连接池获取连接
        async with self.pool.acquire() as conn:
            # 执行SQL语句
            async with conn.cursor() as cur:
                await cur.execute(sql)
                await conn.commit()

                # 释放连接
                conn.close()

                # 处理结果
                result = await cur.fetchall()
                if result is not None:
                    result = [database[0] for database in result]

                    # 生成字典
                    flags = [True for _ in result]
                    temp_dict = dict(zip(result, flags))
                    self.log.debug(f"数据库字典：{temp_dict}")

                    # 更新字典
                    self.__tables.update(temp_dict)
        return result

    async def delete_table(self, table: str):
        """
        删除表格
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            await self.show_tables()

        # 整理SQL语句
        s = f"drop table if exists {table};"

        # 创建表格
        if self.__tables.get(table):
            # 获取创建表格的SQL语句
            self.log.debug(f"删除表格的SQL语句：{s}")

            # 删除表格
            result = await self.execute(s)
            del self.__tables[table]

            # 返回结果
            return result

    async def rename_table(self, table: str, new_table: str):
        """
        重命名表格
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            await self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} rename to {new_table};"

        # 重命名表格
        if self.__tables.get(table):
            # 获取创建表格的SQL语句
            self.log.debug(f"重命名表格的SQL语句：{s}")

            # 重命名表格
            result = await self.execute(s)
            del self.__tables[table]
            self.__tables[new_table] = True

            # 返回结果
            return result

    async def add_column(self, table: str, column: str, column_type: str):
        """
        修改表格，新增一列
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            await self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} add column {column} {column_type};"

        # 修改表格
        if self.__tables.get(table):
            # 获取创建表格的SQL语句
            self.log.debug(f"修改表格的SQL语句：{s}")

            # 修改表格
            result = await self.execute(s)

            # 返回结果
            return result

    async def delete_column(self, table: str, column: str):
        """
        修改表格，删除一列
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            await self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} drop column {column};"

        # 修改表格
        if self.__tables.get(table):
            # 获取创建表格的SQL语句
            self.log.debug(f"修改表格的SQL语句：{s}")

            # 修改表格
            result = await self.execute(s)

            # 返回结果
            return result

    async def update_column(self, table: str, column: str, new_column: str, new_column_type: str):
        """
        修改表格，修改一列
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            await self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} change column {column} {new_column} {new_column_type};"

        # 修改表格
        if self.__tables.get(table):
            # 获取创建表格的SQL语句
            self.log.debug(f"修改表格的SQL语句：{s}")

            # 修改表格
            result = await self.execute(s)

            # 返回结果
            return result
