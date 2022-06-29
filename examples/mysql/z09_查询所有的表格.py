#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 23:16
# @Author  : 张大鹏
# @Site    : 
# @File    : z09_查询所有的表格.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")

print(m.show_tables())
