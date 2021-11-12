import os
import random
from PIL import Image, ImageFilter

import requests
import random

class MyGaussianBlur(ImageFilter.Filter):
    # 用于给图片自定义高斯模糊滤镜
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        # 模糊半径默认为2
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        """
        用于给图片添加高斯滤镜
        根据bounds可以只给指定区域添加

        :param image: Image对象
        :return: 添加高斯滤镜后的Image对象
        """
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


class GasussianBlur_Img:
    """主类 高斯模糊"""

    def __init__(self):
        # 默认存储位置
        # self.path = r"C:\Users\Administrator\Desktop\CQA-tuling\python插件\coolq-trace_anime-master\res\blur"
        self.path = ""
        if not self.path:self.path = os.getcwd()

    def ready_img(self,img_path=None,img_url=None,radius=10)->str:
        """
        在filter进行前的一些准备工作,比如下载/打开图片以获得Image对象

        :param img_path: 本地图片路径(两者都存在,则该项优先)
        C:\\Users\\Administrator\\Desktop\\HoqgblbnFgekkdf.jpg
        
        :param img_url: 网络图片路径
        https://i.pximg.net/img-master/img/2019/11/12/03/26/16/77775892_master1200.jpg

        :return: 添加高斯模糊后的本地图片路径
        """
        # 两个参数都不存在
        if not img_path and not img_url:
            return ""

        # 本地图片路径优先
        if img_path:
            filename_list = img_path.rsplit(".")
            new_img_path = "_blur.".join(filename_list)
            image = Image.open(img_path)
            image = image.filter(MyGaussianBlur(radius=radius))
            image.save(new_img_path)
            return new_img_path

        # 网络图片,主要用于pixiv的图片
        if img_url:
            if img_url[-3:] in ["jpg","png"] and img_url[-4] == '.':
                filename = img_url.rsplit("/",1)[-1]
                # ['77775892_master1200', 'jpg']
                filename_list = filename.rsplit(".")
                new_filename = "_blur.".join(filename_list)

                old_img_path = os.path.join(self.path,filename)
                new_img_path = os.path.join(self.path,new_filename)

                # 网络请求后面需统一使用basic内的模块
                headers = {
                    "Host": "www.pixiv.net",
                    "referer": "https://www.pixiv.net/",
                    "origin": "https://accounts.pixiv.net",
                    "accept-language": "zh-CN,zh;q=0.9",	# 返回translation,中文翻译的标签组
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                }
                try:
                    resp_content = requests.get(img_url,headers=headers,timeout=10).content
                except Exception as e:
                    resp_content = ""
                
                if resp_content:
                    with open(old_img_path,"wb") as f:
                        f.write(resp_content)

                    image = Image.open(old_img_path)
                    image = image.filter(MyGaussianBlur(radius=radius))
                    image.save(new_img_path)
                    os.remove(old_img_path)
                    return new_img_path
                # 没有获取到content
                else:
                    return ""

    def parse(self,eval_cqp_data:dict)->dict:
        pass

# GBImg = GasussianBlur_Img()
Bot_GasussianBlur_Img = GasussianBlur_Img()
# g = GasussianBlur_Img()
# img_url = "https://i.pximg.net/img-master/img/2019/11/12/03/26/16/77775892_master1200.jpg"
# new_path = g.ready_img(img_url=img_url)
# if new_path:
#     print(new_path)
# else:
#     print("下载出错")
# =====================


# simg = '1.jpg'
# dimg = 'res_1.jpg'
# image = Image.open(simg)
# image = image.filter(MyGaussianBlur(radius=10))
# image.save(dimg)