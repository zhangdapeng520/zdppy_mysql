from zdppy_mysql import Mysql

m = Mysql(db="test")

# 查询“95031”班的学生人数。
sql = """
select count(*)
from student
where student.CLASS = '95031';
"""

m.log.info(m.fetchone(sql))
