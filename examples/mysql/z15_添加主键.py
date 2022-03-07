#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:36
# @Author  : 张大鹏
# @Site    : 
# @File    : z15_添加主键.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")

# 创建表格
columns = [
    "name varchar(24)",
    "age smallint"
]
result = m.create_table("test_user", columns=columns, id_column="id bigint")
m.log.info(result)
m.log.info(m.show_tables())

# 添加主键
m.log.info(m.add_primary_key("test_user", "id"))
