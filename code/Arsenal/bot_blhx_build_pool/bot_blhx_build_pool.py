# -*- encoding: utf-8 -*-
'''
@File    :   bot_blhx_build_pool.py
@Time    :   2021/03/30 17:30:10
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   碧蓝航线十连建造
'''

# here put the import lib
import os

from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.basic.plugin_class import PluginClass
from Arsenal.basic.msg_temp import PLUGIN_BLOCK, PLUGIN_IGNORE, MYBOT_ERR_CODE

from Arsenal.bot_blhx_build_pool.blhx_tool import BLHX_Tool
from Arsenal.bot_blhx_build_pool.build_pool import Lucky_Ships_Pool
from Arsenal.bot_blhx_build_pool.build_card import Build_Ships_Card
from Arsenal.bot_blhx_build_pool.data_handler import Blhx_Magic_Data


class Blhx_Build_Pool(PluginClass):
    """碧蓝航线模拟十连建造 - 主类"""
    def __init__(self):
        super(PluginClass, self).__init__()
        # 必须
        self.plugin_name = type(self).__name__

        # 可选-插件别名 - 展示给用户,无则使用plugin_name
        self.plugin_nickname = "碧蓝航线-模拟建造插件(十连)"

        # 插件类型 - 1-主动式插件,0-被动式插件,默认1
        self.plugin_type = 1

        # 插件权限 - 10~999为主动式插件,1~9为被动式插件,默认为10
        # self.plugin_level = [v for k,v in {1: 10, 0: 5}.items() if self.plugin_type == k][0]
        self.plugin_level = 10
        
        # 静态资源文件目录
        self.resource_path = os.path.join(pdr.resource, "Blhx_Build_Pool")
        # self.resource_path 无则不填
        
        # 插件工作目录
        self.workspace = pdr.get_plus_res(self.plugin_name)

        ####### 插件内部全局变量
        self.blhx_tool = BLHX_Tool(self.resource_path, self.workspace)

        self.LSP = Lucky_Ships_Pool(self.blhx_tool)
        self.BSC = Build_Ships_Card(self.blhx_tool)
        self.BMD = Blhx_Magic_Data(self.blhx_tool)

    def help_info(self):
        # 可用池
        poolList_Text = "\n● ".join(list(self.LSP.ship_key_data.keys()))
        # 支持倍率提升的池子
        support_multiple_pools_text = "\n● ".join(self.blhx_tool.support_multiple_pools)
        # 收藏率
        ships_user_data = self.BMD.r_blhx_data(extra_id=self.mybot_data["sender"]["user_id"])
        bookmark_rate = str(round(len(ships_user_data)/len(self.blhx_tool.ships_all_data)*100,3)) + "%"

        message = self.blhx_tool.text_temp["help"].format(
            poolList_Text, support_multiple_pools_text, bookmark_rate, str(self.mybot_data["user_info"]["magic_thing"]),
            self.blhx_tool.activity_pool_info()["name"]
        )
        return message

    def find_ship_data(self,name):
        """
        1.返回舰娘数据
        2.根据舰娘名称找出对应船坞头像路径
        :params name: 舰娘名称
        :return: data
            data: {
                'shipName': '栭', 
                'shipRawName': '谷风', 
                'shipType': '驱逐', 
                'starLevelText': '稀有', 
                'starLevel': 'R', 
                'shipCamp': '重樱', 
                'shipNum': 'NO.319',
                'shipPath': 'D:\\Code\\BLHX\\workspace\\ship\\稀有\\栭'
                }
        """
        data = {}
        for _ in self.blhx_tool.ships_all_data:
            if _["shipName"] == name:
                data = _
                break

        if not data:
            return {}
        else:
            logger.debug(f"{data}")
            starLevelText = data["starLevelText"]
            if starLevelText in ["最高方案","海上传奇","决战方案"]:
                starLevelText = "超稀有"
            shipPath = os.path.join(self.blhx_tool.root_dir, starLevelText, data["shipName"])
            data["shipPath"] = shipPath
            return data

    def get_card(self,extra={}):
        """
        生成并返回模拟建造的图片路径
        :params extra: 额外参数
        :return: path or None
        """
        try:
            ship_list = self.LSP.get_lucky_ships(
                pool_name = extra["pool"],
                multiple = extra["m"])
        except Exception as e:
            logger.info(f"ship_list error:{e}")
            ship_list = ["pool_data_items_error"]

        if ship_list == ["pool_data_items_error"]:
            return ""

        ship_data = []
        for ship in ship_list:
            data = self.find_ship_data(name=ship)
            if data:
                ship_data.append(data)
        
        # 有部分data为空,异常处理--待定
        if len(ship_data) != 10:
            logger.info(f"部分舰娘数据缺失,请更新或重新检查. <ship_list> - {ship_list}")
            return ""

        # 舰娘new数据添加
        ship_data = self.BMD.check_ship(ship_list, ship_data)
    
        # 生成图片
        try:
            build_card_path = self.BSC.build_card(ship_data, extra=extra)
        except Exception as e:
            logger.warning(f"build_card err - {e}")
            logger.warning(f"<ship_data> - {ship_data}")
            build_card_path = ""
        else:
            # 添加新舰娘数据
            self.BMD.w_blhx_data(ship_data)
        finally:
            return build_card_path

    def check_param(self, extra_params):
        """额外参数值校验
        return True or False
        """
        ## 客户端 ##
        # 检查pool 
        if extra_params.get("pool","") == "":
            extra_params["pool"] = self.blhx_tool.default_pool

        # 无效的建造池指定
        if extra_params["pool"] not in list(self.LSP.ship_key_data.keys()):
            self.mybot_data["message"] = self.blhx_tool.err_temp["pool_name_err_msg"].format(extra_params["pool"])
            tool.auto_send_msg(self.mybot_data)
            logger.warning(self.blhx_tool.err_temp["pool_name_err"].format(extra_params["pool"]))
            return PLUGIN_BLOCK

        # 建造池索引文件不存在
        pool_data_path = os.path.join(self.blhx_tool.resource_path, self.LSP.ship_key_data[extra_params["pool"]])
        if not os.path.exists(pool_data_path):
            self.mybot_data["message"] = self.blhx_tool.err_temp["pool_exists_err_msg"].format(extra_params["pool"])
            tool.auto_send_msg(self.mybot_data)
            logger.warning(self.blhx_tool.err_temp["pool_exists_err_msg"].format(extra_params["pool"]))
            return PLUGIN_BLOCK

        # 检查魔方
        if int(self.mybot_data["user_info"]["magic_thing"]) < self.blhx_tool.pool_limit_magic:
            self.mybot_data["message"] = self.blhx_tool.err_temp["magic_thing_err_msg"].format(
                self.mybot_data['user_info']['magic_thing'])
            tool.auto_send_msg(self.mybot_data)
            logger.warning(self.blhx_tool.err_temp["magic_thing_err_msg"].format(
                self.mybot_data['user_info']['magic_thing']))
            return PLUGIN_BLOCK

        # 检查skin
        if not extra_params.get("skin","") or \
            extra_params.get("skin","") not in self.blhx_tool.support_skin_value:
            logger.warning(self.blhx_tool.err_temp["skin_err_msg"])
            extra_params["skin"] = self.blhx_tool.default_skin

        # multiple
        if not extra_params.get("m",""):
            extra_params["m"] = self.blhx_tool.default_multiple

        try:
            extra_params["m"] = abs(int(extra_params["m"]))
        except:
            self.mybot_data["message"] = "参数m(multiple)错误,请重新输入"
            tool.auto_send_msg(self.mybot_data)
            logger.warning("参数m(multiple)错误,请重新输入")
            return PLUGIN_BLOCK
        
        if extra_params["m"] > 10 or extra_params["m"] <= 0:
            logger.warning(self.blhx_tool.err_temp["multiple_err_msg"])
            extra_params["m"] = self.blhx_tool.default_multiple
        
        if extra_params["m"] != self.blhx_tool.default_multiple:
            # 池子不支持提升multiple
            if extra_params["pool"] not in self.blhx_tool.support_multiple_pools:
                support_multiple_text = ",".join(self.blhx_tool.support_multiple_pools)
                self.mybot_data["message"] = "当前指定的建造池: <{}>不支持使用-m参数来提升up舰娘出货倍率!\n仅{}支持".\
                    format(extra_params["pool"],support_multiple_text)
                tool.auto_send_msg(self.mybot_data)
                return PLUGIN_BLOCK
        return PLUGIN_IGNORE

    @logger.catch
    def parse(self, mybot_data):
        self.mybot_data = mybot_data
        self.blhx_tool.mybot_data = mybot_data

        if self.mybot_data["sender"].get('type','') == 'group':
            group_id = self.mybot_data["sender"]["group_id"]
            user_id = self.mybot_data["sender"]["user_id"]
            message = self.mybot_data["arrange"]['message']
            split_words = message.split(" ")

            # 基本关键词检测
            if split_words[0] != self.blhx_tool.keyword:
                return PLUGIN_IGNORE

            # TODO delete 查询到用户数据
            # self.blhx_tool.user_now_data = self.mybot_data["user_info"]
            # if not self.blhx_tool.user_now_data:
            if not self.mybot_data["user_info"]:
                self.mybot_data["message"] = "未查询到用户相关数据"
                tool.auto_send_msg(self.mybot_data)
                logger.warning(self.blhx_tool.err_temp["not_found_user_err"].format(self.mybot_data))
                # 结束消息周期
                return PLUGIN_BLOCK

            # 整合传参
            extra_params = {}
            for word in split_words[1:]:
                k = word.split("=")[0].replace("-","")
                if k == self.blhx_tool.keyword_help:
                    extra_params = k
                    break
                else:
                    v = word.split("=")[1]
                    extra_params[k] = v

            # help
            if extra_params == self.blhx_tool.keyword_help:
                self.mybot_data["message"] = self.help_info()
                tool.auto_send_msg(self.mybot_data)
                # 结束消息周期
                return PLUGIN_BLOCK

            # 检查参数
            logger.debug(MYBOT_ERR_CODE["Generic_Value_Info"].format("extra_params",extra_params))
            if not self.check_param(extra_params):
                # 结束消息周期
                return PLUGIN_BLOCK
            logger.debug(MYBOT_ERR_CODE["Generic_Value_Info"].format("extra_params",extra_params))
            

            build_card_path = self.get_card(extra=extra_params)
            # 服务端错误
            if not build_card_path:
                self.mybot_data["message"] = "非常抱歉o(╥~~╥)o!当前建造池数据文件出错,请@管理员进行修复~"
                tool.auto_send_msg(self.mybot_data)
                return PLUGIN_BLOCK
            else:
                # 计算消耗的魔方
                magic_cost = 10
                if extra_params["m"] != self.blhx_tool.default_multiple:
                    magic_cost = 10 + extra_params["m"]
                
                # 更新魔方数量
                magic_old = self.mybot_data["user_info"]["magic_thing"]
                magic_now = int(magic_old) - int(magic_cost)
                self.mybot_data["user_info"]["magic_thing"] = magic_now
                tool.db.update_records(**{
                    "update_data": self.mybot_data["user_info"], 
                    "judge_data": {"uid": user_id, "gid": group_id}
                })

                # 收藏率
                ships_user_data = self.BMD.r_blhx_data(extra_id=self.mybot_data["sender"]["user_id"])
                bookmark_rate = str(round(len(ships_user_data)/len(self.blhx_tool.ships_all_data)*100,3)) + "%"
                self.mybot_data["message"] = self.blhx_tool.text_temp["success"].format(
                    extra_params["pool"], build_card_path,
                    int(magic_cost), magic_now, bookmark_rate
                )
                tool.auto_send_msg(self.mybot_data)
                return PLUGIN_BLOCK

        # 默认跳过
        return PLUGIN_IGNORE


Bot_Blhx_Build_Pool = Blhx_Build_Pool()