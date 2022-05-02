# -*- encoding: utf-8 -*-
'''
@File    :   saucenao.py
@Time    :   2022/02/28 00:32:09
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
from typing import List
from Arsenal.basic.log_record import logger


class SauceNaoItem:
    URL = 'https://saucenao.com'

    def __init__(self, item) -> None:
        # 数据库id
        self.index_id = int()
        # 相似度
        self.similarity = float()
        # 缩略图
        self.thumbnail = ""
        # 图片标题 / 漫画标题
        self.title = "unknown"
        # 图片链接 / 本子链接
        self.url = ""
        # 作者名称
        self.member_name = "unknown"

        # 插画pid 可能存在
        self.pixiv_id = 0
        # 作者uid 可能存在
        self.member_id = 0
        # 同人本名称 可能存在
        self.doujinName = "unknown"
        # 番剧 可能存在 - 用于在anilist中查询番剧信息
        self.anilist_id = int()

        # # 区分普通搜图与搜本
        # self.normal = "normal"
        # self.doujin = "doujin"

        self._integrate(item)

    def _integrate(self, item):
        """
        data type: json
        """
        self.index_id = item["header"]["index_id"]
        self.similarity = float(item["header"]["similarity"])
        self.thumbnail = item["header"].get("thumbnail", "")
        self.title = self._get_title(item)
        self.url = self._get_url(item)
        self.member_name = self._get_author(item)
        self.pixiv_id = item["data"].get("pixiv_id", 0)
        self.member_id = item["data"].get("member_id", 0)
        self.doujinName = self._get_doujinName(item)
        self.anilist_id = item["data"].get("anilist_id", 0)

    @staticmethod
    def _get_title(item):
        data:dict = item["data"]
        title = data.get('title',"") or data.get('material',"") or \
                data.get('source',"") or data.get('created_at',"") or "unknown"
        return title

    @staticmethod
    def _get_author(item):
        data:dict = item["data"]
        try:
            author = data.get('author',"") or data.get('author_name',"") or \
                        data.get('member_name',"") or data.get('pawoo_user_username',"") or \
                        data.get('company',"") or data.get('creator',[""])[0] or \
                        data.get('creator',"") or "unknown"
        except Exception as e:
            logger.warning(f"Exception - {e} - {item}")
            author = "unknown"
        return author

    @staticmethod
    def _get_url(item):
        data:dict = item["data"]
        if "ext_urls" in data:
            url = data['ext_urls'][0]
        elif "getchu_id" in data:
            url = f"http://www.getchu.com/soft.phtml?id={data['getchu_id']}"
        else:
            url = ""
        return url

    @staticmethod
    def _get_doujinName(item):
        data:dict = item["data"]
        doujinName = data.get("jp_name", "") or data.get("eng_name", "") or "unknown"
        return doujinName


class SauceNaoResp:
    def __init__(self, resp:list) -> None:
        resp_header = resp["header"]
        resp_results = resp["results"]

        # 解析结果
        self.results: List[SauceNaoItem] = [SauceNaoItem(item) for item in resp_results]
        # 剩余搜索次数/30s
        self.short_limit: int = resp_header['short_remaining']
        # 剩余搜索次数/24h
        self.long_limit: int = resp_header['long_remaining']
