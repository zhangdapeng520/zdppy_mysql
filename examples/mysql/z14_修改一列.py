#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:28
# @Author  : 张大鹏
# @Site    : 
# @File    : z14_修改一列.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
print(m.show_tables())
print(m.update_column("school", "name", "name", "varchar(33)"))
print(m.show_tables())
