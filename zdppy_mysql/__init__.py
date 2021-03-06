from .mysql import Mysql
import sys
from ._compat import PY2
from .constants import FIELD_TYPE
from .converters import escape_dict, escape_sequence, escape_string
from .err import (
    Warning, Error, InterfaceError, DataError,
    DatabaseError, OperationalError, IntegrityError, InternalError,
    NotSupportedError, ProgrammingError, MySQLError)
from .times import (
    Date, Time, Timestamp,
    DateFromTicks, TimeFromTicks, TimestampFromTicks)

VERSION = (0, 9, 3, None)
if VERSION[3] is not None:
    VERSION_STRING = "%d.%d.%d_%s" % VERSION
else:
    VERSION_STRING = "%d.%d.%d" % VERSION[:3]
threadsafety = 1
apilevel = "2.0"
paramstyle = "pyformat"


class DBAPISet(frozenset):

    def __ne__(self, other):
        if isinstance(other, set):
            return frozenset.__ne__(self, other)
        else:
            return other not in self

    def __eq__(self, other):
        if isinstance(other, frozenset):
            return frozenset.__eq__(self, other)
        else:
            return other in self

    def __hash__(self):
        return frozenset.__hash__(self)


STRING = DBAPISet([FIELD_TYPE.ENUM, FIELD_TYPE.STRING,
                   FIELD_TYPE.VAR_STRING])
BINARY = DBAPISet([FIELD_TYPE.BLOB, FIELD_TYPE.LONG_BLOB,
                   FIELD_TYPE.MEDIUM_BLOB, FIELD_TYPE.TINY_BLOB])
NUMBER = DBAPISet([FIELD_TYPE.DECIMAL, FIELD_TYPE.DOUBLE, FIELD_TYPE.FLOAT,
                   FIELD_TYPE.INT24, FIELD_TYPE.LONG, FIELD_TYPE.LONGLONG,
                   FIELD_TYPE.TINY, FIELD_TYPE.YEAR])
DATE = DBAPISet([FIELD_TYPE.DATE, FIELD_TYPE.NEWDATE])
TIME = DBAPISet([FIELD_TYPE.TIME])
TIMESTAMP = DBAPISet([FIELD_TYPE.TIMESTAMP, FIELD_TYPE.DATETIME])
DATETIME = TIMESTAMP
ROWID = DBAPISet()


def Binary(x):
    """
    返回x的二进制类型
    """
    return bytes(x)


def Connect(*args, **kwargs):
    """
    连接到数据库
    """
    from .connections import Connection
    return Connection(*args, **kwargs)


from . import connections as _orig_conn

if _orig_conn.Connection.__init__.__doc__ is not None:
    Connect.__doc__ = _orig_conn.Connection.__init__.__doc__
del _orig_conn


def get_client_info():
    """
    获取客户端信息
    """
    version = VERSION
    if VERSION[3] is None:
        version = VERSION[:3]
    return '.'.join(map(str, version))


connect = Connection = Connect

# 版本信息
version_info = (1, 3, 12, "final", 0)

NULL = "NULL"

__version__ = get_client_info()


def thread_safe():
    """
    线程安全，实现MySQLdb.thread_safe()
    """
    return True


def install_as_MySQLdb():
    """
    使用zdppy_mysql作为MySQL数据库DB引擎
    """
    sys.modules["MySQLdb"] = sys.modules["_mysql"] = sys.modules["zdppy_mysql"]


__all__ = [
    'BINARY', 'Binary', 'Connect', 'Connection', 'DATE', 'Date',
    'Time', 'Timestamp', 'DateFromTicks', 'TimeFromTicks', 'TimestampFromTicks',
    'DataError', 'DatabaseError', 'Error', 'FIELD_TYPE', 'IntegrityError',
    'InterfaceError', 'InternalError', 'MySQLError', 'NULL', 'NUMBER',
    'NotSupportedError', 'DBAPISet', 'OperationalError', 'ProgrammingError',
    'ROWID', 'STRING', 'TIME', 'TIMESTAMP', 'Warning', 'apilevel', 'connect',
    'connections', 'constants', 'converters', 'cursors',
    'escape_dict', 'escape_sequence', 'escape_string', 'get_client_info',
    'paramstyle', 'threadsafety', 'version_info',

    "install_as_MySQLdb",
    "NULL", "__version__",
    "Mysql",
]
