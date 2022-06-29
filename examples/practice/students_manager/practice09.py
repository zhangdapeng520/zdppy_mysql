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

#  查询和" 01 "号的同学学习的课程完全相同的其他同学的信息
sql = """
select *
from student 
where student.SId not in (
select t1.SId
from 
(select student.SId,t.CId
from student ,(select sc.CId from sc where sc.SId='01') as t )as t1 
left join sc on t1.SId=sc.SId and t1.CId=sc.CId
where sc.CId is null )
and student.SId !='01'
"""

print(m.fetchall(sql))
print(m.fetchall(sql, to_json=True))
print("--------------------------------")
