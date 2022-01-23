# -*- encoding: utf-8 -*-
'''
@File    :   bot_suolink.py
@Time    :   2021/12/15 17:09:20
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import requests

from Arsenal.basic.bot_tool import tool

# 网络请求函数修正后再统一导入使用
# from BNConnect import baseRequest


class so985:
    def __init__(self):
        self.plugin_name = type(self).__name__
        self.plugin_nickname = "短链接插件"
        self.plugin_level = 8
        # print(f"{self.plugin_name} - Warning!!!")
        # http://api.985.so/api.php?format=json&url=http%3a%2f%2fwww.baidu.com&apikey=18816765357@94f53154fef918eb70d7b74f9a5dfc67
        # {"status":1,"url":"http://r6f.cn/Mjqh","err":""}
        self.suolink_api = "http://api.985.so/api.php"
        # self.host = "https://dlj.li/{}"
    
    def parse(self,mybot_data):
        # TEST DynamicImport
        if mybot_data == "test1":
            return tool.PLUGIN_BLOCK
            return ""
            return None
            return 1
            return 0
    
    def get_slink(self,url):
        """
        :params url: 需要缩短的url
        :return: 短链,错误信息
        不报错则为空,报错则为err
        """
        # 调用BNC模块
        try:
        	# 这样不会直接编码
        	# u = "https://dlj.li/api.php?url={}".format(url)
            params = {
                "url":url,
                "apikey":"18816765357@94f53154fef918eb70d7b74f9a5dfc67",
            }
            resp = requests.get(self.suolink_api,params=params)
            print(resp.text)
        except Exception as e:
            print("so985 ",e)
            return "短链生成失败-dlj"
        else:
            return resp.text

Bot_suolink = so985()

# if __name__ == '__main__':
#     preview_url = "https://trace.moe/122137/[Ohys-Raws] Dogeza de Tanondemita - 08 (AT-X 1280x720 x264 AAC).mp4?start=101.58&end=123&token=FM2mP_l8IPxUaWAQ--D70A"
#     so985().get_slink(preview_url)
