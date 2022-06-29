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

#  查询学过「张三」老师授课的同学的信息
sql = """
select 
    student.*
from 
    teacher, course, student, sc
where 
    teacher.Tname='张三'
    and   teacher.TId=course.TId
    and   course.CId=sc.CId
    and   sc.SId=student.SId
"""

print(m.fetchall(sql))
print(m.fetchall(sql, to_json=True))
print("--------------------------------")
