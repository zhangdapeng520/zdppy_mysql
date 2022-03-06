#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 13:46
# @Author  : 张大鹏
# @Site    : 
# @File    : z03_更新数据.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def update_by_id():
    columns = ["name"]
    values = ["张三三"]
    id = 118
    result = await  m.update_by_id("school", columns, values, id)
    m.log.info(result)


async def update_by_ids():
    columns = ["name"]
    values = ["张三三111"]
    ids = [111, 12, 10]
    result = await  m.update_by_ids("school", columns, values, ids)
    m.log.info(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_by_id())
    loop.run_until_complete(update_by_ids())
    loop.close()
