from zdppy_mysql import Mysql

m = Mysql(db="test")

# 查询Score表中成绩在60到80之间的所有记录
sql = """
select * from score where degree > 60 and degree < 80;
"""

print(m.fetchall(sql, to_json=True))
print("--------------------------------")

sql = """
select * from score where degree between 60 and 80;
"""

print(m.fetchall(sql, to_json=True))
print("--------------------------------")
