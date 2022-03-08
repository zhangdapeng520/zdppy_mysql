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

#  查询没有学全所有课程的同学的信息
sql = """
select 
    student.*
from 
    student 
where 
    student.SId not in ( # 学完了所有课程的同学 
        select sc.SId from sc
        group by sc.SId
        having count(*)=(select count(CId) 
        from course))
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")

#  查询没有学全所有课程的同学的信息
sql = """
select 
    DISTINCT student.*
from 
    (select student.SId,course.CId
    from student,course ) as t1 
    LEFT JOIN (
        SELECT sc.SId,sc.CId from sc)as t2 
    on 
        t1.SId=t2.SId 
        and t1.CId=t2.CId,student
where 
    t2.SId is null
    and   t1.SId=student.SId
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")
