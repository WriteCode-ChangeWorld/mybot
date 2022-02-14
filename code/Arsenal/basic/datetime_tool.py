# -*- encoding: utf-8 -*-
'''
@File    :   datetime_tool.py
@Time    :   2022/01/19 16:28:58
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import datetime

def datetime_now()->datetime.datetime:
    return datetime.datetime.now()

def datetime_offset(now_time:datetime.datetime, offset:int)->datetime.datetime:
    """
    return datetime by now_time + offset
    :params offset: 秒数 
    """
    offset_seconds = datetime.timedelta(seconds=int(offset))
    return now_time + offset_seconds

def seconds2time(seconds:int)->list:
    """
    input: 86400
    output: [day, hour, minute, seconds]
    :params seconds: 秒
    """
    m,s = divmod(int(seconds), 60)
    h,m = divmod(m,60)
    d,h = divmod(h,24)
    return [d, h, m, s]

def str2datetime(now_time:str)->datetime.datetime:
    return datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")