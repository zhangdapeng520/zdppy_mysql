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

#  查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩
sql = """
select student.SId,student.Sname,avg(sc.score)
from student ,sc
where student.SId=sc.SId
and   sc.score<60
GROUP BY sc.SId
HAVING count(*)>=2
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")
