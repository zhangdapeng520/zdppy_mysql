import json

from typing import Tuple, Any, List, Union

import zdppy_mysql
from .sql import (
    get_add_sql, get_add_many_sql, get_sql_delete_by_id,
    get_sql_delete_by_ids, get_sql_update_by_id, get_sql_update_by_ids,
    get_sql_find_by_id, get_sql_find_by_ids, get_sql_find_by_page,
    get_create_table_sql, get_sql_find_column_in, get_sql_find_all)
from .json_encoder import JsonEncoder


class Mysql:
    """
    同步的MySQL
    """

    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 3306,
                 user: str = 'root',
                 password: str = 'root',
                 db: str = 'test',
                 charset: str = 'utf8'
                 ):

        # 初始化连接
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = db
        self.charset = charset

        # 数据库列表 {数据库名：是否存在}
        self.__databases = {}

        # 表格列表 {表格名：是否存在}
        self.__tables = {}

    def get_connection(self):
        """
        初始化，获取数据库连接池
        :return:
        """

        try:
            conn = zdppy_mysql.connect(host=self.host,
                                       port=self.port,
                                       user=self.user,
                                       password=self.password,
                                       db=self.database,
                                       charset=self.charset,
                                       cursorclass=zdppy_mysql.cursors.DictCursor
                                       )
            return conn
        except Exception as e:
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

    def execute(self, sql: str, params: Any = None):
        """
        执行SQL语句
        :param sql: 要执行的SQL语句
        :param params: 要传进来的参数
        :return:
        """

        # 获取数据库连接对象
        conn = self.get_connection()

        # 从连接池获取连接
        result = 0
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
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
                        cur.execute(sql[0], sql[1])
                    except Exception as e:
                        conn.rollback()
                        count = 0
                    count += cur.rowcount
            conn.commit()

        # 返回sql执行后影响的行数
        return count

    def fetchone(self, sql: str, args: Tuple = None, to_json=False):
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

        # 转换json数据
        if to_json:
            result = json.dumps(result, cls=JsonEncoder, ensure_ascii=False)

        # 返回查询结果
        return result

    def fetchall(self, sql: str, args: Tuple = None, to_json: bool = False):
        """
        执行SQL语句
        :param sql:
        :param args:
        :param to_json: 是否转换为json数据
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

        # 转换json数据
        if to_json:
            result = json.dumps(result, cls=JsonEncoder, ensure_ascii=False)

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

    def find_by_page(self,
                     table: str,
                     columns: Union[List[str], None],
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

    def find_all(self,
                 table: str,
                 columns: Union[List[str], None],
                 ):
        """
        查询所有
        :param table 表格名
        :param columns 字段列表
        :return:
        """
        sql = get_sql_find_all(table, columns)
        return self.fetchall(sql)

    def show_databases(self):
        """
        查看所有的数据库
        :return:
        """
        sql = "show databases;"
        # 获取数据库连接对象
        conn = self.get_connection()

        # 从连接池获取连接
        result = None
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()

                # 提取数据库名
                if result is not None and isinstance(result, list):
                    result = [database.get("Database") for database in result]

                    # 生成字典
                    flags = [True for _ in result]
                    temp_dict = dict(zip(result, flags))

                    # 更新字典
                    self.__databases.update(temp_dict)

            conn.commit()
        return result

    def create_database(self, database_name: str):
        """
        创建数据库
        :return:
        """
        # 查看数据库
        if self.__databases is None or len(self.__databases) == 0:
            self.show_databases()

        # 创建数据库
        if not self.__databases.get(database_name):
            sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
            result = self.execute(sql)
            return result

    def delete_database(self, database_name: str):
        """
        删除数据库
        :return:
        """
        # 查看数据库
        if self.__databases is None or len(self.__databases) == 0:
            self.show_databases()

        # 删除数据库
        if self.__databases.get(database_name):
            sql = f"DROP DATABASE IF EXISTS {database_name};"
            result = self.execute(sql)
            del self.__databases[database_name]
            return result

    def create_table(self,
                     table: str,
                     id_column=None,
                     columns: List = None,
                     open_engine=True,
                     open_common: bool = True
                     ):
        """
        创建表格
        :param open_common 是否开启公共字段
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 创建表格
        if not self.__tables.get(table):
            # 获取创建表格的SQL语句
            s = get_create_table_sql(
                table,
                id_column,
                columns,
                open_engine,
                open_common,
            )

            # 创建表格
            result = self.execute(s)

            # 返回结果
            return result

    def show_tables(self):
        """
        查看所有的表格
        :return:
        """
        sql = "show tables;"

        # 获取数据库连接对象
        conn = self.get_connection()

        # 从连接池获取连接
        result = None
        with conn:
            # 执行SQL语句
            with conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()

                # 提取表格名
                if result is not None and isinstance(result, list):
                    result = [table.get(f"Tables_in_{self.database}") for table in result]

                    # 生成字典
                    flags = [True for _ in result]
                    temp_dict = dict(zip(result, flags))

                    # 更新字典
                    self.__tables.update(temp_dict)

            conn.commit()
        return result

    def delete_table(self, table: str):
        """
        删除表格
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"drop table if exists {table};"

        # 创建表格
        if self.__tables.get(table):
            # 删除表格
            result = self.execute(s)
            del self.__tables[table]

            # 返回结果
            return result

    def rename_table(self, table: str, new_table: str):
        """
        重命名表格
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} rename to {new_table};"

        # 重命名表格
        if self.__tables.get(table):
            # 重命名表格
            result = self.execute(s)
            del self.__tables[table]
            self.__tables[new_table] = True

            # 返回结果
            return result

    def add_column(self, table: str, column: str, ctype: str):
        """
        修改表格，新增一列
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} add column {column} {ctype};"

        # 修改表格
        if self.__tables.get(table):
            # 修改表格
            result = self.execute(s)

            # 返回结果
            return result

    def delete_column(self, table: str, column: str):
        """
        修改表格，删除一列
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} drop column {column};"

        # 修改表格
        if self.__tables.get(table):
            # 修改表格
            result = self.execute(s)

            # 返回结果
            return result

    def update_column(self, table: str, column: str, new_column: str, new_column_type: str):
        """
        修改表格，修改一列
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} change column {column} {new_column} {new_column_type};"

        # 修改表格
        if self.__tables.get(table):
            # 修改表格
            result = self.execute(s)

            # 返回结果
            return result

    def add_primary_key(self, table: str, column: str):
        """
        修改表格，添加主键
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} add primary key ({column});"

        # 修改表格
        if self.__tables.get(table):
            # 修改表格
            result = self.execute(s)

            # 返回结果
            return result

    def delete_primary_key(self, table: str):
        """
        修改表格，删除主键
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} drop primary key;"

        # 修改表格
        if self.__tables.get(table):
            # 修改表格
            result = self.execute(s)

            # 返回结果
            return result

    def add_foreign_key(self, table: str,
                        foreign_key_column: str,
                        reference_table: str,
                        reference_primary_key: str = "id",
                        foreign_key_name: str = None,
                        ):
        """
        修改表格，添加外键
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        if foreign_key_name is None:
            foreign_key_name = f"fk_{foreign_key_column}"
        s = f"alter table {table} add constraint {foreign_key_name} foreign key({foreign_key_column}) references {reference_table}({reference_primary_key});"

        # 修改表格
        if self.__tables.get(table):
            # 修改表格
            result = self.execute(s)

            # 返回结果
            return result

    def delete_foreign_key(self, table: str, foreign_key_name: str):
        """
        修改表格，删除外键
        :return:
        """
        # 处理表格字典
        if self.__tables is None or len(self.__tables) == 0:
            self.show_tables()

        # 整理SQL语句
        s = f"alter table {table} drop foreign key {foreign_key_name};"

        # 修改表格
        if self.__tables.get(table):
            # 修改表格
            result = self.execute(s)

            # 返回结果
            return result

    def find_column_in(self, table: str,
                       column: str = None,
                       values: Tuple = None,
                       to_json: bool = False,
                       show_columns: List = None,
                       ):
        """
        根据指定字段执行in查询
        :param table:
        :param show_columns:
        :param column:
        :param values:
        :param to_json:
        :return:
        """
        sql = get_sql_find_column_in(table, show_columns, column, len(values))
        return self.fetchall(sql, values, to_json=to_json)
