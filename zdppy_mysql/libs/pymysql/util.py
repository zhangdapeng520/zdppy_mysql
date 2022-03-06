import struct


def byte2int(b):
    """
    字节类型转换为整数类型
    :param b: 数据
    :return: 整数
    """
    if isinstance(b, int):
        return b
    else:
        return struct.unpack("!B", b)[0]


def int2byte(i):
    """
    整数转字节
    :param i:整数
    :return: 字节
    """
    return struct.pack("!B", i)

