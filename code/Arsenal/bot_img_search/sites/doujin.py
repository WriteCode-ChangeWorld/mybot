# -*- encoding: utf-8 -*-
'''
@File    :   doujin.py
@Time    :   2022/04/01 17:04:15
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   saucenao db-38 图片反向搜索
'''

# here put the import lib
from Arsenal.bot_img_search.sites import SauceNao


class Doujin(SauceNao):
    def __init__(self, 
                 api_key: str = None, 
                 db: int = 38, 
                 output_type: int = 2, 
                 testmode: int = 0, 
                 numres: int = 5
                 ) -> None:
        super().__init__(api_key, db, output_type, testmode, numres)