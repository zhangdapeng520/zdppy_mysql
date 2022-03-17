from zdppy_mysql import Mysql

m = Mysql(db="test")

# 以 cno 升序、degree降序查询 score 表的所有记录
sql = """
select *
from score
order by CNO asc, degree desc;
"""

m.log.info(m.fetchall(sql, to_json=True))
