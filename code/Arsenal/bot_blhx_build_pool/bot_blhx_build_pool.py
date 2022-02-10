# -*- encoding: utf-8 -*-
'''
@File    :   bot_blhx_build_pool.py
@Time    :   2021/03/30 17:30:10
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   碧蓝航线十连建造
'''

# here put the import lib
from email import message
import os
import copy
import json
import time
import random
from PIL import Image,ImageDraw
from collections import Counter

from Arsenal.basic.bot_tool import tool
from Arsenal.basic.plugin_class import PluginClass
from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.basic.log_record import logger
from Arsenal.bot_blhx_build_pool.blhx_tool import BLHX_Tool
from Arsenal.basic.msg_temp import PLUGIN_BLOCK, PLUGIN_IGNORE, MYBOT_ERR_CODE
# TODO from Arsenal.bot_day_illust.bot_day_illust import Day_Illust


class Lucky_Ships_Pool:
#     """构建卡池及建造函数"""
#     def __init__(self,workspace):
#         # 工作区/资源存放区
#         # 自定义
#         self.resource = workspace
#         # 池子名称与索引文件
#         self.ship_key_filename = "pool_key.json"
#         self.ship_key_data = self.read_json(os.path.join(self.resource,self.ship_key_filename))

#         # 池子数据与池子名称文件
#         # self.ship_data_filename = "pool_data.json"
#         # self.ship_data = self.read_json(os.path.join(self.resource,self.ship_data_filename))

#     def get_random_num(self):
#         """获取随机数"""
#         return round(random.random(),4)

#     def read_json(self,path):
#         with open(path,encoding="utf8") as f:
#             return json.load(f)

#     def reload_json_data(self,path,new_data):
#         with open(path, 'w')as f:
#             json.dump(new_data,f)

#         return self.read_json(path)

#     def get_rare_value(self,pool_rare_set,rare_random):
#         """
#         根据pool_rare_set和rare_random确认归属稀有度
#         :params pool_rare_set: 池子数据-稀有度划分
#         :params rare_random: 随机数0~1
#         :return: rare_value 稀有度
#         """
#         # 默认为0~7~19~45~100
#         # 各稀有度占比,从小到大排序
#         pool_rare_set = dict(sorted(pool_rare_set.items(),key=lambda i:i[-1]))
#         start_rare = 0
#         for k,v in pool_rare_set.items():
#             # 各稀有度右侧边界值 = 上一次右侧边界值 + 本轮稀有度占比
#             # print(start_rare,start_rare + v)
#             if start_rare < rare_random <= round((start_rare + v),3):
#                 rare_value = k
#                 return rare_value
#             else:
#                 start_rare = round((start_rare + v),3)
#         else:
#             # 防止无返回值,返回最低稀有度
#             return list(pool_rare_set.keys())[-1]

#     def get_lucky_ships(self,pool_name:str,count:int=10,multiple:int=1):
#         """碧蓝航线模拟建造,默认十连
#         :params pool_name: 池子名称,如:轻型池/重型池/特型池
#         :params count: 建造次数,一次最高建造10个,默认10个
#         :params multiple: 作弊参数,提高up舰娘的中奖概率multiple倍
#         :return: 舰娘信息list ['科隆', '榊', '狐提', '太原', '小天鹅', '科尔克', '布什', '狻', '倔强', '牙买加']
#         """
#         # 负数或次数大于10则返回
#         if count > 10 or count < 0:
#             print("count error")
#             return False

#         pool_data_path = os.path.join(self.resource,self.ship_key_data.get(pool_name,""))
#         # 十连前进行一次读取
#         self.ship_key_data = self.read_json(os.path.join(self.resource,self.ship_key_filename))
#         # 检查pool_name
#         if pool_name not in list(self.ship_key_data.keys()) and \
#             os.path.exists(pool_data_path):
#             print(list(self.ship_key_data.keys()))
#             return False
#         else:
#             pool_data = self.read_json(pool_data_path)
#             # pool_rawname = self.ship_key_data[pool_name]
#             # pool_data = self.ship_data[pool_rawname]

#         # 提升倍数1~10
#         # multiple超出范围 (-∞,0)(10,+∞)
#         if multiple > 10 or multiple <= 0:
#             print("multiple error")
#             return False
#         # (0,10] 提升概率时,需判断池子是否有up舰娘
#         elif multiple != 1:
#             # 无up舰娘
#             if pool_data.get("extra","") == {}:
#                 print("pool_data_not_extra")
#                 return False

#         # 池子数据中各个节点
#         if pool_data.get("ships_list","") == "" or \
#             pool_data.get("extra","") == "" or \
#             pool_data.get("rare_set","") == "":
#             print("pool_data_item_null")
#             return "pool_data_items_error"

#         lucky_result = []
#         log_result = []
#         # 对应建造次数
#         for i in range(count):
#             log_info = {}
#             # shipName
#             pool_ships_list = pool_data["ships_list"]
#             pool_extra_data = pool_data["extra"]
#             pool_rare_set = pool_data["rare_set"]

#             # 确认稀有度
#             rare_random = self.get_random_num()
#             rare_value = self.get_rare_value(pool_rare_set,rare_random)
#             log_info["rare_random"] = rare_random
#             log_info["rare_value"] = rare_value
#             # print("抽取稀有度的概率",rare_random,rare_value)

#             # 确认是否抽中up舰娘
#             up_ship_rare = self.get_random_num()
#             up_ship_list = pool_extra_data.get(rare_value,"")
#             log_info["up_ship_rare"] = up_ship_rare
#             # print("抽取舰娘的概率",up_ship_rare)

#             # 有up舰娘
#             if up_ship_list:
#                 # 取up概率去重并转为list
#                 up_values = list(set(list(up_ship_list.values())))
#                 # 概率增幅multiple倍
#                 up_values = [_*multiple for _ in up_values]
#                 # 从低到高排序
#                 up_values.sort()
#                 log_info["up_values"] = up_values
#                 # print("up概率:",up_values)

#                 # 判断up_ship_rare是否有命中up
#                 up_ship_lucky_number = 0
#                 for _ in up_values:
#                     if up_ship_rare <= _:
#                         up_ship_lucky_number = round(_/multiple,3)
#                         break

#                 # 有命中up舰娘
#                 if up_ship_lucky_number != 0:
#                     same_lucky_number_ship = [k for k,v in up_ship_list.items() if v == up_ship_lucky_number]
#                     lucky_ship = random.choice(same_lucky_number_ship)
#                     # print(same_lucky_number_ship)
#                     # print(up_ship_lucky_number)
#                     # print(lucky_ship)
#                     lucky_result.append(lucky_ship)
#                 # 没有命中up舰娘
#                 else:
#                     # 将up舰娘从pool_ships_list中删除
#                     pool_ships_list_now = pool_ships_list[rare_value][::]
#                     for ship in pool_ships_list_now[::-1]:
#                         if ship in list(pool_extra_data[rare_value].keys()):
#                             pool_ships_list_now.remove(ship)

#                     # 随机选取一个对应稀有度的非up舰娘
#                     lucky_ship = random.choice(pool_ships_list_now)
#                     lucky_result.append(lucky_ship)
#             # 无up舰娘
#             else:
#                 lucky_ship = random.choice(pool_ships_list[rare_value])
#                 lucky_result.append(lucky_ship)

#             log_result.append(log_info)
#             print(log_info)
#             # print(lucky_ship,"\n")

#         # print("log_result\n",log_result)
#         # lucky_result = ['花园', '卡莉永', '树城', '喷水鱼', '雾城', '雾城', '花园', '花园', '卡莉永', '树城']
#         # lucky_result = ['俄克拉荷马', '彭萨科拉', '安克雷奇', '奥古斯特·冯·帕塞瓦尔', '埃吉尔', '萨福克', '马可·波罗', '鹫', '俄克拉荷马', '内华达']
#         print(lucky_result)
#         return lucky_result
    pass


class Build_Ships_Card:
    # """合成十连界面"""
    # def __init__(self,workspace):
    #     self.resource = workspace
    #     # 十连建造合成后的输出目录
    #     self.build_card_result_path = os.path.join(self.resource,"build_card_result")
    #     if not os.path.exists(self.build_card_result_path):os.mkdir(self.build_card_result_path)
    #     # 十连建造背景图片
    #     # self.img_build_bg_path = r"D:\Code\BLHX\workspace\静态素材\建造背景_bg\build_bg_final_2.png"
    #     self.img_build_bg_path = r"D:\Code\BLHX\workspace\静态素材\建造背景_bg\build_bg_final_2_RGBA.png"
    #     # new标识路径
    #     self.new_ico_path = r"D:\Code\BLHX\workspace\静态素材\new标识\new_resize.png"
    #     # new标识坐标
    #     self.new_coordinate_list = [
    #         (135,50),(244,50),(350,50),(456,50),(562,50),
    #         (180,194),(289,194),(395,194),(501,194),(607,194),
    #     ]

    # def build_card(self,result,extra):
    #     """
    #     十连建造-图片合成
    #     :params result: 抽中的舰娘数据,包括新增的舰娘船坞头像路径和是否需要new标识
    #     :return: build_card_path,合成后的十连建造图片路径
    #     :return: extra,额外参数
    #     """
    #     # 过滤皮肤誓约及改造
    #     if extra.get("skin","") == False:
    #         result_img_path = []
    #         for i in result:
    #             list_files = []
    #             for j in os.listdir(i["shipPath"]):
    #                 _ = j.rsplit(".",1)[0]
    #                 if "." not in _:
    #                     list_files.append(j)

    #             temp_path = os.path.join(i["shipPath"],random.choice(list_files))
    #             result_img_path.append(temp_path)
    #     else:
    #         result_img_path = [os.path.join(i["shipPath"],random.choice(os.listdir(i["shipPath"]))) for i in result]
    #     # 图片路径
    #     img_ships_list = []
    #     for img_path in result_img_path:
    #         # img_path = r"D:\Code\BLHX\blhx_code\批量合成船坞头像\阿卡司塔.改_corner11.png"
    #         img_ship = Image.open(img_path)
    #         img_ship = img_ship.resize((91,128))
    #         img_ship = self.circle_corner(img_ship,radii=7)
    #         img_ships_list.append(img_ship)
    #     # img_ships_list = [Image.open(img_path) for img_path in result_img_path]

    #     # 十连建造背景
    #     img_build_bg = Image.open(self.img_build_bg_path)
    #     # new标识
    #     new = Image.open(self.new_ico_path)
    #     # 图片坐标
    #     coordinate_list = [
    #         (114,89),(223,89),(329,89),(435,89),(541,89),
    #         (159,233),(268,233),(374,233),(480,233),(586,233)
    #     ]

    #     # 粘贴船坞头像
    #     for i in range(len(img_ships_list)):
    #         img_build_bg.paste(img_ships_list[i], coordinate_list[i], mask=img_ships_list[i].split()[-1])

    #     # 后粘贴new标识
    #     for i in range(len(self.new_coordinate_list)):
    #         if result[i]["isNew"]:
    #             img_build_bg.paste(new, self.new_coordinate_list[i], mask=new.split()[-1])

    #     build_card_path = os.path.join(self.build_card_result_path,"{}.png".format(int(time.time())))
    #     img_build_bg.save(build_card_path,qulity=100)
    #     return build_card_path

    # def circle_corner(self,img,radii):
    #     """
    #     圆角处理
    #     :param img: 源图象。
    #     :param radii: 半径，如：30。
    #     :return: 返回一个圆角处理后的图象。
    #     """
    #     # 画圆（用于分离4个角）
    #     circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    #     # circle = Image.new('RGBA', (radii * 2, radii * 2))  # 创建一个黑色背景的画布
    #     draw = ImageDraw.Draw(circle)
    #     draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
    #     # 原图
    #     img = img.convert("RGBA")
    #     w, h = img.size

    #     # 四角
    #     alpha = Image.new('L', img.size, 255)
    #     # 左上角
    #     alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
    #     # 右上角
    #     alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
    #     # 右下角
    #     alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))
    #     # 左下角
    #     alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))
    #     # alpha.show()
        
    #     img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    #     return img
    pass


class Blhx_Magic_Data:
    """用户舰娘图鉴管理"""
    def __init__(self,workspace):
        self.resource = workspace
        # self.user_ship_data_dir = os.path.join(self.resource,"user_ship_data")
        # pdr.create_path(self.user_ship_data_dir)
        # if not os.path.exists(self.user_ship_data_dir):os.mkdir(self.user_ship_data_dir)

        # 用户数据文件
        self.user_data_path = ""
        # 用户id
        self.user_id = ""
        
    def r_blhx_data(self,extra_id=None):
        """
        读取并返回用户舰娘图鉴数据
        :params extra_id: 额外指定的用户id
        :return 
        """
        # 看最后消息是否全在该模块处理,再决定是否使用该段代码
        if extra_id:
            user_id = str(extra_id)
        else:
            user_id = self.user_id

        self.user_data_path = os.path.join(self.user_ship_data_dir,user_id)
        with open(self.user_data_path,"a+",encoding="utf8") as f:
            f.seek(0)
            read_ship_list = f.readlines()
            for i in range(len(read_ship_list)):
                read_ship_list[i] = read_ship_list[i].replace("\n","")
            return read_ship_list
    
    def w_blhx_data(self,datas):
        # data -> [{"shipName":"可畏","a":"b",...},{},{}...]
        # 写入
        # 无需再次拼接,调用r_blhx_data时已拼接当前用户的数据文件地址
        with open(self.user_data_path,"a+",encoding="utf8") as f:
            for d in datas:
                if d["isNew"] == True:
                    f.write("{}\n".format(d["shipName"]))

    def check_ship(self,user_id,raw_data,datas):
        """
        检查舰娘是否在
        :params user_id: int,十位舰娘名称
        :params raw_data: list,十位舰娘名称
        ['科隆', '榊', '狐提', '太原', '小天鹅', '科尔克', '布什', '狻', '倔强', '布什']
        :params datas: list,十位舰娘数据的列表
        :return: 添加isNew字段后的datas
        """
        self.user_id = str(user_id)
        raw_data_after = dict(Counter(raw_data))
        # 重复元素-列表
        duplicate_list = [k for k,v in raw_data_after.items() if v >1]
        # 重复元素+重复次数-字典,用于判断
        duplicate_item_dict = {k:v for k,v in raw_data_after.items() if v >1}
        user_magic_data = self.r_blhx_data()

        new_data = []
        for _ in datas:
            d = copy.deepcopy(_)
            # 舰娘存在当前用户数据中
            if d["shipName"] in user_magic_data:
                # print(1)
                d["isNew"] = False
            # 舰娘在重复名单中 + 重复元素列表中当前元素的计数小于原始数据列表的计数
            elif d["shipName"] in duplicate_list:
                if duplicate_item_dict[d["shipName"]] < raw_data.count(d["shipName"]):
                    # print(2)
                    d["isNew"] = False
                else:
                    # print(3)
                    d["isNew"] = True
                    duplicate_item_dict[d["shipName"]] = duplicate_item_dict[d["shipName"]] - 1
            else:
                # 不重复也不在当前用户数据中
                # print(4)
                d["isNew"] = True
            new_data.append(d)

        self.w_blhx_data(new_data)
        return new_data


class Blhx_Build_Pool(PluginClass):
    """碧蓝航线模拟十连建造 - 主类"""
    def __init__(self):
        super(PluginClass, self).__init__()
        # 必须
        self.plugin_name = type(self).__name__

        # 可选-插件别名 - 展示给用户,无则使用plugin_name
        self.plugin_nickname = "碧蓝航线-模拟建造插件(十连)"

        # 插件类型 - 1-主动式插件,0-被动式插件,默认1
        self.plugin_type = 1

        # 插件权限 - 10~999为主动式插件,1~9为被动式插件,默认为10
        # self.plugin_level = [v for k,v in {1: 10, 0: 5}.items() if self.plugin_type == k][0]
        self.plugin_level = 10
        
        # 静态资源文件目录
        self.resource_path = os.path.join(pdr.resource, "Blhx_Build_Pool")
        # TODO self.resource = r"C:\Users\Administrator\Desktop\CQA-tuling\python插件\coolq-trace_anime-master\res\Blhx_Build_Pool"
        
        # 插件工作目录
        self.workspace = pdr.get_plus_res(self.plugin_name)

        ####### 插件内部全局变量
        self.blhx_tool = BLHX_Tool(self.resource_path, self.workspace)

        # TODO
        self.BSC = Build_Ships_Card(self.blhx_tool)
        self.LSP = Lucky_Ships_Pool(self.blhx_tool)
        self.BMD = Blhx_Magic_Data(self.blhx_tool)
        self.DIllust = Day_Illust()

    def help_info(self):
        # 可用池
        poolList_Text = "\n● ".join(list(self.LSP.ship_key_data.keys()))
        # 收藏率
        ships_user_data = self.BMD.r_blhx_data(extra_id=self.mybot_data["sender"]["user_id"])
        bookmark_rate = str(round(len(ships_user_data)/len(self.ships_all_data)*100,3)) + "%"

        message = self.blhx_tool.text_temp["help"].format(
            poolList_Text, bookmark_rate, str(self.mybot_data["user_info"]["magic_thing"]),
            self.blhx_tool.activity_pool_info()["name"]
        )
        return message

    def find_ship_data(self,name):
        """
        1.返回舰娘数据
        2.根据舰娘名称找出对应船坞头像路径
        :params name: 舰娘名称
        :return: data{}
        data: {
            'shipName': '栭', 
            'shipRawName': '谷风', 
            'shipType': '驱逐', 
            'starLevelText': '稀有', 
            'starLevel': 'R', 
            'shipCamp': '重樱', 
            'shipNum': 'NO.319',
            'shipPath': 'D:\\Code\\BLHX\\workspace\\ship\\稀有\\栭'
            }
        """
        data = {}
        for _ in self.ships_all_data:
            if _["shipName"] == name:
                data = _
                break

        if not data:
            return {}
        else:
            starLevelText = data["starLevelText"]
            if starLevelText in ["最高方案","海上传奇","决战方案"]:
                starLevelText = "超稀有"
            shipPath = os.path.join(self.root_dir,starLevelText,data["shipName"])
            data["shipPath"] = shipPath
            return data

    # def main(self,user_id,pool_name,multiple=1,extra={}):
    def main(self,user_id,extra={}):
        """
        碧蓝航线插件主流程
        BBP.main(1308294765,"啥都能建池")
        :params user_id: 用户id
        :params extra: 额外参数
        :return: 合成后的十连图片路径


        :params pool_name: 池子名称ZH
        :params multiple: up池概率提升倍率,默认1
        """
        # 额外参数为空
        if extra == {}:
            print("Extra Params Error")
            return 
        # value有空值
        for k,v in extra.items():
            if v == "":
                print("Item Value Null:{}".format(extra))
                return 

        # ship_list = self.LSP.get_lucky_ships(pool_name=pool_name,multiple=multiple)
        try:
            ship_list = self.LSP.get_lucky_ships(pool_name=extra["pool"],multiple=extra["multiple"])
        except Exception as e:
            print("ship_list error:{}".format(e))
            ship_list = "pool_data_items_error"

        if ship_list == False:
            print("参数错误:{}".format(extra))
            return 
        elif ship_list == "pool_data_items_error":
            print("池子数据错误")
            return 500


        result = []
        for ship in ship_list:
            data = self.find_ship_data(name=ship)
            if data:
                result.append(data)
        
        # 有部分data为空,异常处理--待定
        if len(result) != 10:
            print("result.len < 10:\n",result)
            return 500

        # 经过舰娘图鉴处理
        result = self.BMD.check_ship(user_id,ship_list,result)
        # print("check_ship",result)
    
        # self.BSC.
        build_card_path = self.BSC.build_card(result,extra=extra)
        return build_card_path

    def check_param(self, extra_params):
        """额外参数值校验
        return True or False
        """
        # pool
        if extra_params.get("pool","") == "":
            extra_params["pool"] = "啥都能建池"

        # 无效建造池
        if extra_params["pool"] not in list(self.LSP.ship_key_data.keys()):
            self.mybot_data["message"] = "选择的【{}】池子不存在!\n可以使用'一键十连 -info'来查看详细信息".format(extra_params["pool"])
            tool.auto_send_msg(self.mybot_data)
            return PLUGIN_BLOCK

        # 2.魔方满足当前池子最低魔方需求
        # pool_limit_magic = 10
        if int(self.mybot_data["user_info"]["magic_thing"]) < 10:
            self.mybot_data["message"] = "魔方不足以十连\n当前魔方:{}个".format(str(self.user_now_data["magic_thing"]))
            tool.auto_send_msg(self.mybot_data)
            return PLUGIN_BLOCK

        # skin
        if str(extra_params.get("skin","")) == "0":
            extra_params["skin"] = False
        elif str(extra_params.get("skin","")) == "1":
            extra_params["skin"] = True
        elif str(extra_params.get("skin","")) == "":
            extra_params["skin"] = True
        else:
            self.mybot_data["message"] = "【skin】参数错误"
            tool.auto_send_msg(self.mybot_data)
            return PLUGIN_BLOCK

        # multiple
        if str(extra_params.get("m","")) == "":
            extra_params["m"] = 1
        elif str(extra_params.get("m","")) != "1":
            # 池子不支持提升multiple
            if extra_params["pool"] not in self.blhx_tool.support_multiple_pools:
                support_multiple_text = ",".join(self.blhx_tool.support_multiple_pools)
                self.mybot_data["message"] = "选择的【{}】池子不支持提升up舰娘出货倍率!\n仅{}支持".\
                    format(extra_params["pool"],support_multiple_text)
                tool.auto_send_msg(self.mybot_data)
                return PLUGIN_BLOCK
            # # 非数字
            # try:
            #     extra_params["multiple"] = int(extra_params["multiple"])
            # except:
            #     data["message"] = "[CQ:at,qq={}]\n参数错误,请检查参数".format(user_id)
            #     return data

        try:
            extra_params["m"] = int(extra_params["m"])
            extra_params["multiple"] = extra_params["m"]
        except:
            self.mybot_data["message"] = "参数错误,请检查参数"
            tool.auto_send_msg(self.mybot_data)
            return PLUGIN_BLOCK

    def parse(self, mybot_data):
        self.mybot_data = mybot_data
        if mybot_data["sender"].get('type','') == 'group':
            group_id = mybot_data["sender"]["group_id"]
            user_id = mybot_data["sender"]["user_id"]
            message = mybot_data["arrange"]['message']
            split_words = message.split(" ")

            # 活动更新在这里改动
            # activity_pool_info = "「镜位螺旋」"

            # 基本关键词检测
            if split_words[0] != self.blhx_tool.keyword:
                return PLUGIN_IGNORE

            # 查询到用户数据
            self.blhx_tool.user_now_data = mybot_data["user_info"]
            if not self.blhx_tool.user_now_data:
                mybot_data["message"] = "未查询到用户相关数据"
                tool.auto_send_msg(mybot_data)
                # 结束消息周期
                return PLUGIN_BLOCK

            # 整合传参
            extra_params = {}
            for word in split_words[1:]:
                k = word.split("=")[0].replace("-","")
                if k == self.blhx_tool.keyword_help:
                    extra_params = k
                    break
                else:
                    v = word.split("=")[1]
                    extra_params[k] = v

            # help
            if extra_params == self.blhx_tool.keyword_help:
                self.mybot_data["message"] = self.help_info()
                tool.auto_send_msg(self.mybot_data)
                # 结束消息周期
                return PLUGIN_BLOCK

            # 检查参数
            if not self.check_param(extra_params):
                # 结束消息周期
                return PLUGIN_BLOCK
            
            logger.info(MYBOT_ERR_CODE["Generic_Value_Info"].format("extra_params",extra_params))

            build_card_path = self.main(user_id=user_id,extra=extra_params)
            # 服务端错误
            if build_card_path == 500:
                data["message"] = "[CQ:at,qq={}]\n池子数据出错啦,艾特Master去修复一下吧...".format(user_id)
                return data
            # 参数错误
            elif build_card_path == None:
                data["message"] = "[CQ:at,qq={}]\n参数错误,请检查参数".format(user_id)
                return data
            # 十连合成图片路径.png
            elif type(build_card_path) == type("t") and ".png" in build_card_path:
                # 扣除魔方
                magic_cost = 10
                if int(extra_params["multiple"]) > 1:
                    magic_cost = 10 + int(extra_params["multiple"])
                
                self.user_now_data["magic_thing"] = str(int(self.user_now_data["magic_thing"]) - magic_cost)
                self.DIllust.update_section(self.user_now_data)

                ships_user_data = self.BMD.r_blhx_data(extra_id=user_id)
                bookmark_rate = str(round(len(ships_user_data)/len(self.ships_all_data)*100,3)) + "%"
                data["message"] = "[CQ:at,qq={}]\n当前池子: {}\n".format(user_id,extra_params["pool"]) +\
                                    "欧尼酱,我听到你的召唤了!\n[CQ:image,file=file:///{}]".format(build_card_path) +\
                                    "\n本次消耗{}个魔方,剩余魔方{}个".format(magic_cost,self.user_now_data["magic_thing"]) +\
                                    "\n当前收藏率:{}".format(bookmark_rate)
                return data

    def parse1(self,mybot_data):
        if mybot_data == "test2":
            print(f"{mybot_data + self.plugin_name}")
            return 0

Bot_Blhx_Build_Pool = Blhx_Build_Pool()