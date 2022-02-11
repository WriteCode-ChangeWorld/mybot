# -*- encoding: utf-8 -*-
'''
@File    :   data_handler.py
@Time    :   2022/02/11 11:09:18
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import os
import copy
from collections import Counter


class Blhx_Magic_Data:
    """用户舰娘图鉴管理"""
    def __init__(self, blhx_tool):
        self.blhx_tool = blhx_tool
        
    def r_blhx_data(self,extra_id=None):
        """
        读取并返回用户舰娘图鉴数据
        :params extra_id: 额外指定的用户id
        :return 
        """
        if extra_id:
            user_id = str(extra_id)
        else:
            user_id = self.blhx_tool.mybot_data["sender"]["user_id"]

        # 查询用户舰娘数据
        self.user_data_path = os.path.join(self.blhx_tool.user_ship_data_dir,user_id)
        with open(self.user_data_path,"a+",encoding="utf8") as f:
            f.seek(0)
            read_ship_list = f.readlines()
            for i in range(len(read_ship_list)):
                read_ship_list[i] = read_ship_list[i].replace("\n","")
            return read_ship_list
    
    def w_blhx_data(self,datas):
        # data -> [{"shipName":"可畏","isNew":True}...]
        # r_blhx_data已处理user_data_path
        with open(self.user_data_path,"a+",encoding="utf8") as f:
            for d in datas:
                if d["isNew"] == True:
                    f.write("{}\n".format(d["shipName"]))

    def check_ship(self,ship_list,ship_data):
        """
        检查舰娘是否在
        :params ship_list: 抽取的十位舰娘
        ['科隆', '榊', '狐提', '太原', '小天鹅', '科尔克', '布什', '狻', '倔强', '布什']
        :params ship_data: 抽取舰娘的数据
        :return: 添加isNew字段后的ship_data
        """
        raw_data_after = dict(Counter(ship_list))
        # 重复元素-列表
        duplicate_list = [k for k,v in raw_data_after.items() if v >1]
        # 重复元素:重复次数-字典
        duplicate_item_dict = {k:v for k,v in raw_data_after.items() if v >1}
        user_magic_data = self.r_blhx_data()

        new_data = []
        for _ in ship_data:
            d = copy.deepcopy(_)
            # 用户已拥有该舰娘
            if d["shipName"] in user_magic_data:
                d["isNew"] = False
            # 处理多个相同舰娘,new标识展示问题
            elif d["shipName"] in duplicate_list:
                if duplicate_item_dict[d["shipName"]] < ship_list.count(d["shipName"]):
                    d["isNew"] = False
                else:
                    duplicate_item_dict[d["shipName"]] = duplicate_item_dict[d["shipName"]] - 1
                    d["isNew"] = True
            # 不重复也不在当前用户数据中
            else:
                d["isNew"] = True
            new_data.append(d)

        # 舰娘名称写入用户数据
        self.w_blhx_data(new_data)
        return new_data