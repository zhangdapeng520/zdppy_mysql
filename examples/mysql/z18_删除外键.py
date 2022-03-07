#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 23:08
# @Author  : 张大鹏
# @Site    : 
# @File    : z18_删除外键.py
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
# 删除表
m.log.info(m.delete_table("student"))
m.log.info(m.delete_table("school"))

# 创建表
result = m.create_table("school", columns=school_columns)
m.log.info(result)
m.log.info(m.show_tables())

result = m.create_table("student", columns=student_columns)
m.log.info(result)
m.log.info(m.show_tables())

# 添加外键
m.log.info(m.add_foreign_key("student", "school_id", "school"))

# 删除外键
m.log.info(m.delete_foreign_key("student", "fk_school_id"))

# 删除表不再受外键约束
m.log.info(m.delete_table("school"))
m.log.info(m.delete_table("student"))
