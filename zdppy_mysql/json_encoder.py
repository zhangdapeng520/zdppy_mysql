#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/7 23:46
# @Author  : 张大鹏
# @Site    : 
# @File    : json_encoder.py
# @Software: PyCharm
import json
import decimal
from datetime import datetime, date


class JsonEncoder(json.JSONEncoder):
    """
    decimal解析器
    """

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):  # 将decimal类型转换为float类型
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        super(JsonEncoder, self).default(obj)
