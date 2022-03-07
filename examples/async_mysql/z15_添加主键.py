#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:54
# @Author  : 张大鹏
# @Site    : 
# @File    : z15_添加主键.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def delete_table():
    # 创建表格
    columns = [
        "name varchar(24)",
        "age smallint"
    ]
    result = await m.create_table("test_user1", columns=columns, id_column="id bigint")
    m.log.info(result)
    m.log.info(await m.show_tables())

    # 添加主键
    m.log.info(await m.add_primary_key("test_user1", "id"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_table())
    loop.close()
