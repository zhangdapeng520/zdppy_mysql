import asyncio
from zdppy_mysql import AsyncMysql
import time

m = AsyncMysql(host="127.0.0.1",
               port=3306,
               user='root',
               password='root',
               db='test', )


async def add():
    result = await  m.add("student", ["name", "age", "gender"], ["张三", 22, True])
    m.log.info(result)


async def add_many():
    result = await  m.add_many("student", ["name", "age", "gender"], [["张三1", 22, True], ["张三2", 22, True]])
    m.log.info(result)


async def delete_by_id():
    result = await  m.delete_by_id("student", 1)
    m.log.info(result)


async def delete_by_ids():
    ids = (16, 17, 8, 1)
    result = await  m.delete_by_ids("student", ids)
    m.log.info(result)


async def update_by_id():
    columns = ["name", "age"]
    values = ["张三三", 22]
    id = 18
    result = await  m.update_by_id("student", columns, values, id)
    m.log.info(result)


async def update_by_ids():
    columns = ["name", "age"]
    values = ["张三三111", 22]
    ids = [11, 12, 10]
    result = await  m.update_by_ids("student", columns, values, ids)
    m.log.info(result)


async def find_by_id():
    columns = ["name", "age"]
    id = 10
    result = await  m.find_by_id("student", columns, id)
    m.log.info(result)
    result = await m.tuple1_to_dict(columns, result)
    m.log.info(result)

    result = await  m.find_by_id("student", None, id)
    m.log.info(result)


async def find_by_ids():
    columns = ["name", "age"]
    ids = (10, 11, 12)
    result = await  m.find_by_ids("student", columns, ids)
    m.log.info(result)
    result = await m.tuple2_to_dict(columns, result)
    m.log.info(result)

    result = await  m.find_by_ids("student", None, ids)
    m.log.info(result)


async def find_by_page():
    columns = ["name", "age"]
    result = await  m.find_by_page("student", columns, asc_columns=["id"])
    m.log.info(result)
    result = await m.tuple2_to_dict(columns, result)
    m.log.info(result)

    result = await m.find_by_page("student", None, desc_columns=["id"])
    m.log.info(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(add())
    # loop.run_until_complete(add_many())
    # loop.run_until_complete(delete_by_id())
    # loop.run_until_complete(delete_by_ids())
    # loop.run_until_complete(update_by_id())
    # loop.run_until_complete(update_by_ids())
    loop.run_until_complete(find_by_id())
    loop.run_until_complete(find_by_ids())
    loop.run_until_complete(find_by_page())
    loop.close()
