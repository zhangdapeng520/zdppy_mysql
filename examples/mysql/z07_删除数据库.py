#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 22:48
# @Author  : 张大鹏
# @Site    : 
# @File    : z07_删除数据库.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
print(m.show_databases())
m.delete_database("test_db1")
m.delete_database("test_db2")
m.delete_database("test_db3")
print(m.show_databases())
