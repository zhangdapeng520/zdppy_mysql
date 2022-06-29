#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 23:26
# @Author  : 张大鹏
# @Site    : 
# @File    : practice01.py
# @Software: PyCharm
from zdppy_mysql import Mysql
import json

m = Mysql(db="test")

# 查询在 SC 表存在成绩的学生信息
sql = """
select DISTINCT student.*
from student , sc
where student.SId=sc.SId
"""

print(m.fetchall(sql))
print(m.fetchall(sql, to_json=True))
print("--------------------------------")
