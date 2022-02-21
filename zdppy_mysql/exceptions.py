class MysqlException(Exception):
    def __init__(self, *args):
        super(MysqlException, self).__init__(*args)


class ConnectError(MysqlException):
    """
    MySQL连接错误
    """

    def __init__(self, *args):
        super(MysqlException, self).__init__(*args)


class ParamError(MysqlException):
    """
    参数错误
    """

    def __init__(self, *args):
        super(MysqlException, self).__init__(*args)
