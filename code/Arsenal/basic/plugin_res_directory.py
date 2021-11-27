# -*- encoding: utf-8 -*-
'''
@File    :   plus_res_directory.py
@Time    :   2021/03/18 14:28:41
@Author  :   Coder-Sakura
@Version :   1.0
@Contact :   1508015265@qq.com
@Desc    :   None
'''

# here put the import lib
import os


# from your_module import your func
# from log_record import logger
from Arsenal.basic.log_record import logger


class PRDirectory:
    """检测功能模块的res文件夹
    
    用于检测/创建类的res文件夹或指定文件夹
    """
    def __init__(self):
        """初始化工作"""
        # 类名称
        self.bot_name = type(self).__name__
        # print(self.bot_name)

        # 默认res资源文件根目录
        self.res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..\\..\\res")
        if not os.path.exists(self.res_path):
            os.mkdir(self.res_path)
        
    def exists_path(self,path):
        """判断path是否存在"""
        return os.path.exists(path)

    def create_path(self,path):
        """根据path创建文件夹"""
        try:
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
        plus_res_path = os.path.join(self.res_path,plus_name)
        if not self.exists_path(plus_res_path):
            # 创建失败
            if not self.create_path(plus_res_path):
                return None
        return plus_res_path


pdr = PRDirectory()