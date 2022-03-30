# -*- encoding: utf-8 -*-
'''
@File    :   bot_img_search.py
@Time    :   2022/02/20 02:10:30
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import time
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.plugin_class import PluginClass
from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.basic.datetime_tool import datetime_now, datetime_offset
from Arsenal.basic.msg_temp import MYBOT_ERR_CODE, TASK_PROCESSOR_TEMP,\
    PLUGIN_BLOCK, PLUGIN_IGNORE

# from Arsenal.bot_img_search.sites import saucenao, ascii2d, yandex
from Arsenal.bot_img_search.sites import SauceNao, Ascii2d, Yandex
from Arsenal.bot_img_search.img_search_tool import Img_Search_Tool,\
    saucenao_info, ascii2d_info, yandex_info


def callback():
    pass


class Img_Search(PluginClass):
    def __init__(self):
        super(PluginClass, self).__init__()
        self.plugin_name = type(self).__name__
        self.plugin_nickname = "二次元图片搜索"
        self.plugin_type = 1
        self.plugin_level = 10
        self.resource_path = ""        
        # 插件工作目录
        self.workspace = pdr.get_plus_res(self.plugin_name)

        ###########################
        # 配置类
        self.img_search_tool  = Img_Search_Tool(self.resource_path, self.workspace)
        # 搜图引擎设置
        self.engines = {
            "SauceNao": SauceNao,
            "Ascii2d": Ascii2d,
            "Yandex": Yandex,
            # TODO
            # "Doujin": Doujin, # 同人本 - SauceNao
            # "Iqdb": Iqdb
        }
        self.default_engineName = "SauceNao"
        self.default_engine = self.engines[self.default_engineName]

        # 搜图队列
        # tool.pool.put(self.cycle_check_SearchQueue, (), callback)

    def help_info(self):
        message = self.blhx_tool.text_temp["help"].format()
        return message

    def switch_img_engine(self, engineName):
        """切换为对应的搜图引擎"""
        return self.engines.get(engineName, self.default_engineName)

    @logger.catch
    def cycle_check_SearchQueue(self):
        # def check():
        while True:
            if tool.pool.terminal:
                logger.info(TASK_PROCESSOR_TEMP["TASK_BREAK_TERMINAL"])
                break

            logger.debug("cycle_check_SearchQueue check start")

            for i in self.img_search_tool.search_queue:
                # 到期时间
                expire_time = datetime_offset(i["last"], self.img_search_tool.limit_seconds)
                # 上一次调用时间与到期时间对比
                if datetime_now() > expire_time:
                    # logger.info(f'{future_time} {i["last"]}')
                    self.img_search_tool.search_queue_delete(i)
                    logger.info(f"[DELETE] 从搜图队列中删除: {i}")

            logger.debug(f"search_queue <{len(self.img_search_tool.search_queue)}> {self.img_search_tool.search_queue}")
            logger.debug(f"cycle_check_SearchQueue check success - sleep:{self.img_search_tool.limit_seconds}")
            time.sleep(self.img_search_tool.limit_seconds)


    @logger.catch
    def parse(self, mybot_data: dict) -> dict:
        self.mybot_data = mybot_data
        if self.mybot_data["sender"].get('type','') == 'group':
            group_id = self.mybot_data["sender"]["group_id"]
            user_id = self.mybot_data["sender"]["user_id"]
            message = self.mybot_data["arrange"]['message']
            split_words = message.split(" ")

            data = {
                "user_id": user_id,
                "group_id": group_id,
                "engineName": self.default_engineName,
                "alway": False,
            }

            # enable

            # disable

            # img

            # others

            if split_words[0] not in self.img_search_tool.text_temp["keywords"] or \
                data not in self.img_search_tool.search_queue:
                return PLUGIN_IGNORE

            self.img_search_tool.search_queue_check(data)
            logger.debug(self.img_search_tool.search_queue)
            return PLUGIN_BLOCK

        # 默认跳过
        return PLUGIN_IGNORE

Bot_Img_Search = Img_Search()