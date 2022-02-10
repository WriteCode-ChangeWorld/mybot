# -*- encoding: utf-8 -*-
'''
@File    :   build_card.py
@Time    :   2022/02/09 11:02:29
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
pass

class Build_Ships_Card:
    """合成十连界面"""
    def __init__(self,workspace):
        self.resource = workspace
        # 十连建造合成后的输出目录
        self.build_card_result_path = os.path.join(self.resource,"build_card_result")
        if not os.path.exists(self.build_card_result_path):os.mkdir(self.build_card_result_path)
        # 十连建造背景图片
        # self.img_build_bg_path = r"D:\Code\BLHX\workspace\静态素材\建造背景_bg\build_bg_final_2.png"
        self.img_build_bg_path = r"D:\Code\BLHX\workspace\静态素材\建造背景_bg\build_bg_final_2_RGBA.png"
        # new标识路径
        self.new_ico_path = r"D:\Code\BLHX\workspace\静态素材\new标识\new_resize.png"
        # new标识坐标
        self.new_coordinate_list = [
            (135,50),(244,50),(350,50),(456,50),(562,50),
            (180,194),(289,194),(395,194),(501,194),(607,194),
        ]

    def build_card(self,result,extra):
        """
        十连建造-图片合成
        :params result: 抽中的舰娘数据,包括新增的舰娘船坞头像路径和是否需要new标识
        :return: build_card_path,合成后的十连建造图片路径
        :return: extra,额外参数
        """
        # 过滤皮肤誓约及改造
        if extra.get("skin","") == False:
            result_img_path = []
            for i in result:
                list_files = []
                for j in os.listdir(i["shipPath"]):
                    _ = j.rsplit(".",1)[0]
                    if "." not in _:
                        list_files.append(j)

                temp_path = os.path.join(i["shipPath"],random.choice(list_files))
                result_img_path.append(temp_path)
        else:
            result_img_path = [os.path.join(i["shipPath"],random.choice(os.listdir(i["shipPath"]))) for i in result]
        # 图片路径
        img_ships_list = []
        for img_path in result_img_path:
            # img_path = r"D:\Code\BLHX\blhx_code\批量合成船坞头像\阿卡司塔.改_corner11.png"
            img_ship = Image.open(img_path)
            img_ship = img_ship.resize((91,128))
            img_ship = self.circle_corner(img_ship,radii=7)
            img_ships_list.append(img_ship)
        # img_ships_list = [Image.open(img_path) for img_path in result_img_path]

        # 十连建造背景
        img_build_bg = Image.open(self.img_build_bg_path)
        # new标识
        new = Image.open(self.new_ico_path)
        # 图片坐标
        coordinate_list = [
            (114,89),(223,89),(329,89),(435,89),(541,89),
            (159,233),(268,233),(374,233),(480,233),(586,233)
        ]

        # 粘贴船坞头像
        for i in range(len(img_ships_list)):
            img_build_bg.paste(img_ships_list[i], coordinate_list[i], mask=img_ships_list[i].split()[-1])

        # 后粘贴new标识
        for i in range(len(self.new_coordinate_list)):
            if result[i]["isNew"]:
                img_build_bg.paste(new, self.new_coordinate_list[i], mask=new.split()[-1])

        build_card_path = os.path.join(self.build_card_result_path,"{}.png".format(int(time.time())))
        img_build_bg.save(build_card_path,qulity=100)
        return build_card_path

    def circle_corner(self,img,radii):
        """
        圆角处理
        :param img: 源图象。
        :param radii: 半径，如：30。
        :return: 返回一个圆角处理后的图象。
        """
        # 画圆（用于分离4个角）
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