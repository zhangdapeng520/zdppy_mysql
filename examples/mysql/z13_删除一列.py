#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:24
# @Author  : 张大鹏
# @Site    : 
# @File    : z13_删除一列.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
m.log.info(m.show_tables())
m.log.info(m.delete_column("school", "address"))
m.log.info(m.show_tables())
