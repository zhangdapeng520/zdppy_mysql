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

#  查询没学过"张三"老师讲授的任一门课程的学生姓名
sql = """
select *
from student 
where student.SId not in 
(
select student.SId
from student left join sc on student.SId=sc.SId 
where EXISTS 
(select *
from teacher ,course
where teacher.Tname='张三'
and   teacher.TId=course.TId
and 	course.CId=sc.CId))
"""

print(m.fetchall(sql))
print(m.fetchall(sql, to_json=True))
print("--------------------------------")
