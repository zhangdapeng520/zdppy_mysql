from typing import List, Any
from .exceptions import ParamError


def get_add_sql(table: str, columns: List[str]):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if not columns or not isinstance(columns, list):
        raise ParamError(f"columns 参数错误：columns={columns}")

    # 准备参数
    column_str = ", ".join(columns)
    values = ["%s" for _ in columns]
    values_str = ", ".join(values)

    # 准备sql
    s = f"insert into {table} ({column_str}) values ({values_str});"
    return s


def get_add_many_sql(table: str, columns: List[str], values_length: int):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if not columns or not isinstance(columns, list):
        raise ParamError(f"columns 参数错误：columns={columns}")
    if not values_length or not isinstance(values_length, int):
        raise ParamError(f"values_length 参数错误：values_length={values_length}")

    # 准备参数
    column_str = ",".join(columns)
    values = ["%s" for _ in columns]
    values_str = ",".join(values)
    values_str = f"({values_str})"
    values_strs = [values_str for _ in range(values_length)]
    values_strs = ", ".join(values_strs)

    # 准备sql
    s = f"insert into {table} ({column_str}) values {values_strs};"
    return s


def get_sql_delete_by_id(table: str):
    """
    获取添加数据的字符串
    :param table:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")

    # 准备sql
    s = f"delete from {table} where id = %s;"
    return s


def get_sql_delete_by_ids(table: str, ids_length: int):
    """
    获取添加数据的字符串
    :param table:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if not ids_length or not isinstance(ids_length, int):
        raise ParamError(f"ids_length 参数错误：ids_length={ids_length}")

    # 准备参数
    ids = ["%s" for _ in range(ids_length)]
    ids_str = ", ".join(ids)

    # 准备sql
    s = f"delete from {table} where id in ({ids_str});"
    return s


def get_sql_update_by_id(table: str, columns: List[str]):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if not columns or not isinstance(columns, List):
        raise ParamError(f"columns 参数错误：columns={columns}")

    # 准备参数
    kvs = [f"{columns[i]}=%s" for i in range(len(columns))]
    ids_str = ", ".join(kvs)

    # 准备sql
    s = f"update {table} set {ids_str} where id = %s;"
    return s


def get_sql_update_by_ids(table: str, columns: List[str], ids_length: int):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :param ids_length:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if not columns or not isinstance(columns, List):
        raise ParamError(f"columns 参数错误：columns={columns}")
    if not ids_length or not isinstance(ids_length, int):
        raise ParamError(f"ids_length 参数错误：ids_length={ids_length}")

    # 准备参数
    kvs = [f"{columns[i]}=%s" for i in range(len(columns))]
    kvs_str = ", ".join(kvs)

    ids = ["%s" for _ in range(ids_length)]
    ids_str = ", ".join(ids)

    # 准备sql
    s = f"update {table} set {kvs_str} where id in ({ids_str});"
    return s


def get_sql_find_by_id(table: str, columns: List[str]):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if columns and not isinstance(columns, List):
        raise ParamError(f"columns 参数错误：columns={columns}")

    # 准备参数
    columns_str = "*"
    if columns is not None:
        columns_str = ", ".join(columns)

    # 准备sql
    s = f"select {columns_str} from {table} where id = %s;"
    return s


def get_sql_find_by_ids(table: str, columns: List[str], ids_length: int):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if columns and not isinstance(columns, List):
        raise ParamError(f"columns 参数错误：columns={columns}")
    if ids_length and not isinstance(ids_length, int):
        raise ParamError(f"ids_length 参数错误：ids_length={ids_length}")

    # 准备参数
    columns_str = "*"
    if columns is not None:
        columns_str = ", ".join(columns)
    ids = ["%s" for _ in range(ids_length)]
    ids_str = ", ".join(ids)

    # 准备sql
    s = f"select {columns_str} from {table} where id in ({ids_str});"
    return s


def get_sql_find_by_page(table: str, columns: List[str],
                         page: int = 1,
                         size: int = 20,
                         asc_columns: List[str] = None,
                         desc_columns: List[str] = None):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :return:
    """
    # 校验数据
    if not table:
        raise ParamError(f"table 参数错误：table={table}")
    if columns and not isinstance(columns, List):
        raise ParamError(f"columns 参数错误：columns={columns}")
    if page <= 0:
        page = 1
    if size <= 0 or size > 100:
        size = 20

    # 准备参数
    columns_str = "*"
    if columns is not None:
        columns_str = ", ".join(columns)

    # 准备sql
    s = f"select {columns_str} from {table}"

    # 排序
    if asc_columns is not None or desc_columns is not None:
        s = f"{s} order by"
        if asc_columns is not None:
            asc_str = ", ".join(asc_columns)
            s = f"{s} {asc_str} asc"
        if desc_columns is not None:
            desc_str = ", ".join(desc_columns)
            s = f"{s} {desc_str} desc"

    # 分页
    offset = (page - 1) * size
    s = f"{s} limit {size} offset {offset}"
    return s


def get_create_table_sql(table: str, id_column=None, columns: List = None, open_engine=True):
    """
    获取创建表格的SQL语句
    :return: 创建表格的SQL语句
    """
    # 处理id列
    if id_column is None:
        id_column = "id bigint primary key auto_increment,"

    # 处理columns列表
    if columns is None:
        raise ParamError("columns不能为空")
    columns_str = ",".join(columns)

    # 引擎
    engine_str = ";"
    if open_engine:
        engine_str = "engine = innodb charset=utf8mb4;"

    # 整理SQL语句
    s = f"create table if not exists {table} ({id_column} {columns_str}) {engine_str}"

    # 返回SQL语句
    return s


if __name__ == '__main__':
    # print(get_add_sql("student", ["name", "age"]))
    print(get_add_many_sql("student", ["name", "age"]), [["张三", 22], ["李四", 33]])
