import os
import time
from PIL import Image,ImageDraw,ImageFont

from basic.plus_res_directory import pdr

# 白色背景——ImageA——opacity=100%
# 黑色背景——ImageB——opacity=0%
# A图亮度大于B图亮度，提高A图/降低B图
class Phantom_Img:
    """
    生成一张表图+指定里图=幻影坦克
    """
    def __init__(self):
        self.bot_name = type(self).__name__
        self.workspace = pdr.get_plus_res(self.bot_name)
        self.ttf_path = os.path.join(self.workspace,"..","dy.ttf")
        # 表图text
        self.text = "点我看涩图"

    def get_font_size(self,img_size):
        """
        根据图片宽度与字体,得出合适的fontsize
        :params img_size: 图片大小,tuple
        :return: fontsize
        """
        # starting font size
        fontsize = 1
        # portion of image width you want text width to be
        img_fraction = 0.50

        font = ImageFont.truetype(self.ttf_path, fontsize)
        while font.getsize(self.text)[0] < img_fraction * img_size[0]:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype(self.ttf_path, fontsize)

        # optionally de-increment to be sure it is less than criteria
        fontsize -= 1
        return fontsize

    def main(self,img1_path):
        # 里图: 手机qq点开显示 上层
        img1 = Image.open(img1_path)
        img1_size = img1.size
        # 手机qq未点开显示 下层
        # 表图: 根据里图 新建一个图片并居中写入文字
        img2 = Image.new('RGB',img1.size)
        draw = ImageDraw.Draw(img2)
        # 调整表图字体
        fontsize = self.get_font_size(img1_size)
        font = ImageFont.truetype(self.ttf_path, fontsize)
        text_size = font.getsize(self.text)
        text_coordinate = int((img1_size[0]-text_size[0])/2), int((img1_size[1]-text_size[1])/2)
        draw.text(text_coordinate, self.text, (242,237,238), font)
        # 转为灰度图 mode
        img1_g = img1.convert("L")
        img2_g = img2.convert("L")
        # 调整大小
        img2_r = img2_g.resize((int(img1_g.width), int(img1_g.height)))
        img1_g = img1_g.resize((int(img1_g.width), int(img1_g.height)))
        # 调整亮度
        img1 = self.light_degree(img1_g, 0)
        img2 = self.light_degree(img2_r, 1)

        line = self.opposed_line(img2, img1)
        divided = self.divide(img1, line)

        final_path = self.final(divided, line)
        return final_path

    def light_degree(self,img,i):
        """
        调整图片整体亮度
        :params img: img对象
        :params i: 判定亮度增加或减少
        :return: 调整亮度后的img
        """
        if i > 0:
            img = img.point(lambda i: i * 1.1)
        else:
            img = img.point(lambda i: i * 0.3)
        return img

    def opposed_line(self, img2, img1):
        """
        同时进行反相与线性减淡操作
        :params img1: 里图
        :params img2: 表图
        """
        imgb = img2.load()
        imga = img1.load()
        for x in range(0, img2.width, 1):
            for y in range(0, img2.height, 1):
                # 逐点读取像素值
                b = imgb[x, y]
                a = imga[x, y]
                # (255-)b表示该像素点反相,(255-b)+a即为线性减淡运算
                color = (255-b+a,)
                # 避免线性减淡过程中有灰度值超过255的情况
                if color > (220,):
                    imgb[x, y] = (160 - b + a,)
                else:
                    imgb[x, y] = color
        return img2

    def divide(self, img1, imgO):
        # 划分操作,得到差异显著的里图
        imga = img1.load()
        imgo = imgO.load()
        for x in range(0, img1.width, 1):
            for y in range(0, img1.height, 1):
                A = imga[x, y]
                O = imgo[x, y]
                if O == 0:
                    color = (int(A*0.3),)
                elif A/O >= 1:
                    color = (int(A*6.2),)
                else:
                    color = (int(255*A/O),)
                imga[x, y] = color
        return img1

    def final(self, divided, line):
        """
        将反相与线性减淡过的表图的灰度值,添加到经过划分操作的里图A通道中
        """
        LINE = line.load()
        divided_RGBA = divided.convert("RGBA")
        DIV_RGBA = divided_RGBA.load()
        line = line.convert("RGBA")
        for x in range(0, line.width, 1):
            for y in range(0, line.height, 1):
                DIV_RGBA[x, y] = (DIV_RGBA[x, y][0], DIV_RGBA[x, y][1], 
                                    DIV_RGBA[x, y][2], LINE[x, y])
        # divided_RGBA.show()
        filename = str(int(time.time()))
        final_path = os.path.join(self.workspace,"{}.png".format(filename))
        divided_RGBA.save(final_path)
        return final_path

Bot_Phantom_Img = Phantom_Img() 

if __name__ == "__main__":
    # from bot_phantom_img import Bot_Phantom_Img
    # img1_path = r'D:\Code\mybot\code\res\Phantom_Img\85071750_p0.jpg'
    # img1_path = r'D:\Code\mybot\code\res\Phantom_Img\82028936_p0.jpg'
    img1_path = r'C:\Users\lenovo\Desktop\收藏\83887426_p0.png'
    Bot_Phantom_Img = Phantom_Img() 
    Bot_Phantom_Img.main(img1_path)