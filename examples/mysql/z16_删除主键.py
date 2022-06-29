#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 22:46
# @Author  : 张大鹏
# @Site    : 
# @File    : z16_删除主键.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")

# 创建表格
columns = [
    "name varchar(24)",
    "age smallint"
]
result = m.create_table("test_user", columns=columns)
print(result)
print(m.show_tables())

# 添加主键
print(m.delete_primary_key("test_user"))
