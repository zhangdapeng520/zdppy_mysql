#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 21:00
# @Author  : 张大鹏
# @Site    : 
# @File    : z06_创建数据库.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def create_database():
    await m.create_database("test_db1")
    await m.create_database("test_db2")
    await m.create_database("test_db3")
    print(await m.show_databases())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database())
    loop.close()
