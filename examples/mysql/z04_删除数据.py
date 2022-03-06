#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 13:48
# @Author  : 张大鹏
# @Site    : 
# @File    : z04_删除数据.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def delete_by_id():
    result = await  m.delete_by_id("school", 1)
    m.log.info(result)


async def delete_by_ids():
    ids = (16, 17, 8, 1)
    result = await  m.delete_by_ids("school", ids)
    m.log.info(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_by_id())
    loop.run_until_complete(delete_by_id())
    loop.run_until_complete(delete_by_ids())
    loop.close()
