import sys
import time
# sys.path.append("Arsenal")

from dynamic_import import Dynamic_Load
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.db_pool import DBClient
from Arsenal.basic.log_record import logger
from Arsenal.basic.msg_temp import MYBOT_ERR_CODE, EXECUTOR_TASK_STATUS_INFO, TASK_PROCESSOR_TEMP
from Arsenal.basic.thread_pool import ThreadPool, callback
from Arsenal.basic.task_processor import taskprocessor

class Executor:
	"""执行者: 动态导入插件及执行"""
	def __init__(self):
		# 为tool创建线程池pool
		self.init_thread_pool(8)

		# 启动定时任务检测线程
		# tool.pool.put(self.cycle_task_detect, (), callback)

		# 动态导入调试中
		# self.dynamic_load = Dynamic_Load()

		# 回复群聊的数据包
		self.reply_group = {}
		# 回复私聊的数据包
		self.reply = {}
		
		# trace.moe的api地址
		# self.trace_moe_url = 'https://trace.moe/api/search?url='
		# saucenao的API地址
		# self.search_image_url = "https://saucenao.com/search.php?db=999&output_type=2&\
		# 			testmode=1&numres=16&api_key={}&&url={}"

	# thread_pool func start
	def init_thread_pool(self,max_num=8):
		"""
		初始化线程池,暂不考虑reload情况
		< -- not reliable! -- >
		"""
		try:
			if hasattr(tool,"pool"):
				tool.pool.terminal = True
				logger.debug("3秒后重启线程池...")
				time.sleep(3)
		except Exception as e:
			logger.debug(MYBOT_ERR_CODE.format(e))
			return False
		finally:
			# 重置中断标志
			tool.pool = ThreadPool(max_num=max_num)
			tool.pool.terminal = False
			return True

	@logger.catch
	def cycle_task_detect(self,cycle=10):
		"""
		定时(<cycle>秒)监测任务并将任务放入线程池执行
		:params cycle: 监测周期,默认10秒检查一次
		"""
		# 通过terminal来强制中断
		while True:
			logger.info(TASK_PROCESSOR_TEMP["TASK_START"])
			if tool.pool.terminal:
				logger.info(TASK_PROCESSOR_TEMP["TASK_BREAK_TERMINAL"])
				break

			tasks_list = taskprocessor.get_tasks()
			if not tasks_list:
				logger.info(TASK_PROCESSOR_TEMP["TASK_NO_RECORD"])
			else:
				tasks_count_info = taskprocessor.task_count(tasks_list)
				[logger.info(EXECUTOR_TASK_STATUS_INFO["info"].format(i,j)) for i,j in tasks_count_info.items()]
				
				for task in tasks_list:
					tool.pool.put(taskprocessor.exec_tasks, (task,), callback)

			logger.info(TASK_PROCESSOR_TEMP["TASK_END"].format(cycle))
			time.sleep(cycle)

	

	# def create_tasks(self,insert_data):
	# 	"""
	# 	根据insert_data创建task记录
	# 	:params insert_data: 任务信息, key顺序必须与数据库字段一样
	# 	:return: True or False
	# 	"""
	# 	result = DBClient.insert_records(cqp_data=None, table="tasks", **{"insert_data": insert_data})
	# 	# result = DBClient.insert_records(cqp_data=None, table="tasks", **{insert_data})
	# 	return result

	# def get_tasks(self,nums=0):
	# 	"""
	# 	从tass表中根据优先级获取nums个waiting状态的任务
	# 	:params nums: 获取的任务数量
	# 		range:1~10 0 -> all
	# 	:return: tasks_dict
	# 	"""
	# 	if nums == 0:
	# 		limit = -1
	# 	elif 1 <= nums <= 10:
	# 		limit = nums
	# 	else:
	# 		limit = 10
	# 	result = DBClient.select_records(table="tasks",limit=limit,**{"task_status":"waiting"})
	# 	return sorted(result, key=lambda x: x["task_level"], reverse=True)

	# def exec_tasks(self,tasks_list):
	# 	pass

	# thread_pool func end

	def load_function_list(self):
		"""
		加载Arsenal目录下所有前缀为bot的功能模块
		"""
		# 需要添加sys.path
		# arsenal_files = os.listdir(os.path.join(os.getcwd(),"Arsenal"))
		# bot_arsenal_files = [i for i in arsenal_files if i[:3] == "bot"]
		"""
		for i in bot_arsenal_files:
			
			zz = __import__("{}.{}".format("Arsenal",i.split(".")[0]),fromlist = ("SauceNao",))
		"""
		# module_paths = import_modules('Arsenal/bot**.py')
		module_paths = self.dynamic_load.import_modules(self.dynamic_load.pathname)

	def task_parse(self, eval_cqp_data, extra=None):
		"""
		用于校验是否符合功能模块的触发条件
		:paramas eval_cqp_data: cq数据包
		:return : 功能模块封装好发给机器人的消息包
			{"group_id":123456789,"message":"Something","User":[...]}
			User字段为调用者的自定义数据包,尚未处理
		"""

		# 基本参数
		# 数据包发送者
		user_id = eval_cqp_data["user_id"]
		# 数据包消息
		msg = eval_cqp_data["message"]
		# 功能模块返回的结果/信息
		message = ""

		# ========================功能模块=========================
		# 整合三个判断条件,开启搜图,结束搜图,搜图名单中
		# print("user_id:{},当前群组搜图列表:{}".format(user_id,search_image_group_list))
		if msg == search_image_enable or \
			msg == search_image_quit  or \
			user_id in search_image_group_list:  
			print("匹配到<搜图>功能")
			try:
				message =  SauceNao().parse(eval_cqp_data)
			except Exception as e:
				message = "未知错误:{}".format(e)

		# 结束搜图
		# if msg == search_image_quit:
		# 	return self.search_image(eval_cqp_data)
		# 搜图名单中
		# if user_id in search_image_group_list:
			# return self.search_image(eval_cqp_data)
		# ========================功能模块结束=====================



		# 模板消息
		if eval_cqp_data["message_type"] == "group":
			self.reply_group = {
				"group_id": eval_cqp_data['group_id'],
				"message":message
			}
			return self.reply_group
		elif eval_cqp_data["message_type"] == "private":
			self.reply = {
				"user_id": eval_cqp_data['user_id'],
				"message":message
			}
			return self.reply

	# TODO(Coder-Sakura): 分离成单一模块, /Arsenal/image.py
	# 2020年9月22日22:14:28 已分离到/Arsenal/search_img.py
	def search_image(self, eval_cqp_data):
		"""
		用于校验是否符合功能模块的触发条件
		:paramas eval_cqp_data: cq数据包
		:return : 封装好的消息包
		"""
		user_id= eval_cqp_data["user_id"]
		msg = eval_cqp_data["message"]
		message_type = eval_cqp_data["message_type"]

		# 开启搜图
		# 群聊
		if message_type == "group":
			print(msg, search_image_group_list)
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
						msg_url = msg.split("url=")[-1].replace("]", "")
						url = self.search_image_url.format(api_key, msg_url)
						return tra_images_group(url, eval_cqp_data)
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

