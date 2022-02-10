# -*- encoding: utf-8 -*-
'''
@File    :   blhx_tool.py
@Time    :   2022/02/09 15:53:42
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import os
import json

from Arsenal.basic.plugin_res_directory import pdr

class BLHX_Tool:
    """碧蓝航线模拟建造插件 - 全局变量"""
    def __init__(self, resource_path, workspace):
        self.resource_path = resource_path
        self.workspace = workspace

        # 合成所需船坞头像目录
        self.root_dir = os.path.join(self.resource, "shipyardicon")
        # TODO self.root_dir = r"D:\Code\BLHX\workspace\静态素材\船坞头像"

        # 舰娘数据
        self.ships_all_data_filename = os.path.join(self.resource,"ships_all_data.json")
        # TODO self.ships_all_data_filename = r"D:\Code\BLHX\blhx_code\res\ships_all_data.json"
        self.ships_all_data = json.load(open(self.ships_all_data_filename,encoding="utf8"))

        # 用户舰娘图鉴数据目录 - 收藏率
        self.user_ship_data_dir = os.path.join(self.workspace,"user_ship_data")
        pdr.create_path(self.user_ship_data_dir)
        # if not os.path.exists(self.user_ship_data_dir):os.mkdir(self.user_ship_data_dir)

        # 建造池数据 - build pool
        self.ship_key_filename = "pool_key.json"
        self.key_filepath = os.path.join(self.resource_path,self.ship_key_filename)
        

        # TODO 用户数据
        self.user_now_data = {}

        # ==================================================
        # 关键词
        self.keyword = "一键十连"
        self.keyword_help = "help"

        ##### 支持魔方-倍率提升的池子名称 #####
        self.support_multiple_pools = ["活动池"]

        # 模板相关
        self.msg_temp()

    def activity_pool_info(self):
        """活动池名称介绍"""
        return {"name": "「镜位螺旋」"}

    def msg_temp(self):
        self.text_temp = {
            "help": """当前可用池子:\n● {}"""\
                    """\n\n当前收藏率: {}"""\
                    """\n当前魔方: {}个"""\
                    """\n当前活动池为:「{}」活动"""\
                    """\n\n使用命令&相关文档 请访问: https://www.yuque.com/mybot/blhx"""\
                    """\n--2021/6/1更新""",
        }

    def err_temp(self):
        self.err_temp = {
            "pool_name_err": "建造池<{}>不存在 | 当前池子数据 - {}",
            "general_err": "<{} value> err - {}",
        }