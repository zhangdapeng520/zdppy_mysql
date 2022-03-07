#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:14
# @Author  : 张大鹏
# @Site    : 
# @File    : z11_重命名表格.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
m.log.info(m.show_tables())
m.log.info(m.rename_table("school", "school1"))
m.log.info(m.show_tables())
