import os
import json
import random
import requests
from PIL import Image, ImageDraw, ImageFont

from Arsenal.basic.plugin_res_directory import pdr


class Blhx_Secretary:
    """碧蓝航线随机秘书抽取
    """
    def __init__(self):
        """初始化工作"""
        self.plugin_name = type(self).__name__
        self.api_url = "https://api.bilibili.com/x/activity/prediction"
        self.headers = {
            "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
        }
        self.point_list = list(range(10,110,10))
        self.ttf_path = "../res/dy.ttf"
        self.temporary_file_path = pdr.get_plus_res(self.plugin_name)
        # self.temporary_file_path = os.path.join(os.getcwd(),"../res/blhx")
        isExists = os.path.exists(self.temporary_file_path)
        if not isExists:os.mkdir(self.temporary_file_path)
        
    # def parse(self,eval_cqp_data->dict):->dict
    #     """解析函数"""
    #     pass

    def download_pic(self,path,info):
        """下载图片"""
        resp_content = requests.get(info["pic"],headers=self.headers,timeout=10).content
        with open(path,"wb") as f:
            f.write(resp_content)

    def get_pic_favor(self,nickname):
        """
        简要注明函数功能
        
        :param word:输入的单词
        :return: 返回生成的单词字典
        """
        params = {
            "sid":"11947",
            # 这里用昵称,写在图片上用qq号
            "nickname":nickname,
            "point":random.choice(self.point_list),
        }
        print(params)
        try:
            # 2.0改为使用基础模块,基础模块增加下载文件Func
            resp = requests.get(self.api_url,headers=self.headers,params=params,timeout=10)
        except Exception as e:
            resp = ""
        if not resp:
            return None

        try:
            result = json.loads(resp.text)
        except Exception as e:
            print("json解析错误")
            return None

        if result["data"] == None or result["code"] != 0:
            return None

        pic = "{}{}".format("http:",result["data"]["157"]["image"])
        favor = str(result["data"]["160"]["desc"])

        return {"pic":pic,"favor":favor}

    def add_text(self,path,new_path,point_text_list):
        # ttf_path = "./res/dy.ttf"
        # ttf_path = "../res/dy.ttf"
        img = Image.open(path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.ttf_path,30)
        for text in point_text_list:
            draw.text(text["point"],text["char"],"black",font)

        img.save(new_path)
        return new_path

    def main(self,eval_cqp_data):
        """主函数"""
        # 获取CQ数据包
        
        nickname = eval_cqp_data.get("sender","None")["nickname"]
        info = self.get_pic_favor(nickname)
        if info:
            filename = info["pic"].rsplit("/",1)[-1]
            path = os.path.join(self.temporary_file_path,filename)
            new_path = os.path.join(self.temporary_file_path,filename)
            point_text_list = [
                {"point": (440,970),"char": str(eval_cqp_data["user_id"])},
                {"point": (624,953),"char": info['favor']},
            ]

            self.download_pic(path,info)
            self.add_text(path,new_path,point_text_list)
            data = {
                "group_id": eval_cqp_data["group_id"],
                "message":"[CQ:at,qq={}]\n今天侍奉你的秘书舰为".format(eval_cqp_data["user_id"]) + 
                          "[CQ:image,file=file:///{}]".format(new_path),
            }
        else:
            data = {
                "group_id": eval_cqp_data["group_id"],
                "message":"[CQ:at,qq={}]\n接口错误,请联系master".format(eval_cqp_data["user_id"])
            }
        
        return data,path,new_path
        # requests.get()
        # if new_path:
        #     os.remove(path)
        #     os.remove(new_path)

Bot_Blhx_Secretary = Blhx_Secretary()

# 测试数据
# eval_cqp_data = {"group_id":123, "user_id":5101314, "sender":{"nickname":"桜花树下宇焉酱"}}
# Bot_Blhx_Secretary.main(eval_cqp_data)
# ============ 调用demo——添加文字 ============
# path = r"C:\Users\lenovo\Desktop\test.jpg"
# new_path = r"C:\Users\lenovo\Desktop\test1.jpg"
# favor = str(random.choice(Bot_Blhx_Secretary.point_list))
# point_text_list = [
#     {"point": (420,970),"char": "1508015265"},
# 	  {"point": (627,953),"char": favor},
# ]
# Bot_Blhx_Secretary.add_text(path,new_path,point_text_list)
# ============ 调用demo——添加文字 ============

"""
上层调用
from blhx_prediction import Bot_Blhx_Secretary
if eval_cqp_data.get('group_id','') in [1072957655,813614458,965302904,780849000]:
    # 随机概率 > 中奖阈值
    if prob >= limit_prob:
        blhx_data,blhx_path,blhx_new_path = Bot_Blhx_Secretary.main(eval_cqp_data)
        print(blhx_data)
        time.sleep(0.01)
        requests.get(url=qunliao, params=blhx_data)
        if blhx_new_path:
            os.remove(blhx_path)
            os.remove(blhx_new_path)
"""