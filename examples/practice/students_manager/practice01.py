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

# 查询" 01 "课程比" 02 "课程成绩高的学生的信息及课程分数
sql = """
select *
from 
    (select SId ,score from sc where sc.CId='01') as t1,  # 课程01
    (select SId ,score from sc where sc.CId='02') as t2 # 课程02
where t1.SId = t2.SId # 筛选学生
and t1.score > t2.score; # 课程01的分数比课程02的分数高
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")


# 查询同时存在" 01 "课程和" 02 "课程的情况
sql = """
select *
from 
    (select SId ,score from sc where sc.CId='01')as t1 , 
    (select SId ,score from sc where sc.CId='02') as t2
where t1.SId=t2.SId;
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")


# 查询存在" 01 "课程但可能不存在" 02 "课程的情况(不存在时显示为 null )
sql = """
select *
from 
    (select SId ,score from sc where sc.CId='01')as t1 left join  
    (select SId ,score from sc where sc.CId='02') as t2
on t1.SId=t2.SId
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")


# 查询不存在" 01 "课程但存在" 02 "课程的情况
sql = """
select *
from sc
where sc.SId not in (select SId from sc where sc.CId='01') # 不存在课程01
and  sc.CId='02'; # 存在课程02
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")

