import os
import json
import time
import random
import configparser

from Arsenal.basic.log_record import logger
# 2.0
from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.bot_gaussianblur_img import Bot_GasussianBlur_Img
# from color_img import get_img
from Arsenal.bot_color_img import get_img
from Arsenal.image import cat2pixiv

class Day_Illust:
	"""每日涩图"""
	# 1、功能类实例化对象时,要创建NewYearIllust.conf
	# 2、业务进行时,判断是否存在NewYearIllust.conf
	# --存在则判断是否为空,为空,则写入后再发送;反之判断是否存在该用户,存在则不发送,反之则写入后再发送
	# --不存在则创建文件(空,则写入后再发送)

	def __init__(self):
		self.bot_name = type(self).__name__
		self.plugin_level = 8

		self.flag = False
		
		# 本功能插件res目录 2.0
		self.plus_res_path = pdr.get_plus_res(self.bot_name)
		logger.debug("{} - {}".format(self.bot_name,self.plus_res_path))
		# self.plus_res_path = r"D:\Code\mybot\code\res\Day_Illust"

		self.person_file_path = os.path.join(self.plus_res_path,"NewYearIllust.conf")

		if not os.path.exists(self.person_file_path):
			open(self.person_file_path,"w")

		self.config = self.read_cfg()

		# ===== 业务数据 =====
		# 抽卡
		self.rare_set = {"R":0.55,"SR":0.26,"SSR":0.12,"UR":0.07}
		self.illust_level_pool = {"R":"★★☆☆☆ R稀有度","SR":"★★★☆☆ SR稀有度","SSR":"★★★★☆ SSR稀有度","UR":"★★★★★ UR稀有度"}
		# 最低阈值限制
		# self.limit_prob = 0.7
		# 通过的群
		self.pass_group_list = [1072957655,813614458,930858571,780849000]
		# 限制的群
		self.extra_group_list = [1072957655,813614458,780849000]
		# 随机事件数据
		self.blhx_random_filename = r"D:\Code\mybot\code\res\Day_Illust\day_illust_randomData.json"
		# 稀有度总分布最右边界值(0~1)
		self.pool_rare_set_sum = 1
		# 高斯模糊后的图片路径,方便上层进行调用
		self.new_path = ""

	def read_json(self):
		with open(self.blhx_random_filename,encoding="utf8") as f:
			return json.load(f)

	def read_cfg(self):
		"""
		重新读取用户配置文件
		"""
		self.config = configparser.ConfigParser()
		self.config.read(self.person_file_path,encoding="utf8")
		return self.config
		# return self.person_file_path

	def get_sections(self):
		"""
		返回用户配置文件中的所有section/用户节点
		:return: ['123456', '150801']
		"""
		return self.config.sections()

	def get_all_data(self):
		# 获取前先读取一遍,更新self.config
		self.config = self.read_cfg()
		sections_data = []
		for i in self.config.sections():
			sections_data.append(dict(self.config.items(i)))

		return sections_data

	def get_section_data(self,section_name):
		"""获取section_name的data,转化为dict"""
		self.config = self.read_cfg()

		now_data = {}
		for i in self.config.sections():
			if i == section_name:
				for j in self.config.options(i):
					now_data[j] = self.config.get(i,j)
		return now_data

	def check_express_data(self,key=None,value=None,express_key=None,express_value=None):
		"""
		是否存在满足key为value的section
		:params key: key1
		:params value: value1
		:params express_key: key2
		:params express_value: value2
		:return: True/False
		比如,检查conf中某个群是否有被选为天选之人的用户
		check_express_data(key="group_id",value="123455",express_key="is_koi",express_value=True)
		"""
		if not key or not express_key:
			return False

		for _ in self.get_all_data():
			if _.get(str(key),"") == str(value) and _.get(str(express_key),"") == str(express_value):
				# logger.info(_)
				return True
		return False

	def create_section(self,fusion_data:dict,diy_data:dict=None)->dict:
		"""
		以user_id创建一个默认用户节点
		:params fusion_data: 用户id及群id
		fusion_data = {"user_id":"123","group_id":"1072957655"}
		:params diy_data: 自定义默认创建数据
		"""
		section_name = str(fusion_data["user_id"]) + "-" + str(fusion_data["group_id"])
		# if diy_data:
		# 	data = diy_data
		# else:
		data = {
			'user_id': fusion_data["user_id"],
			'group_id': fusion_data["group_id"],
			# 是否触发过每日抽图
			'is_remind': "False",
			# 创建时间
			'date': time.strftime("%Y-%m-%d"),
			# 抽中每日x图的次数
			'count': "0",
			# 魔方数量
			'magic_thing': "0",
			# 天选之子
			'is_koi': "False",
			# 发言次数 
			# extra_prob额外概率通过读取后计算
			'msg_count': "0",
			# 抽中涩图之前的保留概率
			'retention_prob': "0.0"
		}
		self.read_cfg()
		try:
			self.config.add_section(section_name)
		except configparser.DuplicateSectionError as e:
			logger.info("已存在{}节点".format(section_name))
			return {}

		for k,y in data.items():
			self.config.set(section_name, str(k), str(y))

		# 写入cfg_name,重新读取
		self.config.write(open(self.person_file_path,"w"))
		# self.read_cfg()
		return data

	# 调用update_section时,会自动更新date
	def update_section(self,writedata:dict)->dict:
		"""
		上层先update再执行业务操作,出错回滚否则略过
		功能: 更新user_id节点的数据,上层写入需要添加date字段

		:param writedata: 更新数据
		:return: 原路返回writedata
		date字段由func创建
		"""
		writedata["date"] = time.strftime("%Y-%m-%d")
		section_name = str(writedata["user_id"]) + "-" + str(writedata["group_id"])
		self.read_cfg()
		logger.info("写入数据 | result: {}".format(writedata))
		for k,v in writedata.items():
			self.config.set(section_name, str(k), str(v))
			
		self.config.write(open(self.person_file_path,"w"))
		return writedata

	def judge_remind_main(self,fusion_data:dict)->dict:
		"""
		通过fusion_data判断是否需要创建节点及更改is_remind来触发Bot_Day_Illust的业务
		:parmas fusion_data: 用户id及群id
		:return: 用户节点信息
		"""
		users_data = self.get_all_data()
		sections_data = self.get_sections()
		section_name = "{}-{}".format(fusion_data["user_id"],fusion_data["group_id"])
		logger.info("judge_remind_main | section_name:{},sections_data:{}".format(section_name,len(sections_data)))
		
		# 目标节点不在配置文件节点列表中
		if section_name not in sections_data:
			logger.info("judge_remind_main | Empty Data:{}".format(section_name))
			result = self.create_section(fusion_data)
			return result
			
		date = time.strftime("%Y-%m-%d")
		u_data = [_ for _ in users_data if "{}-{}".format(str(_["user_id"]),str(_["group_id"])) == section_name][0]
		# 非今日日期,则进行签到
		if u_data["date"] != date:
			logger.info("judge_remind_main | Update Date")
			u_data['is_remind'] = "False"
			return u_data
		# 未触发过每日抽图
		elif u_data['is_remind'] == "False":
			logger.info("judge_remind_main | User is_remind False")
			return u_data
		else:
			logger.info("judge_remind_main | User is_remind True")
			return u_data

	def day_illust_process(self,eval_cqp_data):
		"""
		通过eval_cqp_data判断每日插件的功能是否进行
		:params eval_cqp_data: CQ数据包
		:return: 可直接发送的CQ消息/None
		"""
		group_id = eval_cqp_data.get("group_id",0)
		user_id = eval_cqp_data.get("user_id",0)
		# 上层作判断
		if user_id == 0 or group_id == 0:
			logger.info("uid or gid 0")
			return 

		if eval_cqp_data.get('message_type','') == 'group' and \
			group_id in self.pass_group_list:
			fusion_data = {"user_id":str(user_id),"group_id":str(group_id)}
			self.new_path = ""
			result = self.judge_remind_main(fusion_data)
			backup_result = result.copy()
			logger.info("本地数据 | result: {}".format(result))
			# logger.info("测试原始数据: {}".format(backup_result))

			# 触发每日插件
			if result.get("is_remind","") == "False":
				# 先更新,避免A用户第一条消息未处理完,A用户第二条消息跑到同个位置
				user_msg_count = int(result["msg_count"])
				is_koi = result["is_koi"]

				result["is_koi"] = "False"
				result["is_remind"] = "True"
				result["msg_count"] = "1"	# 清零昨天的,这是今天第一条
				self.update_section(result)

				# 确认随机数及稀有度
				prob = round(random.random(),3)
				# 排除0 | random.random() -> x in the interval [0, 1)
				if prob == 0:
					prob == 0.001
				# 发言增幅概率
				additional_prob = self.get_additional_prob(user_msg_count)
				# 天选之人概率
				koi_prob = 0.2 if is_koi == "True" else 0.0
				# 保留的增幅概率
				retention_prob = float(result["retention_prob"])
				logger.info("基础概率: {} 发言增幅概率: {} 天选之人概率: {} 保留概率: {}".format(\
					prob,additional_prob,koi_prob,retention_prob))

				# 抽取天选之人
				next_koi_text = ""
				if not self.check_express_data("group_id",group_id,"is_koi",True):
					next_koi_random = random.choice(list(range(100)))
					logger.info("next_koi_random 天选之人抽取概率: {}".format(next_koi_random))
					if next_koi_random == 50:
						# 按实际为准
						next_koi_text = "\n恭喜你被选为【天选之人】,明日抽卡概率上升20%"
						result["is_koi"] = "True"


				# 判断是否在限制群内
				limit_prob=0.0
				if group_id in self.extra_group_list:
					# 魔方
					magic_thing_count = random.choice(list(range(3,7)))
					result["magic_thing"] = str(int(result["magic_thing"]) + magic_thing_count)
					# 根据发言数/天选之人/保留概率,通过降低阈值的方式增加抽卡概率
					limit_prob = round(0.7 - additional_prob - koi_prob - retention_prob, 3)
					logger.info("最低阈值: {}".format(limit_prob))
					if limit_prob < 0.0:
						limit_prob = 0.0
					illust_level = self.get_rare_value(prob,limit_prob=limit_prob)
					logger.info("in limit group |illust_level: {}".format(illust_level))
				else:
					# 魔方
					magic_thing_count = random.choice(list(range(10,16)))
					result["magic_thing"] = str(int(result["magic_thing"]) + magic_thing_count)
					# 根据发言数/天选之人/保留概率,提高随机值以抽取高稀有度
					new_prob = prob + additional_prob + koi_prob + retention_prob
					new_prob = round(new_prob, 3)
					if new_prob >= 0.5:
						new_prob = 1 - new_prob
					if new_prob < 0:
						new_prob = 0.001
					illust_level = self.get_rare_value(new_prob)
					logger.info("not in limit group | illust_level: {}".format(illust_level))
				

				magic_thing_text = "\n\n今日抽到{}个魔方,共有{}个魔方".format(magic_thing_count,result["magic_thing"])
				prob_interval_static = "\n涩图区间 | random"
				pool_rare_set_sum = str(round(1-limit_prob,3))
				prob_interval_text = "\n 0—{}  |  {}".format(pool_rare_set_sum,prob)
				# logger.info(prob_interval_static,prob_interval_text)


				# 获取链接并高斯模糊
				if illust_level:
					illust_flag = True
					# 更新抽中涩图次数
					result["count"] = str(int(result["count"]) + 1)
					try:
						reverse_url,img_url = self.safe2pid_error(illust_level=illust_level)
						reverse_url = reverse_url.replace("https://","")
						new_path = GBImg.ready_img(img_url=img_url,radius=10)
						self.new_path = new_path
					except Exception as e:
						logger.info("get_pid_localtion",e)
						result["is_remind"] = "False"
						self.update_section(backup_result)
				# 未抽中
				else:
					illust_flag = False
					reverse_url,img_url,new_path = "","",""
					self.new_path = new_path


				# 可发送illust,但无高斯模糊图片路径返回
				# 使用原始数据
				if illust_flag == True and not new_path:
					self.update_section(backup_result)
					logger.info("NotGBImgPath backup_result: {}↓".format(backup_result))
					return 
				# 未抽到卡的模板消息
				# is_remind此时已为True,无需改动
				elif illust_flag == False:
					# retention_prob = 旧值 + additional_prob
					result["retention_prob"] = str(round(retention_prob + additional_prob,3))
					data = {
						"group_id":result["group_id"],
						"message":"[CQ:at,qq={}]\n".format(result["user_id"]) + 
									"非常抱歉,你的涩图已被群主没收~" + 
									magic_thing_text + 
									next_koi_text + 
									prob_interval_static + 
									prob_interval_text									
					}
					logger.info("Miss Img: {}".format(result))
				# 抽到卡的模板消息
				else:
					# retention_prob清零
					result["retention_prob"] = "0.0"
					date_hms = time.strftime("%Y-%m-%d %H:%M:%S")
					data = {
						"group_id":result["group_id"],
						"message":"[CQ:at,qq={}]\n".format(result["user_id"]) + 
									"现在是{}\n{}\n".format(date_hms,self.illust_level_pool[illust_level]) + 
									"[CQ:image,file=file:///{}]\n".format(new_path) + 
									"反代直链\n{}".format(reverse_url) + 
									magic_thing_text + 
									next_koi_text + 
									prob_interval_static + 
									prob_interval_text
					}

				# 未抽到卡/抽到卡 发送消息
				self.update_section(result)
				return data
			# 发言数统计
			elif result.get("is_remind","") == "True":
				result["msg_count"] = str(int(result["msg_count"]) + 1)
				extra_magic_set = {"lost":0.002,"get":0.005,"normal":0.993}
				prob = round(random.random(),3)

				r = self.get_rare_value(prob,rare_set=extra_magic_set)
				blhx_random_json = self.read_json()
				if r == "get":
					extra_magic_count = random.choice(list(range(1,4)))
					result["magic_thing"] = int(result["magic_thing"]) + extra_magic_count
					t_i_combo = random.choice(blhx_random_json["get_magic_msg"])
				elif r == "lost":
					extra_magic_count = 1
					result["magic_thing"] = int(result["magic_thing"]) - extra_magic_count
					t_i_combo = random.choice(blhx_random_json["lost_magic_msg"])
				else:
					extra_magic_count = ""
					data = ""

				if extra_magic_count:
					data = {
						"group_id":result["group_id"],
						"message":"[CQ:at,qq={}]\n".format(result["user_id"]) + 
									"[CQ:image,file={}]\n【随机事件】{}\n".format(t_i_combo["url"],t_i_combo["text"].format(extra_magic_count)) + 
									"反代直链:\n{}\n".format(t_i_combo["reverse_url"]) + 
									"当前魔方:{}个".format(result["magic_thing"])
					}
				logger.info("更新前总用户长度:{}".format(len(self.get_sections())))
				self.update_section(result)
				logger.info("更新后总用户长度:{}".format(len(self.get_sections())))
				return data

		# 不满足返回None
		logger.info("Not Found")
		return 

	def safe2pid_error(self,illust_level,count=5):
		"""获取pid,pid不存在则重新获取"""
		try:
			random_result = get_img(word="",limit=1000,illust_level=illust_level)["result"]
		except Exception as e:
			logger.info("safe2pid_error")
			logger.info(e)
			if count > 0:
				return self.safe2pid_error(illust_level=illust_level,count=count-1)
			else:
				return "",""
		else:
			if random_result:
				random_pid = random.choice(random_result)["pid"]
				random_pid = str(random_pid)
			# 请求成功,但返回的不是json数据 get_img会返回None
			else:
				logger.info("safe2pid_error")
				# logger.info(e)
				if count > 0:
					return self.safe2pid_error(illust_level=illust_level,count=count-1)
				else:
					return "",""

		# ecd=None, cat2pixiv出错会返回None
		try:
			random_pid_res = cat2pixiv(random_pid,extra=2,ecd=None)
		except Exception as e:
			logger.info("safe2pid_error")
			logger.info(e)
			if count > 0:
				return self.safe2pid_error(illust_level=illust_level,count=count-1)
			else:
				return "",""

		if not random_pid_res or "错误" in random_pid_res:
			if count > 0:
				return self.safe2pid_error(illust_level=illust_level,count=count-1)
			else:
				return "",""
		else:
			h = "https://pixiv.cat/"
			try:
				# 反代
				pid = random_pid_res["body"]["illustId"]
				# suffix = random_pid_res["body"]["urls"]["original"].split(".")[-1]
				suffix = "png"
				if random_pid_res["body"]["pageCount"] > 1:
					reverse_url = "{}{}-{}.{}".format(h,pid,1,suffix)
				else:
					reverse_url = "{}{}.{}".format(h,pid,suffix)
				img_url = random_pid_res["body"]["urls"]["small"]
			except Exception as e:
				logger.info("safe2pid_error")
				logger.info(e)
				if count > 0:
					return self.safe2pid_error(illust_level=illust_level,count=count-1)
				else:
					return "",""
			else:
				return reverse_url,img_url

		return "",""

	def get_rare_value(self,rare_random,limit_prob=0.0,rare_set=None):
		"""
		根据rare_set和rare_random确认归属稀有度
		每日插件对限制群组有最低阈值的限制,因此对原get_rare_value函数进行改动
        :params rare_random: 概率0~1,存在增幅后概率大于1的情况
        :params limit_prob: 最低阈值
        :params rare_set: 自定义概率分布列表
        :return: rare_value 稀有度
		get_rare_value(0.7) # 未限制(0~1)
		get_rare_value(1.7) # 未限制(0~1)
		get_rare_value(0.115,limit_prob=0.7) # 限制(0~0.3)
		get_rare_value(0.8,limit_prob=0.7) # 限制(0~0.3)
		get_rare_value(1.115,limit_prob=0.7) # 限制(0~0.3)
		get_rare_value(0.2,rare_set={"lost":0.05,"get":0.1,"normal":0.85}) # 指定分布且进行限制
		get_rare_value(1.2,rare_set={"lost":0.05,"get":0.1,"normal":0.85}) # 人为避免该情况
        """

        # 各稀有度占比,从小到大排序; 默认为0~7~19~45~100
		if not rare_set:
			rare_set = self.rare_set

		self.pool_rare_set_sum = round(1-limit_prob,3)
		pool_rare_set = dict(sorted(rare_set.items(),key=lambda i:i[-1]))
		# 针对最低阈值作调整
		for k,v in pool_rare_set.items():
			pool_rare_set[k] = round(v*(1-limit_prob),3)
		logger.info("get_rare_value | 稀有度分布 pool_rare_set: {}".format(pool_rare_set))
		logger.info("get_rare_value | 随机值 rare_random: {}".format(rare_random))

		start_rare = 0
		# 0~稀有度分布最右侧
		for k,v in pool_rare_set.items():
            # 各稀有度右侧边界值 = 上一次右侧边界值 + 本轮稀有度占比
			# logger.info(start_rare, round((start_rare + v),3))
			if start_rare < rare_random <= round((start_rare + v),3):
				rare_value = k
				return rare_value
			else:
				start_rare = round((start_rare + v),3)
		# 不在定义的稀有度分布中
		else:
			# rare_random大于pool_rare_set+limit_prob,则返回稀有度最高的级别,也就是占比最小的
			# line:517 self.pool_rare_set_sum = round(1-limit_prob,3)
			# self.pool_rare_set_sum = round(sum(list(pool_rare_set.values())),3)
			# 1~∞(额外概率,天选之人之类)
			if rare_random > round((self.pool_rare_set_sum + limit_prob),3):
				return list(pool_rare_set.keys())[0]
			# 稀有度分布最右侧~1
			else:
				return ""
				# return list(pool_rare_set.keys())[-1]

	def get_additional_prob(self,user_msg_count):
		"""根据发言数调节概率"""
		proportion = 0.004
		if user_msg_count > 50:
			additional_prob = 0.2
		else:
			additional_prob = proportion * user_msg_count
		return additional_prob
			

Bot_Day_Illust = Day_Illust()
"""
from bot_day_illust import Bot_Day_Illust
eval_cqp_data = {"group_id": 1072957655,"user_id":207,"message_type":"group"}
Bot_Day_Illust.day_illust_process(eval_cqp_data)
"""

"""
cqp.py调用
from bot_day_illust import Bot_Day_Illust,logger.info
Day_Illust_Data = Bot_Day_Illust.day_illust_process(eval_cqp_data)
logger.info("Day_Illust_Data:{}".format(Day_Illust_Data))

if Day_Illust_Data:
	time.sleep(0.08)
	requests.get(url=qunliao, params=Day_Illust_Data)
"""
"""
cqp.py调用 添加Arsenal
import sys,os
sys.path.append(os.path.join(os.getcwd(),"Arsenal"))
from Arsenal.bot_day_illust import Bot_Day_Illust
"""