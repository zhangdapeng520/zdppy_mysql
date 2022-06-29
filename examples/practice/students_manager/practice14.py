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

#   查询各科成绩最高分、最低分和平均分
sql = """
select sc.CId ,max(sc.score)as 最高分,min(sc.score)as 最低分,AVG(sc.score)as 平均分,count(*)as 选修人数,sum(case when sc.score>=60 then 1 else 0 end )/count(*)as 及格率,sum(case when sc.score>=70 and sc.score<80 then 1 else 0 end )/count(*)as 中等率,sum(case when sc.score>=80 and sc.score<90 and sc.score<80 then 1 else 0 end )/count(*)as 优良率,sum(case when sc.score>=90 then 1 else 0 end )/count(*)as 优秀率 
from sc
GROUP BY sc.CId
ORDER BY count(*)DESC,sc.CId asc
"""

print(m.fetchall(sql))
print(m.fetchall(sql, to_json=True))
print("--------------------------------")
