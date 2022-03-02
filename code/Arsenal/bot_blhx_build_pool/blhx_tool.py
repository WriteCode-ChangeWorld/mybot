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

        ##### 主类Blhx_Build_Pool #####
        # 合成所需船坞头像目录
        self.root_dir = os.path.join(self.resource_path, "shipyardicon")

        # 所有舰娘数据 暂时只有主类使用
        self.ships_all_data_filename = os.path.join(self.resource_path,"ships_all_data.json")
        self.ships_all_data = json.load(open(self.ships_all_data_filename,encoding="utf8"))


        ##### Blhx_Magic_Data #####
        # 用户舰娘图鉴数据目录 - 收藏率
        self.user_ship_data_dir = os.path.join(self.workspace,"user_ship_data")
        pdr.create_path(self.user_ship_data_dir)
        # TODO delete 用户数据
        # self.user_now_data = {}


        ##### Lucky_Ships_Pool #####
        # 建造池数据
        self.ship_key_filename = "pool_key.json"
        self.key_filepath = os.path.join(self.resource_path,self.ship_key_filename)
        
        
        ##### Build_Ships_Card #####
        # 生成图片路径
        self.build_card_result_path = os.path.join(self.workspace,"build_card_result")
        pdr.create_path(self.build_card_result_path)

        # 建造背景图片
        self.img_build_bg_path = os.path.join(self.resource_path, "static", "build_bg_final_2_RGBA.png")
        # new icon
        self.new_ico_path = os.path.join(self.resource_path, "static", "new_resize.png")
        # new icon 坐标
        self.new_coordinate_list = [
            (135,50),(244,50),(350,50),(456,50),(562,50),
            (180,194),(289,194),(395,194),(501,194),(607,194),
        ]
        # img 坐标
        self.img_coordinate_list = [
            (114,89),(223,89),(329,89),(435,89),(541,89),
            (159,233),(268,233),(374,233),(480,233),(586,233)
        ]


        # ====================自定义========================
        # 关键词
        self.keyword = "一键十连"
        self.keyword_help = "help"
        # 最低魔方需求
        self.pool_limit_magic = 10
        # 默认建造池
        self.default_pool = "啥都能建池"
        # 默认关闭 - 皮肤/改造/誓约显示
        self.default_skin = str(0)
        self.support_skin_value = ["0", "1"]
        # 默认倍率
        self.default_multiple = 1

        ##### 支持魔方-倍率提升的池子名称 #####
        self.support_multiple_pools = ["活动池"]

        # 初始化模板
        self.msg_temp()
        self.error_temp()

    def activity_pool_info(self):
        """活动池名称介绍"""
        return {"name": "「镜位螺旋」"}

    def msg_temp(self):
        self.text_temp = {
            "help": """<{}>使用方法:\n发送'一键十连'"""\
                    """\n添加参数: 发送'一键十连' -pool=活动池 -skin=1 -m=10"""\
                    """\n\n-help : 查看此条帮助信息"""\
                    """\n-pool : 指定建造池, 参考<当前可用池子>"""\
                    """\n-skin : 皮肤/誓约/改造的显示, 默认为0,关闭; 1为开启"""\
                    """\n-m : 额外消耗m个魔方(1~10), 提高所有抽卡概率m倍\n仅限<支持倍率提升池子>"""\
                    """\n\n当前可用池子:\n● {}"""\
                    """\n\n当前支持倍率提升池子:\n● {}"""\
                    """\n\n当前收藏率: {}"""\
                    """\n当前魔方: {}个"""\
                    """\n当前活动池为:「{}」活动"""\
                    """\n\n更多文档: https://www.yuque.com/mybot/blhx""",
            "success": """当前建造池: {}\n建造结果如下图:\n"""\
                       """[CQ:image,file=file:///{}]"""\
                       """消耗魔方: {}\n"""\
                       """当前魔方: {}\n"""\
                       """当前收藏率: {}"""
        }

    def error_temp(self):
        self.err_temp = {
            "pool_name_err": "指定的建造池<{}>不存在",
            "pool_name_err_msg": "指定的<{}>建造池不存在!\n可以使用'一键十连 -help'来查看详细信息",
            "pool_exists_err_msg": "指定的<{}>建造池索引文件不存在,请通知管理员!\n(: ′⌒`)",
            "magic_thing_err_msg": "十连建造至少需要10个魔方.\n当前魔方: {}个",
            "skin_err_msg": f"用户未显式指定skin或指定的<skin>参数错误,将采用默认参数 - {self.default_skin}",
            "multiple_err_msg": f"指定的<multiple>参数超出支持范围,将采用默认参数 - {self.default_multiple}",
            "general_err": "<{} value> err - {}",
            "not_found_user_err": "未查询到用户相关数据 <mybot_data> - {}"
        }