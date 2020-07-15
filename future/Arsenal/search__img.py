# coding=utf8
"""
搜图功能,开启搜图
"""
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

pass

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Img:
	# 搜图功能实现类,返回msg
	def __init__(self, api_key):
		# TODO(Coder-Sakura): 2020/07/13 15:52 后续使用配置类提供
		self.api_key = api_key
		self.search_image_url = "https://saucenao.com/search.php?db=999&output_type=2&\
					testmode=1&numres=16&api_key={}&&url={}"
		# 数据包字段
		self.eval_cqp_data = {}
		self.user_id = ""
		self.msg = ""
		self.message_type = ""
		# 实验性/正在开发的功能
		self.search_image_group_list = []
		self.search_image_list = []
		self.search_image_enable = "开启搜图"
		self.search_image_quit = "关闭搜图"
		self.reply_image = "搜图模式开启成功!\n发送图片或连续发图进行搜图吧~"
		# 观察者对此项进行监控,重复开启则进入限制模式
		self.reply_tip = "已开启搜图模式,请勿重复开启!\n(加入黑名单)"
		self.reply_image_quit = "搜图模式关闭成功!"
		# 观察者对此项进行监控,重复开启则进入限制模式
		self.reply_enable_search = "未启用搜图模式!请勿重复关闭!\n(加入黑名单)"
		self.reply_bot_quit = "检测到发送非图片信息\n搜图模式自动关闭"
		
	def parse(self, eval_cqp_data):
		# executor传入方法
		# 解析群聊/私聊
		self.eval_cqp_data = eval_cqp_data
		self.user_id = self.eval_cqp_data.get("user_id", "")
		self.msg = self.eval_cqp_data.get("message", "")
		self.message_type = self.eval_cqp_data.get("message_type", "")

		if message_type == "group":
			return self.img_group()
		elif message_type == "private":
			return self.img_private()

	def img_group(self):
		# 群聊搜图方法动作触发
		print(self.msg, self.search_image_group_list)

		# 消息 == 开启搜图模式命令
		if self.msg == self.search_image_enable:
			# 判断是否在搜图名单中,以及恶意开启
			# 开启搜图,未在搜图名单中 --> 添加
			if self.user_id not in self.search_image_group_list:
				self.search_image_group_list.append(user_id)
				return reply_image
			# 开启搜图,已在搜图名单中 --> 提示
			else:
				return reply_tip
		# 消息 == 图片
		elif msg.split(',')[0] == '[CQ:image':
			for i in search_image_group_list:
				if user_id == i:
					msg_url = msg.split("url=")[-1].replace("]", "")
					img_url = self.search_image_url.format(self.api_key, msg_url)
					# 搜图函数组装好搜图结果,返回文字信息
					return search_img(img_url, eval_cqp_data)
		# 消息 == 关闭搜图
		elif msg == search_image_quit:
			# 判断是否在搜图名单中,以及恶意关闭
			# 关闭搜图,在名单中,删除
			if user_id in search_image_group_list:
				for i in search_image_group_list[::-1]:
					if i == user_id:
						search_image_group_list.remove(i)
						return reply_image_quit
			# 关闭搜图,不在名单中,提示
			else:
				return reply_enable_search
		# 消息 == 其他
		else:
			# 搜图模式发送非图片信息,自动关闭
			print(msg)
			if user_id in search_image_group_list:
				if msg.split(',')[0] != "[CQ:image":
					for i in search_image_group_list[::-1]:
						if i == user_id:
							search_image_group_list.remove(i)
							return reply_bot_quit

	# TODO(Coder-Sakura): 2020/07/13 16:09 私聊搜图待添加
	def img_private(self):
		# 私聊搜图方法动作触发
		pass

	# TODO(Coder-Sakura) 2020/07/13 16:19 headers请求头待设置
	def search_img(self, img_url, eval_cqp_data):
		# 搜图功能函数
		# saucenao,ascii2d等
		# 前五个,60%相似度以上,原图链接多个取前三个,优先pixiv
		try:
			resp = json.loads(requests.get(img_url, timeout=5).text)
		except Exception as e:
			# TODO(Coder-Sakura) 2020/07/13 16:22 异常类统一处理返回结果
			print(e)
			return e



	def reverse_pixiv(self):
		# pixiv直链反代
		pass

image = Img()