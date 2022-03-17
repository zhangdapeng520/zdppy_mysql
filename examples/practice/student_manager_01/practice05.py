from zdppy_mysql import Mysql

m = Mysql(db="test")

# 查询Score表中的最高分的学生学号和课程号
sql = """
select sno, CNO
from score
where DEGREE = (
    select max(DEGREE)
    from score
);
"""

m.log.info(m.fetchone(sql))

# 方法2：效率更高
sql = """
select sno, CNO
from score
order by DEGREE desc
limit 1;
"""

m.log.info(m.fetchone(sql))
