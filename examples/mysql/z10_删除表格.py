#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 23:35
# @Author  : 张大鹏
# @Site    : 
# @File    : z10_删除表格.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
print(m.show_tables())
print(m.delete_table("test_user"))
print(m.show_tables())
