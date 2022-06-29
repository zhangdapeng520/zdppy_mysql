#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 11:12
# @Author  : 张大鹏
# @Site    : 
# @File    : z01_添加数据.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(host="127.0.0.1",
          port=3306,
          user='root',
          password='root',
          db='test', )


def create_table():
    # 创建表格
    columns = [
        "name varchar(24)",
    ]
    result = m.create_table("school", columns=columns)
    print(result)


def school_add():
    result = m.add("school", ["name"], ["北京大学"])
    print(result)


def school_add_many():
    data = [
        [{f"北京大学{i}"}]
        for i in range(100)
    ]
    result = m.add_many("school", ["name"], data)
    print(result)


if __name__ == '__main__':
    create_table()
    school_add()
    school_add_many()
