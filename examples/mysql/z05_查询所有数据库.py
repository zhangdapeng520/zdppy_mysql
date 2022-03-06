#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 18:12
# @Author  : 张大鹏
# @Site    : 
# @File    : z05_查询所有数据库.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
print(m.show_databases())
