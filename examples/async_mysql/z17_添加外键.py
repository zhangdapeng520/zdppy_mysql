#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 23:14
# @Author  : 张大鹏
# @Site    : 
# @File    : z17_添加外键.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import AsyncMysql

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def add_foreign_key():
    # 创建表格
    school_columns = [
        "name varchar(24)",
    ]
    student_columns = [
        "name varchar(24)",
        "age smallint",
        "school_id bigint"
    ]
    result = await m.create_table("school", columns=school_columns)
    m.log.info(result)
    m.log.info(await m.show_tables())

    result = await m.create_table("student", columns=student_columns)
    m.log.info(result)
    m.log.info(await m.show_tables())

    # 添加外键
    m.log.info(await m.add_foreign_key("student", "school_id", "school"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_foreign_key())
    loop.close()
