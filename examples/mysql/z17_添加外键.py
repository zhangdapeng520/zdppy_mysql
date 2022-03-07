#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 23:05
# @Author  : 张大鹏
# @Site    : 
# @File    : z17_添加外键.py
# @Software: PyCharm
from zdppy_mysql import Mysql

m = Mysql(db="test")

# 创建表格
school_columns = [
    "name varchar(24)",
]
student_columns = [
    "name varchar(24)",
    "age smallint",
    "school_id bigint"
]
result = m.create_table("school", columns=school_columns)
m.log.info(result)
m.log.info(m.show_tables())

result = m.create_table("student", columns=student_columns)
m.log.info(result)
m.log.info(m.show_tables())

# 添加外键
m.log.info(m.add_foreign_key("student", "school_id", "school"))
