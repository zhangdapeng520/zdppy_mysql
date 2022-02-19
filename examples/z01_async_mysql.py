import asyncio
from zdppy_mysql import AsyncMysql
import time

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def executemany():
    # 批量插入
    records = [('一灰灰1 executemany', 'asdf', 0, int(time.time()), int(time.time())),
               ('一灰灰2 executemany', 'qwer', 0, int(time.time()), int(time.time()))]
    sql = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    result = await m.executemany(sql, records)
    m.log.info(f"受影响的行数：{result}")


async def execute():
    """
    测试执行SQL语句
    :return:
    """
    sql = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params = ('测试execute', 'qwer', 0, int(time.time()), int(time.time()))
    result = await m.execute(sql, *params)
    m.log.info(f"受影响的行数：{result}")


async def executes():
    """
    测试执行SQL语句
    :return:
    """
    sql1 = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params1 = ('测试executes 111', 'qwer', 0, int(time.time()), int(time.time()))
    sql2 = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params2 = ('测试executes 222', 'qwer', 0, int(time.time()), int(time.time()))
    sqls = ((sql1, params1), (sql2, params2))
    result = await m.executes(sqls)
    m.log.info(f"受影响的行数：{result}")


async def fetchone():
    """
    测试执行SQL语句
    :return:
    """
    sql = "select * from user where id = 3"
    result = await m.fetchone(sql)
    m.log.info(f"查询单个结果：{result}")


async def fetchall():
    """
    测试执行SQL语句
    :return:
    """
    sql = "select * from user"
    result = await m.fetchall(sql)
    m.log.info(f"查询单个结果：{result}")


async def transaction_error():
    """
    测试事务
    :return:
    """
    # 成功SQL
    sql1 = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params1 = ('transaction 111', 'qwer', 0, int(time.time()), int(time.time()))

    # 失败SQL
    sql2 = "insert into user(`name1`, `pwd2`, `isDeleted3`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params2 = ('transaction 222', 'qwer', 0, int(time.time()), int(time.time()))

    # 执行SQL
    sqls = ((sql1, params1), (sql2, params2))
    result = await m.executes(sqls)
    m.log.info(f"受影响的行数：{result}")


async def transaction_success():
    """
    测试事务
    :return:
    """
    # 成功SQL
    sql1 = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params1 = ('transaction 111', 'qwer', 0, int(time.time()), int(time.time()))

    # 失败SQL
    sql2 = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params2 = ('transaction 222', 'qwer', 0, int(time.time()), int(time.time()))

    # 执行SQL
    sqls = ((sql1, params1), (sql2, params2))
    result = await m.executes(sqls)
    m.log.info(f"受影响的行数：{result}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(executemany())
    # loop.run_until_complete(execute())
    # loop.run_until_complete(executes())
    # loop.run_until_complete(fetchone())
    # loop.run_until_complete(fetchall())
    # loop.run_until_complete(transaction_error())
    loop.run_until_complete(transaction_success())
    loop.close()
