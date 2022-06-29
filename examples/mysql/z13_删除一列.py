#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:24
# @Author  : 张大鹏
# @Site    : 
# @File    : z13_删除一列.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
print(m.show_tables())
print(m.delete_column("school", "address"))
print(m.show_tables())
