from zdppy_mysql import Mysql
import time

m = Mysql(host="127.0.0.1",
          port=3306,
          user='root',
          password='root',
          db='test', )


def executemany():
    # 批量插入
    records = [('一灰灰1 executemany', 'asdf', 0, int(time.time()), int(time.time())),
               ('一灰灰2 executemany', 'qwer', 0, int(time.time()), int(time.time()))]
    sql = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    result = m.executemany(sql, records)
    m.log.info(f"受影响的行数：{result}")


def execute():
    """
    测试执行SQL语句
    :return:
    """
    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    params = ('webmaster@python.org', 'very-secret')
    result = m.execute(sql, params)
    m.log.info(f"受影响的行数：{result}")


def executes():
    """
    测试执行SQL语句
    :return:
    """
    sql1 = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params1 = ('测试executes 111', 'qwer', 0, int(time.time()), int(time.time()))
    sql2 = "insert into user(`name`, `pwd`, `isDeleted`, `created`, `updated`) values (%s, %s, %s, %s, %s)"
    params2 = ('测试executes 222', 'qwer', 0, int(time.time()), int(time.time()))
    sqls = ((sql1, params1), (sql2, params2))
    result = m.executes(sqls)
    m.log.info(f"受影响的行数：{result}")


def fetchone():
    """
    测试执行SQL语句
    :return:
    """
    sql = "select * from user where id = 3"
    result = m.fetchone(sql)
    m.log.info(f"查询单个结果：{result}")


def fetchall():
    """
    测试执行SQL语句
    :return:
    """
    sql = "select * from user"
    result = m.fetchall(sql)
    m.log.info(f"查询单个结果：{result}")


def transaction_error():
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
    result = m.executes(sqls)
    m.log.info(f"受影响的行数：{result}")


def transaction_success():
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
    result = m.executes(sqls)
    m.log.info(f"受影响的行数：{result}")


if __name__ == '__main__':
    # execute()
    # executes()
    # fetchone()
    # fetchall()
    # transaction_error()
    transaction_success()
