# -*- encoding: utf-8 -*-
''' 
@File    :   img_search_tool.py
@Time    :   2022/02/20 02:04:21
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
# from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.datetime_tool import datetime_now


# saucenao 索引数据库id
DB_id = {
	"all": 999,
	
	"pixiv": 5,
	"danbooru": 9,
	"yande": 12,
	"gelbooru": 25,
	"konachan": 26,
	
	"doujin": 38,
	"mangadex": 37,

	"niconico": 8,
	"anime": 21,
}


# 各个搜图引擎的一些常量配置
def saucenao_info_func():
    """saucenao info"""
    return {
        "short_limit_count": 3,     # 30秒内剩余次数 触发提醒次数
        "short_limit_min": 0,
        "long_limit_count": 30,     # 24h内剩余次数 触发提醒次数
        "long_limit_min": 0,
    }

def ascii2d_info_func():
    """ascii2d info"""
    return {

    }

def yandex_info_func():
    """yandex info"""
    return {

    }
saucenao_info = saucenao_info_func()
ascii2d_info = ascii2d_info_func()
yandex_info = yandex_info_func()


class Img_Search_Tool:
    def __init__(self, resource_path, workspace): 
        self.resource_path = resource_path 
        self.workspace = workspace
        self.tool = tool

        # self.default_engine = "saucenao"
        # self.engines = {
        #     "saucenao": "search_by_saucenao",
        #     "ascii2d": "search_by_ascii2d",
        #     "yandex": "search_by_yandex"
        # }

        # 搜图插件队列
        self.search_queue = []
        # 搜图 最大消息等待时间
        self.limit_seconds = tool.config["Plugin"]["bot_img_search"]["timeout"]

        # 初始化模板
        self.msg_temp()
        self.error_temp()
            
    def saucenao_api_key(self):
        return self.tool.config["Plugin"]["saucenao"]["api_key"]

    # ======== search_queue =======

    def search_queue_add(self, data):
        """搜图队列添加记录"""
        now_time = datetime_now()

        add_data = {
            "user_id": data["user_id"],
            "group_id": data["group_id"],
            "engineName": data["engineName"],
            "alway": data["alway"],
            "last": now_time
        }
        self.search_queue.append(add_data)
        logger.info(f"[ADD] 从搜图队列中增加: {add_data}")

    def search_queue_check(self, data):
        # 存在队列中
        # for i in self.search_queue[::-1]:
        for k,v in enumerate(self.search_queue[::]):
            if v["user_id"] == data["user_id"] and \
                v["group_id"] == data["group_id"]:
                now_time = datetime_now()
                self.search_queue[k]["last"] = now_time
                logger.info(f"[UPDATE] 从搜图队列中更新: {v}")
                # v["last"] = now_time
                # future_time = datetime_offset(now_time, self.limit_seconds)
                # i["expire"] = future_time
                break
        # 加入对象
        else:
            self.search_queue_add(data)

    def search_queue_delete(self, data):
        for i in self.search_queue[::]:
            if i["user_id"] == data["user_id"] and \
                i["group_id"] == data["group_id"]:
                self.search_queue.remove(i)
                # break
    
    # ======== search_queue =======


    def msg_temp(self):
        """general msg"""
        self.text_temp = {
            "help": """""",
            "alway_search_info": """已进入连续搜图模式, 请发送一张或多张图片进行搜图,"""\
                        """发送'退出搜图'以退出搜图队列.\n提示: 请注意发送图片的频次,以免给他人造成困扰""",
            
            "keywords": ["搜图", "连续搜图", "搜本", "退出搜图"],
            "enable_keyword_doujin": ["搜本"],
            "enable_keyword_img": ["搜图", "连续搜图"],
            "disable_keyword_img": ["退出搜图"],
        }


    def error_temp(self):
        """err msg"""
        self.err_temp = {
            
        }
