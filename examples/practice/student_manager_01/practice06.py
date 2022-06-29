from zdppy_mysql import Mysql

m = Mysql(db="test")

# 查询‘3-105’号课程的平均分。
sql = """
select avg(DEGREE)
from score
where CNO = '3-105';
"""

print(m.fetchone(sql, to_json=True))
    