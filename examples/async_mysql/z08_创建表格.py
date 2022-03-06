#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 23:29
# @Author  : 张大鹏
# @Site    : 
# @File    : z08_创建表格.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def create_table():
    m.log.info(await m.show_tables())
    columns = [
        "name varchar(22)",
        "age int"
    ]
    await m.create_table("test_user1", columns=columns)
    m.log.info(await m.show_tables())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_table())
    loop.close()
