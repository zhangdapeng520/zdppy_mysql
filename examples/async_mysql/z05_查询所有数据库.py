#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 18:19
# @Author  : 张大鹏
# @Site    : 
# @File    : z05_查询所有数据库.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def show_databases():
    result = await  m.show_databases()
    m.log.info(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(show_databases())
    loop.close()
