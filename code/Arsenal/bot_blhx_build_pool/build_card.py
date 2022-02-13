# -*- encoding: utf-8 -*-
'''
@File    :   build_card.py
@Time    :   2022/02/09 11:02:29
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import os
import time
import random
from PIL import Image,ImageDraw

from Arsenal.basic.log_record import logger


class Build_Ships_Card:
    """合成十连界面"""
    def __init__(self, blhx_tool):
        self.blhx_tool = blhx_tool

    def build_card(self, ship_data, extra):
        """
        十连建造图片合成
        :params ship_data: 舰娘数据
        :params extra: 额外参数
        :return: build_card_path,合成后的十连建造图片路径
        """
        # 关闭 - 皮肤/改造/誓约显示
        if extra.get("skin","") == self.blhx_tool.default_skin:
            result_img_path = []
            for i in ship_data:  
                list_files = []
                for j in os.listdir(i["shipPath"]):
                    _ = j.rsplit(".",1)[0]
                    if "." not in _:
                        list_files.append(j)
                try:
                    temp_path = os.path.join(i["shipPath"],random.choice(list_files))
                except Exception as e:
                    logger.warning(f"Err <list_files> - {i} {os.listdir(i['shipPath'])}")
                    temp_path = os.path.join(i["shipPath"],random.choice(os.listdir(i["shipPath"])))

                result_img_path.append(temp_path)
        else:
            result_img_path = [os.path.join(i["shipPath"],random.choice(os.listdir(i["shipPath"]))) for i in ship_data]
        
        # 舰娘船坞头像图片
        img_ships_list = []
        for img_path in result_img_path:
            img_ship = Image.open(img_path)
            img_ship = img_ship.resize((91,128))
            img_ship = self.circle_corner(img_ship,radii=7)
            img_ships_list.append(img_ship)

        # 十连建造背景
        img_build_bg = Image.open(self.blhx_tool.img_build_bg_path)
        # new标识
        new = Image.open(self.blhx_tool.new_ico_path)
        # new坐标
        new_coordinate_list = self.blhx_tool.new_coordinate_list
        # 图片坐标
        img_coordinate_list = self.blhx_tool.img_coordinate_list # img_coordinate_list

        # 粘贴船坞头像
        for i in range(len(img_ships_list)):
            img_build_bg.paste(img_ships_list[i], img_coordinate_list[i], mask=img_ships_list[i].split()[-1])

        # 粘贴new标识
        for i in range(len(new_coordinate_list)):
            if ship_data[i]["isNew"]:
                img_build_bg.paste(new, new_coordinate_list[i], mask=new.split()[-1])

        build_card_path = os.path.join(self.build_card_result_path,"{}.png".format(int(time.time())))
        img_build_bg.save(build_card_path,qulity=100)
        return build_card_path

    def circle_corner(self, img, radii):
        """
        圆角处理
        :param img: 源图象。
        :param radii: 半径,如: 30
        :return: 返回一个圆角处理后的img
        """
        # 画圆 (用于分离4个角)
        circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
        # circle = Image.new('RGBA', (radii * 2, radii * 2))  # 创建一个黑色背景的画布
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
        # 原图
        img = img.convert("RGBA")
        w, h = img.size

        # 四角
        alpha = Image.new('L', img.size, 255)
        # 左上角
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
        # 右上角
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
        # 右下角
        alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))
        # 左下角
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))
        # alpha.show()
        
        img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
        return img