# -*- encoding: utf-8 -*-
'''
@File    :   ascii2d.py
@Time    :   2022/02/27 23:55:22
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib

class Ascii2dItem:
    URL = 'https://ascii2d.net'

    def __init__(self, item) -> None:
        # 图片信息
        self.info = ""
        # 图片链接
        self.pic_link = ""
        # 图片名称
        self.pic_name = ""
        # 作者链接
        self.author_link = ""
        # 作者名称
        self.author = ""
        # 缩略图
        self.thumb = ""
        # 类型
        self.type = ""

        self._integrate(item)

    def _integrate(self, item):
        """data type: html"""
        try:
            self.info = item.xpath(""".//div[2]/small""")
        except:
            self.info = None
        try:
            self.pic_link = item.xpath(""".//div[2]/div[3]/h6/a[1]/@href""")
        except:
            self.pic_link = None
        try:
            self.pic_name = item.xpath(""".//div[2]/div[3]/h6/a[1]/text()""")
        except:
            self.pic_name = None
        try:
            self.author_link = item.xpath(""".//div[2]/div[3]/h6/a[2]/@href""")
        except:
            self.author_link = None
        try:
            self.author = item.xpath(""".//div[2]/div[3]/h6/a[2]/text()""")
        except:
            self.author = None
        try:
            self.thumb = item.xpath(""".//div[1]/img/@src""")
        except:
            self.thumb = None
        try:
            self.type = item.xpath(""".//div[2]/div[3]/h6/small""")
        except:
            self.type = None
        

class Ascii2dResp:
    def __init__(self, resp_list:list) -> None:
        self.results = []

        for resp in resp_list:
            self.results.append(Ascii2dItem(resp))