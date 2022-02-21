# Add(c * gin.Context) // 增加数据
# AddMany(c * gin.Context) // 批量增加数据
# DeleteById(c * gin.Context) // 根据ID删除数据
# DeleteByIds(c * gin.Context) // 根据ID列表删除数据
# UpdateById(c * gin.Context) // 修改数据
# UpdateByIds(c * gin.Context) // 根据ID列表修改数据
# FindById(c * gin.Context) // 根据ID查询数据
# FindByIds(c * gin.Context) // 根据ID列表查询数据
# FindByPage(c * gin.Context) // 根据分页查询数据
from zdppy_mysql import Mysql

m = Mysql(db="test")


def add():
    result = m.add("student", ["name", "age", "gender"], ["张三", 22, True])
    print(result)


def add_many():
    result = m.add_many("student", ["name", "age", "gender"], [["张三1", 22, True], ["张三2", 22, True]])
    print(result)


def delete_by_id():
    result = m.delete_by_id("student", 1)
    print(result)


def delete_by_ids():
    ids = (6, 7, 8, 1)
    result = m.delete_by_ids("student", ids)
    print(result)


def update_by_id():
    columns = ["name", "age"]
    values = ["张三三", 22]
    id = 9
    result = m.update_by_id("student", columns, values, id)
    print(result)


def update_by_ids():
    columns = ["name", "age"]
    values = ["张三三111", 22]
    ids = [8, 9, 10]
    result = m.update_by_ids("student", columns, values, ids)
    print(result)


def find_by_id():
    columns = ["name", "age"]
    id = 10
    result = m.find_by_id("student", columns, id)
    print(result)
    result = m.find_by_id("student", None, id)
    print(result)


def find_by_ids():
    columns = ["name", "age"]
    ids = (10, 11, 12)
    result = m.find_by_ids("student", columns, ids)
    print(result)
    result = m.find_by_ids("student", None, ids)
    print(result)


def find_by_page():
    columns = ["name", "age"]
    result = m.find_by_page("student", columns, asc_columns=["id"])
    print(result)
    result = m.find_by_page("student", None, desc_columns=["id"])
    print(result)


if __name__ == '__main__':
    # add()
    # add_many()
    # delete_by_id()
    # delete_by_ids()
    # update_by_id()
    # update_by_ids()
    # find_by_id()
    # find_by_ids()
    find_by_page()
