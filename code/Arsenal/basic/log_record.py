# -*- encoding: utf-8 -*-
'''
@File    :   log_record.py
@Time    :   2021/05/08 14:50:15
@Author  :   Coder-Sakura
@Version :   1.0
@Contact :   1508015265@qq.com
@Desc    :   None
'''

# here put the import lib
import os
import sys
import yaml
from loguru import logger
from yaml.loader import SafeLoader


from Arsenal.basic.msg_temp import TOOL_TEMP


def init_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "..","..","config.yaml")
    default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "..","..","resource","temp","default.yaml")
    if not os.path.exists(config_path):
        with open(config_path,"w") as f1:
            with open(default_path) as f2:
                f1.write(f2.read())
                
    config_yaml = yaml.load(open(config_path, encoding="utf8"), Loader=SafeLoader)
    return config_yaml



config_yaml = init_config()
if config_yaml["Debug"]:
    level = "DEBUG"
else:
    level = "INFO"

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "log")
# remove default handler
logger.remove()
# 控制台输出
logger.add( 
    sys.stderr,
    level=level
)
# 日志写入
logger.add( 
    os.path.join(log_path, "{time}.log"),
    encoding="utf-8",
    rotation="00:00",
    enqueue=True,
    level=level
)

"""
DEBUG    10 logger.debug()
INFO     20 logger.info()
SUCCESS  25 logger.success()
WARNING  30 logger.warning()
ERROR    40 logger.error()
CRITICAL 50 logger.critical()
"""


"""
使用@logger.catch可以直接进行 Traceback 的记录
@logger.catch
def my_function(x, y, z):
    return 1 / (x + y + z)

my_function(0, 0, 0)
"""