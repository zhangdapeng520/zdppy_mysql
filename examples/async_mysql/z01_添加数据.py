#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 11:12
# @Author  : 张大鹏
# @Site    : 
# @File    : z01_添加数据.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql
import time

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def school_add():
    result = await  m.add("school", ["name"], ["北京大学"])
    m.log.info(result)


async def school_add_many():
    data = [
        [{f"北京大学{i}"}]
        for i in range(100)
    ]
    result = await  m.add_many("school", ["name"], data)
    m.log.info(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(school_add())
    loop.run_until_complete(school_add_many())
    loop.close()
