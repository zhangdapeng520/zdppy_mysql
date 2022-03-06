#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 11:12
# @Author  : 张大鹏
# @Site    : 
# @File    : z01_添加数据.py
# @Software: PyCharm
import asyncio
from zdppy_mysql import Mysql

m = Mysql(host="127.0.0.1",
          port=3306,
          user='root',
          password='root',
          db='test', )


def school_add():
    result = m.add("school", ["name"], ["北京大学"])
    m.log.info(result)


def school_add_many():
    data = [
        [{f"北京大学{i}"}]
        for i in range(100)
    ]
    result = m.add_many("school", ["name"], data)
    m.log.info(result)


if __name__ == '__main__':
    school_add()
    school_add_many()
