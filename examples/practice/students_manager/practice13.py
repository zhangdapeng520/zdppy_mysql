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

#  按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩
sql = """
select 
sc.SId,sc.CId,sc.score,t1.avgscore 
from  sc left join (select sc.SId,avg(sc.score) as avgscore 
from sc 
GROUP BY sc.SId) as t1 on sc.SId =t1.SId 
ORDER BY t1.avgscore DESC
"""

print(m.fetchall(sql))
print(m.fetchall(sql, to_json=True))
print("--------------------------------")
