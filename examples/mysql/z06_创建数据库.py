#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 18:25
# @Author  : 张大鹏
# @Site    : 
# @File    : z06_创建数据库.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
m.create_database("test_db1")
m.create_database("test_db2")
m.create_database("test_db3")
print(m.show_databases())
