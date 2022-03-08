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

# 查询所有同学的学生编号、学生姓名、选课总数、所有课程的总成绩(没成绩的显示为null)
sql = """
select student.SId,student.Sname,t1.sumscore,t1.coursecount
from student ,(
    select SC.SId,sum(sc.score) as sumscore ,count(sc.CId) as coursecount
    from sc 
    GROUP BY sc.SId) as t1
where student.SId =t1.SId
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")

#  查有成绩的学生信息
sql = """
select *
from student
where EXISTS(select * from sc where student.SId=sc.SId)
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")
