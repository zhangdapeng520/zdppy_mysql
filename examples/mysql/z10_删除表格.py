#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 23:35
# @Author  : 张大鹏
# @Site    : 
# @File    : z10_删除表格.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
m.log.info(m.show_tables())
m.log.info(m.delete_table("test_user"))
m.log.info(m.show_tables())
