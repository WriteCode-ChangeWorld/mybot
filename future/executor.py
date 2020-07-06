import json

from image import tra_images,tra_images_group,cat2pixiv



# 配置文件
config = json.load(open("config.json",encoding='utf-8-sig'))
api_key = config['api_key']					# saucenao api_key
tarce_message = config['tarce_message']  	# 搜番
search_message = config['search_message']   # 搜图
setu_message = config['setu_message']  		# 来点x图命令
setu_path = config['setu_path']  			# x图地址,后续取消
count_setu = config['count_setu']  			# 统计x图
search_pid_info = config['search_pid_info'] # 查询pid
coolq_http_api_ip = config['coolq_http_api_ip']
coolq_http_api_port = config['coolq_http_api_port']

# 酷Q http插件私聊推送url
siliao = "http://{}:{}/send_private_msg?".format(coolq_http_api_ip,coolq_http_api_port)
# 酷Q http插件群聊推送url
qunliao = "http://{}:{}/send_group_msg?".format(coolq_http_api_ip,coolq_http_api_port)

# 实验性/正在开发的功能
search_image_enable = "开启搜图"
search_image_quit = "关闭搜图"
search_image_group_list = []
search_image_list = []
reply_image = "搜图模式开启成功!\n发送图片或连续发图进行搜图吧~"
reply_tip = "已开启搜图模式,请勿重复开启!\n(加入黑名单)"	# 观察者对此项进行监控,重复开启则进入限制模式
reply_image_quit = "搜图模式关闭成功!"
reply_bot_quit = "检测到发送非图片信息\n搜图模式自动关闭"
reply_enable_search = "未启用搜图模式!请勿重复关闭!\n(加入黑名单)"

class Executor:
	def __init__(self):
		self.reply_group = {}
		self.reply = {}
		# trace.moe的api地址
		self.trace_moe_url = 'https://trace.moe/api/search?url='
		# saucenao的API地址
		self.search_image_url = "https://saucenao.com/search.php?db=999&output_type=2&\
					testmode=1&numres=16&api_key={}&&url={}"



	def task_parse(self,eval_cqp_data):
		# 模板消息
		if eval_cqp_data["message_type"] == "group":
			self.reply_group = {"group_id": eval_cqp_data['group_id']}
		elif eval_cqp_data["message_type"] == "private":
			self.reply = {"user_id": eval_cqp_data['user_id']}

		msg = eval_cqp_data["message"]
		user_id = eval_cqp_data["user_id"]

		# 开启搜图
		if msg == search_image_enable:
			return self.search_image(eval_cqp_data)
		# 结束搜图
		if msg == search_image_quit:
			return self.search_image(eval_cqp_data)

		# 在搜图名单中
		if user_id in search_image_group_list:
			return self.search_image(eval_cqp_data)

	def search_image(self,eval_cqp_data):
		user_id= eval_cqp_data["user_id"]
		message_type = eval_cqp_data["message_type"]
		msg = eval_cqp_data["message"]

		# 开启搜图
		# 群聊
		if message_type == "group":
			print(msg,search_image_group_list)
			# 消息 == 开启搜图模式命令
			if msg == search_image_enable:
				# 判断是否在搜图名单中,以及恶意开启
				# 开启搜图,未在搜图名单中 --> 添加
				if user_id not in search_image_group_list:
					search_image_group_list.append(user_id)
					self.reply_group["message"] = reply_image
					return self.reply_group
				# 开启搜图,在搜图名单中 --> 提示
				else:
					self.reply_group["message"] = reply_tip
					return self.reply_group
			# 消息 == 图片
			elif msg.split(',')[0] == '[CQ:image':
				for i in search_image_group_list:
					if user_id == i:
						msg_url = msg.split("url=")[-1].replace("]","")
						url = self.search_image_url.format(api_key,msg_url)
						return tra_images_group(url,eval_cqp_data)
			# 消息 == 关闭搜图
			elif msg == search_image_quit:
				# 判断是否在搜图名单中,以及恶意关闭
				# 关闭搜图,在名单中,删除
				if user_id in search_image_group_list:
					for i in search_image_group_list[::-1]:
						if i == user_id:
							search_image_group_list.remove(i)
							self.reply_group["message"] = reply_image_quit
							return self.reply_group
				# 关闭搜图,不在名单中,提示
				else:
					self.reply_group["message"] = reply_enable_search
					return self.reply_group
			# 消息 == 其他
			else:
				# 搜图模式发送文字,自动关闭
				print(msg)
				if user_id in search_image_group_list:
					if msg.split(',')[0] != "[CQ:image":
						for i in search_image_group_list[::-1]:
							if i == user_id:
								search_image_group_list.remove(i)
								self.reply_group["message"] = reply_bot_quit
								return self.reply_group



		# 私聊
		elif message_type == "private":
			if user_id not in search_image_list:
				search_image_list.append(user_id)
				self.reply["message"] = reply_image
				return self.reply






	def search_anime(self):
		pass

	def jiki(self):
		pass

	def random_pixiv_image(self):
		pass

	def search_pid(self):
		pass

	def count_image(self):
		pass
