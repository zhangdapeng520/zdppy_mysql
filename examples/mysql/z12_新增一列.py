#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:20
# @Author  : 张大鹏
# @Site    : 
# @File    : z12_新增一列.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")
m.log.info(m.show_tables())
m.log.info(m.add_column("school", "address", "varchar(22)"))
m.log.info(m.show_tables())
