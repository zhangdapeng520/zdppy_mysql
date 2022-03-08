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

#  查询至少有一门课与学号为" 01 "的同学所学相同的同学的信息
sql = """
select DISTINCT student.* # 去重的用法
from  sc ,student
where sc.CId in (select CId from sc where sc.SId='01')
and   sc.SId=student.SId
"""

m.log.info(m.fetchall(sql))
m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")
