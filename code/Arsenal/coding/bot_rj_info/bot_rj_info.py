# -*- encoding: utf-8 -*-
'''
@File    :   dlsite_info.py
@Time    :   2021/05/28 21:11:32
@Author  :   Coder-Sakura
@Version :   1.0
@Contact :   1508015265@qq.com
@Desc    :   None
'''

# here put the import lib
import json
from lxml import etree


# from basic.plus_res_directory import pdr
from Arsenal.basic.BNConnect import baseRequest
from Arsenal.basic.log_record import logger


class RJ_Info:
    """有关DLsite上的RJ号查询
    1. 指定RJ号查询
    2. 指定关键字搜索
    """
    def __init__(self):
        self.headers = {
            "referer": "https://www.dlsite.com",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        # 关键字搜索
        self.search_dl_url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/keyword/{}/order[0]/trend/options[0]/JPN/options[1]/NM/per_page/30/lang_options[0]/%E6%97%A5%E6%9C%AC%E8%AA%9E/lang_options[1]/%E8%A8%80%E8%AA%9E%E4%B8%8D%E5%95%8F"
        self.search_result_expression = """.//ul[@id='search_result_img_box']//li/dl"""
        # 缩略图
        self.pic_expression = """.//a[@class='work_thumb_inner']/img/@src"""
        # 名称
        self.name_expression = """.//div[@class='multiline_truncate']/a/@title"""
        # DL地址
        self.url_expression = """.//a[@class='work_thumb_inner']/@href"""

        # 指定RJ号查询
        self.rj_ajax = "https://www.dlsite.com/maniax/product/info/ajax"
        self.temp_url = "https://www.dlsite.com/maniax/work/=/product_id/{}.html"

    def search_by_RJ(self,data):
        if data.get("product_id","") == "":
            logger.info("product_id is None")
            logger.info(data)
            return {}

        params = {"product_id":data["product_id"]}
        resp = baseRequest(options={"url":self.rj_ajax,"headers":self.headers},params=params)
        if resp:
            try:
                result = json.loads(resp.text)
            except json.decoder.JSONDecodeError as e:
                logger.info("JSONDecodeError: {}".format(e))
                logger.info(resp.text)
                return {}
            else:
                product_info = {}
                # RJ号信息为空
                if result == []:
                    logger.info(product_info)
                    return product_info

                for k,v in result.items():
                    product_info["pic"] = "http:" + v["work_image"]
                    product_info["product_name"] = v["work_name"]
                    product_info["RJ"] = k
                    product_info["dlsite_url"] = self.temp_url.format(k)
                logger.info(product_info)
                return product_info
        else:
            logger.info("resp is None")
            logger.info("{} {}".format(self.rj_ajax,data))
            return {}
                
    def search_by_keyword(self,data):
        if data.get("keyword","") == "":
            logger.info("keyword is None")
            logger.info(data)
            return {}

        url = self.search_dl_url.format(data["keyword"])
        resp = baseRequest(options={"url":url,"headers":self.headers,"timeout":10})
        if resp:
            obj = etree.HTML(resp.text)
            try:
                result = obj.xpath(self.search_result_expression)
            except Exception as e:
                logger.info("Xpath Parser Error: {}".format(e))
                logger.info(resp.text)
                return {}
            else:
                search_result_dict = {}
                if result == []:
                    logger.info(search_result_dict)
                    return search_result_dict
                
                # 只取前三个
                for _ in result[:3]:
                    pic = _.xpath(self.pic_expression)[0]
                    name = _.xpath(self.name_expression)[0]
                    url = _.xpath(self.url_expression)[0]
                    RJ = url.split("/")[-1].split(".")[0]

                    search_result_dict[RJ] = {}
                    search_result_dict[RJ]["pic"] = "http:" + pic
                    search_result_dict[RJ]["name"] = name
                    search_result_dict[RJ]["url"] = url
                    search_result_dict[RJ]["RJ"] = RJ

                logger.info(search_result_dict)
                return search_result_dict
        else:
            logger.info("resp is None")
            logger.info("{} {}".format(url,data))
            return {}

    def parse(self):
        return "Unexpected use..."

Bot_RJ_Info = RJ_Info()
"""
from bot_rj_info import Bot_RJ_Info
data = {"product_id":"RJ250814"}
data = {"product_id":""}
data = {"product_id":" "}
data = {"product_id":"asa"}
data = {"product_id":"123321"}
Bot_RJ_Info.search_by_RJ(data)

from bot_rj_info import Bot_RJ_Info
data = {"keyword":"RJ250814"}
data = {"keyword":"RJ"}
data = {"keyword":""}
data = {"keyword":" "}
data = {"keyword":"双 子"}
data = {"keyword":"双子"}
data = {"keyword":"双子乙女"}
Bot_RJ_Info.search_by_keyword(data)

"""