# -*- encoding: utf-8 -*-
'''
@File    :   PluginClass.py
@Time    :   2022/02/07 22:01:39
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
# 导入内置库及第三方库
pass

# 导入自定义模块
from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.basic.msg_temp import PLUGIN_BLOCK, PLUGIN_IGNORE

# 插件主类命名以模块文件(如:bot_ascii2d_img.py)
# bot_之后的部分为名,并且首字母大写
# 如:class Ascii2d_Img
class PluginClass:
    """简要注释类功能"""

    def __init__(self):
        # 必须
        self.plugin_name = type(self).__name__

        # 可选-插件别名 - 展示给用户,无则使用plugin_name
        self.plugin_nickname = "测试插件"

        # 插件类型 - 1-主动式插件,0-被动式插件,默认1
        self.plugin_type = 1
        # self.plugin_type = your plugin_type

        # 插件权限 - 10~999为主动式插件,1~9为被动式插件,默认为10
        self.plugin_level = [v for k,v in {1: 10, 0: 5}.items() if self.plugin_type == k][0]
        # self.plugin_level = your plugin_level
        
        # 静态资源文件目录
        self.resource_path = pdr.resource
        # self.resource_path = your resource path
        
        # 插件工作目录
        self.workspace = pdr.get_plus_res(self.plugin_name)
        # self.workspace = your workspace

    def help_info(self):
        """插件介绍"""
        return """|============|\n"""\
               """|  暂无相关  |\n"""\
               """|  插件介绍  |\n"""\
               """|============|"""
        
    def parse(self,mybot_data:dict) -> dict:
        """
        每个功能插件的主类必须存在一个parse函数
        用以解析mybot_data和执行插件功能
        
        :param mybot_data: mybot内部消息体
        :return: PLUGIN_BLOCK / PLUGIN_IGNORE
        """

        """
        # ===== 主动式插件demo =====
        
        message = mybot_data["arrange"].get("message")
        # your expression
        if "hello world" in message:
            # send message to go-cq or anything
            # do something
            # 命中解析规则
            return PLUGIN_BLOCK
        elif "#time" in message:
            mybot_data["at"] = True
            mybot_data["message"] = now_time
            tool.auto_send_msg(mybot_data)
            return PLUGIN_BLOCK


        # 未命中,使用下一个插件解析规则进行解析
        return PLUGIN_IGNORE

        # ===== 主动式插件demo =====
        # ===== 被动式插件demo =====

        message = mybot_data["arrange"].get("message")
        # your expression
        if "hello world" in message:
            # do something
            # 无论是否命中解析规则,都返回PLUGIN_IGNORE
            return PLUGIN_IGNORE

        return PLUGIN_IGNORE

        # ===== 被动式插件demo =====

        """
        return PLUGIN_IGNORE
        
# 实例化对象以'Bot_' + 类名来命名
# 插件加载器通过识别'Bot_'(特征之一)来载入实例对象
# 此处仅为注释说明使用
# Bot_Ascii2d_Img = Ascii2d_Img()