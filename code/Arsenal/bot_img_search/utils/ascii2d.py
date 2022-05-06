# -*- encoding: utf-8 -*-
'''
@File    :   ascii2d.py
@Time    :   2022/02/27 23:55:22
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib


from loguru import logger


class Ascii2dItem:
    URL = 'https://ascii2d.net'

    def __init__(self, item) -> None:
        # 图片分辨率 格式 大小信息
        self.info = "unknown"
        # 缩略图
        self.thumb = ""
        # hash
        self.hash = "unknown"

        # 来源链接
        self.pic_link = "unknown"
        # 标题
        self.pic_name = "unknown"
        # 作者链接
        self.author_link = "unknown"
        # 作者名称
        self.author = "unknown"
        # 类型
        self.type = "unknown"

        self._integrate(item)

    def _integrate(self, item):
        """data type: html"""
        try:
            self.info = item.xpath(""".//div[2]/small/text()""")[0]
        except:
            pass

        try:
            self.thumb = f"{Ascii2dItem.URL}{item.xpath('.//div[1]/img/@src')[0]}"
        except:
            pass

        try:
            self.hash = item.xpath(""".//div[2]/div[@class='hash']/text()""")[0]
        except:
            pass

        self.get_detailInfo(item)
        
        # 额外处理
        self.pic_name = self.pic_name.replace("\u3000"," ").replace("\n","")
        self.type = self.type.replace("\n","")

        # pic_link
        self.pic_link = self.pic_link.replace("\n","")
        if "/ch2/" in self.pic_link:
            self.pic_link = Ascii2dItem.URL + self.pic_link
            
        
    def get_detailInfo(self, item)->dict:
        detail_info = item.xpath(""".//div[@class='detail-box gray-link']""")
        logger.debug(detail_info)

        if detail_info:
            check_data = detail_info[0].xpath("""./strong[@class='info-header']/text()""")
            # ascii2d类型数据
            if not check_data:
                _ = detail_info[0].xpath(""".//h6""")
                if not _:return

                _test = _[0].xpath("""./small[@class='text-muted']/a""")
                _dmm = _[0].xpath("""./small[@class='text-muted']""")
                if _test:
                    try:
                        self.pic_name = _[0].xpath("""./text()""")[0]
                    except:
                        pass

                    try:
                        self.pic_link = _dmm[0].xpath("""./a/@href""")[0]
                    except:
                        pass

                    try:
                        self.type = _dmm[0].xpath("""./a/text()""")[0]
                    except:
                        pass
                else:
                    try:
                        self.pic_name = _[0].xpath("""./a[1]/text()""")[0]
                    except:
                        pass

                    try:
                        self.pic_link = _[0].xpath("""./a[1]/@href""")[0]
                    except:
                        pass

                    try:
                        self.author = _[0].xpath("""./a[2]/text()""")[0]
                    except:
                        pass

                    try:
                        self.author_link = _[0].xpath("""./a[2]/@href""")[0]
                    except:
                        pass

                    try:
                        self.type = _[0].xpath("""./small/text()""")[0]
                    except:
                        pass

            # 评论类型数据
            elif check_data[0] == "登録された詳細":
                comment_data = detail_info[0].xpath("""./div[@class='external']""")[0]
                data = comment_data.xpath(" ./a")
                logger.debug(f"<comment_data> - {comment_data} | <data> - {data}")                
                
                # 较少数据
                if not data:
                    try:
                        self.pic_link = comment_data.xpath("""./text()""")[0]
                    except:
                        pass

                # 较多数据
                else:
                    # 评论+文字+链接 如:dmm dlsite
                    if len(data) == 1:
                        try:
                            self.pic_name = comment_data.xpath("""./text()""")[0]
                        except:
                            pass

                        try:
                            self.pic_link = data[0].xpath("""./@href""")[0]
                        except:
                            pass

                        try:
                            self.type = data[0].xpath("""./text()""")[0]
                        except:
                            pass

                    elif len(data) == 2:
                        try:
                            self.pic_name = data[0].xpath("""./text()""")[0]
                        except:
                            pass

                        try:
                            self.pic_link = data[0].xpath("""./@href""")[0]
                        except:
                            pass

                        try:
                            self.author = data[1].xpath("""./text()""")[0]
                        except:
                            pass

                        try:
                            self.author_link = data[1].xpath("""./@href""")[0]
                        except:
                            pass

                        try:
                            self.type = comment_data.xpath("""./small/text()""")[0]
                        except:
                            pass


class Ascii2dResp:
    def __init__(self, resp_list:list) -> None:
        self.results = []

        for resp in resp_list:
            self.results.append(Ascii2dItem(resp))