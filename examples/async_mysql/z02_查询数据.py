#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 11:13
# @Author  : 张大鹏
# @Site    : 
# @File    : z02_查询数据.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql
import time

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def find_by_id():
    columns = ["name"]
    id = 10
    result = await  m.find_by_id("school", columns, id)
    m.log.info(result)
    result = await m.tuple1_to_dict(columns, result)
    m.log.info(result)

    result = await  m.find_by_id("school", None, id)
    m.log.info(result)


async def find_by_ids():
    columns = ["name"]
    ids = (10, 11, 12)
    result = await  m.find_by_ids("school", columns, ids)
    m.log.info(result)
    result = await m.tuple2_to_dict(columns, result)
    m.log.info(result)

    result = await  m.find_by_ids("school", None, ids)
    m.log.info(result)


async def find_by_page():
    columns = ["name"]
    result = await  m.find_by_page("school", columns, asc_columns=["id"])
    m.log.info(result)
    result = await m.tuple2_to_dict(columns, result)
    m.log.info(result)

    result = await m.find_by_page("school", None, desc_columns=["id"])
    m.log.info(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(find_by_id())
    loop.run_until_complete(find_by_ids())
    loop.run_until_complete(find_by_page())
    loop.close()
