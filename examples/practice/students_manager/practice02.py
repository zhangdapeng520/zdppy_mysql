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

# 查询平均成绩大于等于 60 分的同学的学生编号和学生姓名和平均成绩
sql = """
select student.SId, student.Sname, t1.avgscore
from student inner JOIN(
    select sc.SId ,AVG(sc.score) as avgscore
    from sc 
    GROUP BY sc.SId
    HAVING AVG(sc.score)>=60) as t1 # 平均成绩大于60分的学生编号和平均成绩
on student.SId=t1.SId 
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")
