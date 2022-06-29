#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 11:13
# @Author  : 张大鹏
# @Site    : 
# @File    : z02_查询数据.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(host="127.0.0.1",
          port=3306,
          user='root',
          password='root',
          db='test', )


def find_by_id():
    columns = ["name"]
    id = 10
    result = m.find_by_id("school", columns, id)
    print(result)
    result = m.find_by_id("school", None, id)
    print(result)


def find_by_ids():
    columns = ["name"]
    ids = (10, 11, 12)
    result = m.find_by_ids("school", columns, ids)
    print(result)
    result = m.find_by_ids("school", None, ids)
    print(result)


def find_by_page():
    columns = ["name"]
    result = m.find_by_page("school", columns, asc_columns=["id"])
    print(result)
    result = m.find_by_page("school", None, desc_columns=["id"])
    print(result)


def find_all():
    columns = ["name"]
    result = m.find_all("school", columns)
    print(result)
    result = m.find_all("school", None)
    print(result)


if __name__ == '__main__':
    find_by_id()
    find_by_ids()
    find_by_page()
    find_all()
