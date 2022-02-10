# -*- encoding: utf-8 -*-
'''
@File    :   plus_res_directory.py
@Time    :   2021/03/18 14:28:41
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   提供目录相关功能
'''

# here put the import lib
import os


# from your_module import your func
# from log_record import logger
from Arsenal.basic.log_record import logger


class PRDirectory:
    """检测/创建创建功能模块的res目录(工作目录)"""
    def __init__(self):
        # resource 静态资源文件目录
        self.resource = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..\\..\\resource")
        # 插件工作目录
        self.workspace = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..\\..\\workspace")
        if not os.path.exists(self.workspace):
            os.mkdir(self.workspace)
        
    def exists_path(self,path):
        """判断path是否存在"""
        return os.path.exists(path)

    def create_path(self,path):
        """根据path创建文件夹"""
        try:
            if not self.exists_path(path):
                os.mkdir(path)
        except Exception as e:
            logger.warning(f"<Exception> - {e}")
            logger.warning(f"<Error Path> - {path}")
            return False
        else:
            return True

    def get_plus_res(self,plus_name):
        """返回插件对应的res文件目录
        :params plus_name: 功能插件名称
        :return: plus_res_path/None
        """
        plus_res_path = os.path.join(self.workspace,plus_name)
        # 创建失败
        if not self.create_path(plus_res_path):
            return None
        return plus_res_path


pdr = PRDirectory()