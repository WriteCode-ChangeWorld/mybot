import requests
import json
import random

# from basic.plus_res_directory import pdr


# bot_day_illust每日插件会引用到该函数,需要对每日插件进行修改
def get_img(word,limit=None,illust_level=None,num=None,retry_num=3):
	"""
	根据关键字返回1~3张图片

	limit: 最低收藏数
	"""
	# api_url = "http://127.0.0.1:1526/api/v2/random"
	api_url = "http://106.55.244.64:1526/api/v2/random"

	if not num:
		num = random.choice(list(range(1,4)))

	data = {
		"num":num,
		# "num":random.choice(list(range(1,6))),
		"extra":word,
		"limit":limit,
		"illust_level":illust_level,
	}
	print(data)
	try:
		resp = requests.post(api_url,data=data,timeout=10)
	except Exception as e:
		if retry_num > 0:
			return get_img(word=word,limit=limit,illust_level=illust_level,num=num,retry_num=retry_num-1)
		else:
			return None
	else:
		# print(resp.text)
		result = json.loads(resp.text)
		return result


# from bot_color_img import Bot_Color_Img
# Bot_Color_Img.parse_extra(msg)
class Color_Img:
	"""
	整合涩图插件,提供4种涩图输出模式
	mode:从支持的四种模式中选择一种并返回(反代直链)
	extra_params 额外支持的键:
		illust_level -- 指定稀有度,R/SR/SSR/UR其中一种
		limit -- 最低收藏数

	"""
	def __init__(self):
		# self.bot_name = type(self).__name__
        # self.workspace = pdr.get_plus_res(self.bot_name)
		# keyword[:2] keyword[-2:]
		self.keyword = "来点涩图"
		self.start_keyword = self.keyword[:2]
		self.end_keyword = self.keyword[-2:]

		self.basic_text = ""
		self.temp_eval = "self.{}('{}')"
		self.mode_info = {
			"r":"get_img",
			"gs":"gaussianblur_img",
			"qr":"qr_img",
			"p":"phantom_img"
		}
		self.help_info = """当前支持模式:\n""" +\
			""" 1.r -- 反代直链(默认)\n 2.gs -- 高斯模糊\n 3.qr -- 二维码\n 4.p -- 幻影坦克\n形如:来点涩图 -qr\n\n""" +\
			"""当前支持额外的键值\n1.illust_level\n 指定返回作品的稀有度,值可选R/SR/SSR/UR其中一种\n2.limit\n 指定返回作品的最低收藏数""" +\
			"""\n\n形如:来点涩图 -gs -limit=3000"""
		# eval(self.temp_eval.format("parse_extra",self.keyword))

	def parse_extra(self,msg):
		"""
		从msg中解析出参数键值 
		"""
		parse_result = {}
		# 指定tag
		if msg[:4] == self.keyword:
			parse_result["word"] = ""
		else:
			parse_result["word"] = msg.split(self.start_keyword)[-1].split(self.end_keyword)[0]

		# 获取并整合键值对
		for k_v in msg.split(" ")[1:]:
			split_list = k_v.split("=")
			k = split_list[0].replace("-","")
			if len(split_list) == 1:
				v = ""			
			else:
				v = split_list[1]
			parse_result[k] = v

		# {'word': '原创', 'help': '', 'qr': '', 'illust_level': 'SSR', 'limit': '1000'}

		# 检查是否有help
		if "help" in list(parse_result.keys()):
			return {"help":self.help_info}

		# 检查mode
		temp_list = []
		# 倒序遍历删除 & 添加
		for k in list(parse_result.keys())[::-1]:
			if k in list(self.mode_info.keys()):
				temp_list.append(k)
				del parse_result[k]
				continue

		if not temp_list:
			mode = "r"
		else:
			# 再次翻转,顺序恢复
			mode = temp_list[::-1][0]

		# 检查extra
		result = self.get_img(parse_result)
		print(parse_result,temp_list,mode)
		return {
			"parse_result":parse_result,
			"temp_list":temp_list,
			"mode":mode
			}

	def service_func(self,eval_cqp_data):
		"""
		"""
		# 判断群
		pass

	# def get_img(self,word,limit=None,illust_level=None,num=None,retry_num=3):
	def get_img(self,parse_result:dict,retry_num:int=3)->dict:
		"""
		根据parse_result向PixiC API random接口发起请求

		limit: 最低收藏数
		"""
		# api_url = "http://127.0.0.1:1526/api/v2/random"
		api_url = "http://112.74.90.108:1526/api/v2/random"

		if not num:
			num = random.choice(list(range(1,4)))

		data = {
			"num":num,
			# "num":random.choice(list(range(1,6))),
			"extra":word,
			"limit":limit,
			"illust_level":illust_level,
		}
		print(data)
		try:
			resp = requests.post(api_url,data=data,timeout=10)
		except Exception as e:
			if retry_num > 0:
				# return get_img(word=word,limit=limit,illust_level=illust_level,num=num,retry_num=retry_num-1)
				return get_img(word=word,limit=limit,illust_level=illust_level,num=num,retry_num=retry_num-1)
			else:
				return None
		else:
			# print(resp.text)
			try:
				result = json.loads(resp.text)
			except Exception as e:
				return None
			else:
				return result

	# TODO 2020年10月3日17:22:20
	# 更新返回模板数据,有tag情况下返回当前tag数据库存量
	def parse_img_data(eval_cqp_data):
		msg = eval_cqp_data["message"]
		word = msg[2:-2]
		result = get_img(word)
		# print("result",result)
		reply_group = {
			"group_id": eval_cqp_data['group_id'],
			# "message":"[CQ:at,qq={}]\n".format(eval_cqp_data["user_id"]) + msg
		}
		# 返回None
		if not result:
			msg = "网络爆炸惹~请重试"
			reply_group["message"] = "[CQ:at,qq={}]\n".format(eval_cqp_data["user_id"]) + msg
			return reply_group

		# 无结果返回
		if type(result["result"]) != type([]):
			msg = "{}\ntag:{} 暂无数据哦~".format(result["result"]["message"],word)
		else:
			msg = "\n".join([i["reverse_url"] for i in result["result"]])
			if word:
				msg += "\ntag:{} 共有{}张".format(word,result["count"])
		# print(msg)

		reply_group["message"] = "[CQ:at,qq={}]\n".format(eval_cqp_data["user_id"]) + msg
		print("color_img",reply_group)
		return reply_group


Bot_Color_Img = Color_Img()
"""
from bot_color_img import Bot_Color_Img
msg = "来点原创涩图 -qr -gs -Gs -gS -illust_level=SSR -limit=1000"
Bot_Color_Img.parse_extra(msg)
"""