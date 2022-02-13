# -*- encoding: utf-8 -*-
'''
@File    :   build_pool.py
@Time    :   2022/02/09 10:57:24
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import os
import random

from Arsenal.basic.file_handler import loadFile, dumpFile
from Arsenal.basic.log_record import logger


class Lucky_Ships_Pool:
    """构建卡池及建造函数"""
    def __init__(self, blhx_tool):
        self.blhx_tool = blhx_tool 
        # 池子名称与索引文件
        self.ship_key_data = self.read_json(self.blhx_tool.key_filepath)

    def get_random_num(self):
        """获取随机数"""
        return round(random.random(),4)

    def read_json(self,path):
        return loadFile.by_json(path)

    def reload_json_data(self,path):
        return dumpFile.by_json(path)

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
            # logger.info(start_rare,start_rare + v)
            if start_rare < rare_random <= round((start_rare + v),3):
                rare_value = k
                return rare_value
            else:
                start_rare = round((start_rare + v),3)
        else:
            # 防止无返回值,返回最低稀有度
            return list(pool_rare_set.keys())[-1]

    def get_lucky_ships(self, pool_name:str,
                              count:int=10,
                              multiple:int=1,
                              cheating_list:list=[])->list:
        """碧蓝航线模拟十连建造
        :params pool_name: 池子名称,如:轻型池/重型池/特型池
        :params count: 建造次数,最高10个
        :params multiple: 魔方-倍率参数
            消耗<multiple>个魔方提高舰娘判定概率<multiple>倍
        :return: 舰娘信息list ['科隆','榊','狐提','太原','小天鹅','科尔克','布什','狻','倔强','牙买加']
        """
        # [作弊]请使用本地数据内包含的舰娘名称,否则后果自负
        if cheating_list:
            logger.debug(f"<cheating!!!> - {cheating_list}")
            return cheating_list

        # 负数或次数大于10则返回
        if count > 10 or count <= 0:
            logger.warning(self.blhx_tool.err_temp["general_err"].format("count", count))
            return []

        # 读取对应池子索引数据
        self.ship_key_data = self.read_json(self.blhx_tool.key_filepath)
        # 读取对应池子数据
        pool_data_path = os.path.join(self.resource,self.ship_key_data.get(pool_name,""))
        pool_data = self.read_json(pool_data_path)

        # 池子数据中各个节点
        if pool_data.get("ships_list","") == "" or \
            pool_data.get("rare_set","") == "":
            logger.warning(self.blhx_tool.err_temp["general_err"].format("pool_data", pool_data))
            return ["pool_data_items_error"]

        # 舰娘建造结果
        lucky_result = []
        log_result = []
        # 对应建造次数
        for i in range(count):
            log_info = {}
            pool_ships_list = pool_data["ships_list"]
            pool_extra_data = pool_data["extra"]
            pool_rare_set = pool_data["rare_set"]

            # 确认稀有度
            rare_random = self.get_random_num()
            rare_value = self.get_rare_value(pool_rare_set,rare_random)
            log_info["rare_random"] = rare_random
            log_info["rare_value"] = rare_value

            # 确认是否抽中up舰娘
            up_ship_rare = self.get_random_num()
            log_info["up_ship_rare"] = up_ship_rare

            up_ship_list = pool_extra_data.get(rare_value,"")
            # 有up舰娘
            if up_ship_list:
                # 取up概率去重并转为list
                up_values = list(set(list(up_ship_list.values())))
                # 概率增幅multiple倍
                up_values = [_*multiple for _ in up_values]
                # 从低到高排序
                up_values.sort()
                log_info["up_values"] = up_values

                # 判断up_ship_rare是否有命中up
                up_ship_lucky_number = 0
                for _ in up_values:
                    if up_ship_rare <= _:
                        up_ship_lucky_number = round(_/multiple,3)
                        break

                # 有命中up舰娘
                if up_ship_lucky_number != 0:
                    same_lucky_number_ship = [k for k,v in up_ship_list.items() if v == up_ship_lucky_number]
                    if not same_lucky_number_ship:
                        # TODO
                        lucky_ship = random.choice(pool_ships_list[rare_value])
                    else:
                        lucky_ship = random.choice(same_lucky_number_ship)
                    log_info["lucky_ship"] = lucky_ship
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
                    log_info["lucky_ship"] = lucky_ship
                    lucky_result.append(lucky_ship)
            # 无up舰娘
            else:
                lucky_ship = random.choice(pool_ships_list[rare_value])
                log_info["lucky_ship"] = lucky_ship
                lucky_result.append(lucky_ship)

            log_result.append(log_info)
            logger.debug(f"第{i}发建造结果: {log_info}")

        # logger.info("log_result\n",log_result)
        # lucky_result = ['花园', '卡莉永', '树城', '喷水鱼', '雾城', '雾城', '花园', '花园', '卡莉永', '树城']
        # lucky_result = ['俄克拉荷马', '彭萨科拉', '安克雷奇', '奥古斯特·冯·帕塞瓦尔', '埃吉尔', '萨福克', '马可·波罗', '鹫', '俄克拉荷马', '内华达']
        logger.info(lucky_result)
        return lucky_result