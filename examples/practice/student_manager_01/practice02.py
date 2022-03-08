from zdppy_mysql import Mysql

m = Mysql(db="test")

# 查询 score 表中成绩为85，86或88的记录
sql = """
select * from score where degree in (85, 86, 88);
"""

m.log.info(m.fetchall(sql, to_json=True))
print("--------------------------------")

m.log.info(m.find_column_in("score", "degree", (85, 86, 88), to_json=True))
print("--------------------------------")
