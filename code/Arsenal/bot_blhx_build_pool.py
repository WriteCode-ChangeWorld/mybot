# -*- encoding: utf-8 -*-
'''
@File    :   bot_blhx_build_pool.py
@Time    :   2021/03/30 17:30:10
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   碧蓝航线十连建造
'''

# here put the import lib
import os
import copy
import json
import time
import random
from PIL import Image,ImageDraw
from collections import Counter

from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.bot_day_illust import Day_Illust

class Lucky_Ships_Pool:
    """构建卡池及建造函数"""
    def __init__(self,workspace):
        # 工作区/资源存放区
        # 自定义
        self.workspace = workspace
        # 池子名称与索引文件
        self.ship_key_filename = "pool_key.json"
        self.ship_key_data = self.read_json(os.path.join(self.workspace,self.ship_key_filename))

        # 池子数据与池子名称文件
        # self.ship_data_filename = "pool_data.json"
        # self.ship_data = self.read_json(os.path.join(self.workspace,self.ship_data_filename))

    def get_random_num(self):
        """获取随机数"""
        return round(random.random(),4)

    def read_json(self,path):
        with open(path,encoding="utf8") as f:
            return json.load(f)

    def reload_json_data(self,path,new_data):
        with open(path, 'w')as f:
            json.dump(new_data,f)

        return self.read_json(path)

    def get_rare_value(self,pool_rare_set,rare_random):
        """
        根据pool_rare_set和rare_random确认归属稀有度
        :params pool_rare_set: 池子数据-稀有度划分
        :params rare_random: 随机数0~1
        :return: rare_value 稀有度
        """
        # 默认为0~7~19~45~100
        # 各稀有度占比,从小到大排序
        pool_rare_set = dict(sorted(pool_rare_set.items(),key=lambda i:i[-1]))
        start_rare = 0
        for k,v in pool_rare_set.items():
            # 各稀有度右侧边界值 = 上一次右侧边界值 + 本轮稀有度占比
            # print(start_rare,start_rare + v)
            if start_rare < rare_random <= round((start_rare + v),3):
                rare_value = k
                return rare_value
            else:
                start_rare = round((start_rare + v),3)
        else:
            # 防止无返回值,返回最低稀有度
            return list(pool_rare_set.keys())[-1]

    def get_lucky_ships(self,pool_name:str,count:int=10,multiple:int=1):
        """碧蓝航线模拟建造,默认十连
        :params pool_name: 池子名称,如:轻型池/重型池/特型池
        :params count: 建造次数,一次最高建造10个,默认10个
        :params multiple: 作弊参数,提高up舰娘的中奖概率multiple倍
        :return: 舰娘信息list ['科隆', '榊', '狐提', '太原', '小天鹅', '科尔克', '布什', '狻', '倔强', '牙买加']
        """
        # 负数或次数大于10则返回
        if count > 10 or count < 0:
            print("count error")
            return False

        pool_data_path = os.path.join(self.workspace,self.ship_key_data.get(pool_name,""))
        # 十连前进行一次读取
        self.ship_key_data = self.read_json(os.path.join(self.workspace,self.ship_key_filename))
        # 检查pool_name
        if pool_name not in list(self.ship_key_data.keys()) and \
            os.path.exists(pool_data_path):
            print(list(self.ship_key_data.keys()))
            return False
        else:
            pool_data = self.read_json(pool_data_path)
            # pool_rawname = self.ship_key_data[pool_name]
            # pool_data = self.ship_data[pool_rawname]

        # 提升倍数1~10
        # multiple超出范围 (-∞,0)(10,+∞)
        if multiple > 10 or multiple <= 0:
            print("multiple error")
            return False
        # (0,10] 提升概率时,需判断池子是否有up舰娘
        elif multiple != 1:
            # 无up舰娘
            if pool_data.get("extra","") == {}:
                print("pool_data_not_extra")
                return False

        # 池子数据中各个节点
        if pool_data.get("ships_list","") == "" or \
            pool_data.get("extra","") == "" or \
            pool_data.get("rare_set","") == "":
            print("pool_data_item_null")
            return "pool_data_items_error"

        lucky_result = []
        log_result = []
        # 对应建造次数
        for i in range(count):
            log_info = {}
            # shipName
            pool_ships_list = pool_data["ships_list"]
            pool_extra_data = pool_data["extra"]
            pool_rare_set = pool_data["rare_set"]

            # 确认稀有度
            rare_random = self.get_random_num()
            rare_value = self.get_rare_value(pool_rare_set,rare_random)
            log_info["rare_random"] = rare_random
            log_info["rare_value"] = rare_value
            # print("抽取稀有度的概率",rare_random,rare_value)

            # 确认是否抽中up舰娘
            up_ship_rare = self.get_random_num()
            up_ship_list = pool_extra_data.get(rare_value,"")
            log_info["up_ship_rare"] = up_ship_rare
            # print("抽取舰娘的概率",up_ship_rare)

            # 有up舰娘
            if up_ship_list:
                # 取up概率去重并转为list
                up_values = list(set(list(up_ship_list.values())))
                # 概率增幅multiple倍
                up_values = [_*multiple for _ in up_values]
                # 从低到高排序
                up_values.sort()
                log_info["up_values"] = up_values
                # print("up概率:",up_values)

                # 判断up_ship_rare是否有命中up
                up_ship_lucky_number = 0
                for _ in up_values:
                    if up_ship_rare <= _:
                        up_ship_lucky_number = round(_/multiple,3)
                        break

                # 有命中up舰娘
                if up_ship_lucky_number != 0:
                    same_lucky_number_ship = [k for k,v in up_ship_list.items() if v == up_ship_lucky_number]
                    lucky_ship = random.choice(same_lucky_number_ship)
                    # print(same_lucky_number_ship)
                    # print(up_ship_lucky_number)
                    # print(lucky_ship)
                    lucky_result.append(lucky_ship)
                # 没有命中up舰娘
                else:
                    # 将up舰娘从pool_ships_list中删除
                    pool_ships_list_now = pool_ships_list[rare_value][::]
                    for ship in pool_ships_list_now[::-1]:
                        if ship in list(pool_extra_data[rare_value].keys()):
                            pool_ships_list_now.remove(ship)

                    # 随机选取一个对应稀有度的非up舰娘
                    lucky_ship = random.choice(pool_ships_list_now)
                    lucky_result.append(lucky_ship)
            # 无up舰娘
            else:
                lucky_ship = random.choice(pool_ships_list[rare_value])
                lucky_result.append(lucky_ship)

            log_result.append(log_info)
            print(log_info)
            # print(lucky_ship,"\n")

        # print("log_result\n",log_result)
        # lucky_result = ['花园', '卡莉永', '树城', '喷水鱼', '雾城', '雾城', '花园', '花园', '卡莉永', '树城']
        # lucky_result = ['俄克拉荷马', '彭萨科拉', '安克雷奇', '奥古斯特·冯·帕塞瓦尔', '埃吉尔', '萨福克', '马可·波罗', '鹫', '俄克拉荷马', '内华达']
        print(lucky_result)
        return lucky_result


class Build_Ships_Card:
    """合成十连界面"""
    def __init__(self,workspace):
        self.workspace = workspace
        # 十连建造合成后的输出目录
        self.build_card_result_path = os.path.join(self.workspace,"build_card_result")
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


class Blhx_Magic_Data:
    """用户舰娘图鉴管理"""
    def __init__(self,workspace):
        self.workspace = workspace
        self.user_ship_data_dir = os.path.join(self.workspace,"user_ship_data")
        if not os.path.exists(self.user_ship_data_dir):os.mkdir(self.user_ship_data_dir)

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


class Blhx_Build_Pool:
    # 业务上层判定,魔方大于0进行使用
    # from bot_blhx_build_pool import Bot_Blhx_Build_Pool
    # Bot_Blhx_Build_Pool.main(1508015265,extra={"pool":"活动池","multiple":10,"skin":False})
    """对接业务上层-碧蓝航线模拟十连建造"""
    def __init__(self):
        # plugin_level
        # self.plugin_level = 10

        # 服务器端自定义
        self.bot_name = type(self).__name__
        # D:\Code\mybot\code\res\Blhx_Build_Pool
        self.workspace = pdr.get_plus_res(self.bot_name)
        # self.workspace = r"C:\Users\Administrator\Desktop\CQA-tuling\python插件\coolq-trace_anime-master\res\Blhx_Build_Pool"

        self.BSC = Build_Ships_Card(self.workspace)
        self.LSP = Lucky_Ships_Pool(self.workspace)
        self.BMD = Blhx_Magic_Data(self.workspace)
        self.DIllust = Day_Illust()

        # 合成后的船坞头像目录
        self.root_dir = r"D:\Code\BLHX\workspace\静态素材\船坞头像"
        # 用户舰娘图鉴数据目录
        self.user_ship_data_dir = os.path.join(self.workspace,"user_ship_data")
        if not os.path.exists(self.user_ship_data_dir):os.mkdir(self.user_ship_data_dir)

        self.ships_all_data_filename = r"D:\Code\BLHX\blhx_code\res\ships_all_data.json"
        # self.ships_all_data_filename = os.path.join(self.workspace,"ships_all_data.json")
        self.ships_all_data = json.load(open(self.ships_all_data_filename,encoding="utf8"))
        # 用户数据
        self.user_now_data = {}

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

    def service_func(self,eval_cqp_data):
        # 业务端逻辑
        # service
        if eval_cqp_data.get('message_type','') == 'group':
            group_id = eval_cqp_data["group_id"]
            user_id = eval_cqp_data["user_id"]
            message = eval_cqp_data['message']

            split_words = message.split(" ")
            keyword = "一键十连"
            poolList = "info"
            # 活动更新在这里改动
            activity_pool_info = "「镜位螺旋」"
            support_multiple_pools = ["活动池"]
            data = {
                "group_id": group_id,
                "message":""
            }

            # 未触发关键词
            if split_words[0] != keyword:
                return 

            # 1.是否能查询到用户数据-魔方
            section_name = str(user_id) + "-" + str(group_id)
            self.user_now_data = self.DIllust.get_section_data(section_name)
            if self.user_now_data == {}:
                data["message"] = "[CQ:at,qq={}]\n未查询到数据".format(user_id)
                return data

            # 整合传参
            extra_params = {}
            for word in split_words[1:]:
                k = word.split("=")[0].replace("-","")
                if k == poolList:
                    extra_params = poolList
                    break
                else:
                    v = word.split("=")[1]
                    extra_params[k] = v

            # 校验是否为poolList return
            if extra_params == poolList:
                poolList_Text = "可用池子:\n● " + "\n● ".join(list(self.LSP.ship_key_data.keys()))
                ships_user_data = self.BMD.r_blhx_data(extra_id=user_id)
                bookmark_rate = str(round(len(ships_user_data)/len(self.ships_all_data)*100,3)) + "%"
                data["message"] = """[CQ:at,qq={}]\n{}\n\n当前收藏率: {}\n当前魔方: {}个\n当前活动池: {}\n\n"""\
                                    .format(user_id,poolList_Text,bookmark_rate,
                                        str(self.user_now_data["magic_thing"]),activity_pool_info) +\
                                    """使用命令&相关文档 请访问: https://www.yuque.com/mybot/blhx\n--2021/6/1更新"""
                return data


            # ===== 额外参数值校验 =====
            # pool
            if extra_params.get("pool","") == "":
                extra_params["pool"] = "啥都能建池"
            # 池子不存在 return
            if extra_params["pool"] not in list(self.LSP.ship_key_data.keys()):
                data["message"] = "[CQ:at,qq={}]\n选择的【{}】池子不存在!\n可以使用'一键十连 -info'来查看详细信息".format(user_id,extra_params["pool"])
                return data

            # 2.魔方满足当前池子最低魔方需求
            # pool_limit_magic = 10
            if int(self.user_now_data["magic_thing"]) < 10:
                data["message"] = "[CQ:at,qq={}]\n魔方不足以十连\n当前魔方:{}个".format(user_id,str(self.user_now_data["magic_thing"]))
                return data

            # skin
            if str(extra_params.get("skin","")) == "0":
                extra_params["skin"] = False
            elif str(extra_params.get("skin","")) == "1":
                extra_params["skin"] = True
            elif str(extra_params.get("skin","")) == "":
                extra_params["skin"] = True
            else:
                data["message"] = "[CQ:at,qq={}]\n【skin】参数错误".format(user_id)
                return data

            # multiple
            if str(extra_params.get("m","")) == "":
                extra_params["m"] = 1
            elif str(extra_params.get("m","")) != "1":
                # 池子不支持提升multiple
                if extra_params["pool"] not in support_multiple_pools:
                    support_multiple_text = ",".join(support_multiple_pools)
                    data["message"] = "[CQ:at,qq={}]\n选择的【{}】池子不支持提升up舰娘出货倍率!\n仅{}支持".\
                        format(user_id,extra_params["pool"],support_multiple_text)
                    return data
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
                data["message"] = "[CQ:at,qq={}]\n参数错误,请检查参数".format(user_id)
                return data
            # ===== 额外参数值校验 =====

            print("extra_params",extra_params)
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

    def parse(self,msg):
        return msg + self.bot_name

Bot_Blhx_Build_Pool = Blhx_Build_Pool()