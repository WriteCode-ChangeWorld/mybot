# -*- encoding: utf-8 -*-
'''
@File    :   church.py
@Time    :   2021/05/08 18:21:37
@Author  :   Coder-Sakura
@Version :   1.0
@Contact :   1508015265@qq.com
@Desc    :   Mybot消息-生命周期事件处理
'''

# here put the import lib
import os
import json
import time
import random
import requests
from threading import Thread
from flask import Flask, request, jsonify


from executor import Executor
# from Arsenal.basic.db_pool import DBClient
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.msg_temp import CHURCH_IDENTIFY_MSG

# CHURCH_IDENTIFY_MSG = [
# 	{"code": -100, "description":"识别到心跳包或其他未知原因"},
# 	{"code": -1, "description":"识别到用户处于黑名单列表,将忽略信息"},
# 	{"code": 0, "description":"距离下次调用还有{}秒,当前非法调用:{}次"},
# 	{"code": 1, "description":"识别到用户再次过快调用,请等待20秒再调用"},
# 	{"code": 10, "description":"识别到用户状态正常"},
# 	{"code": 200, "description":"识别通过,用户状态正常"},
# ]


class Church:
	"""Mybot消息-生命周期事件处理"""

	def __init__(self):
		self.eval_cqp_data = {}
		self.fusion_data = {}
		# level 0 等待时间
		self.waiting_time = 0
		# level 1 惩罚时间
		self.illegal_time = 20

	# 使用config
	# def bot_send_msg(self,bot_data):
	# 	requests.get(url=qunliao, params=bot_data)

	def analysis_fusion(self):
		"""
		分解酷Q数据包,创建/读取用户配置,构造fusion_data
		"""
		fusion_data = {}
		# Group_id,为空置None,后续优先判断
		fusion_data["group_id"] = self.eval_cqp_data.get("group_id",None)
		# user_id,为空置None
		fusion_data["user_id"] = self.eval_cqp_data.get("user_id",None)
		# 消息类型:group/private
		fusion_data["message_type"] = self.eval_cqp_data.get("message_type",None)
		# 消息:普通文本/带CQ码
		fusion_data["message"] = self.eval_cqp_data.get("message",None)
		# 数据包时间戳:数据包自带/time.time()生成
		fusion_data["tt"] = self.eval_cqp_data.get("time",int(time.time()))

		# 心跳包、群组撤回消息、私聊撤回消息、其他
		if fusion_data["user_id"] == None or \
			fusion_data["user_id"] == None or \
			fusion_data["user_id"] == "":
			return {}

		# user_id,level,limit,timestamp,in_blacklist,remind_enable
		if not self.configer.exists_section(fusion_data["user_id"]):
			user_config = self.configer.create_section(fusion_data["user_id"])
		else:
			user_config = self.configer.get_section_items(fusion_data["user_id"])
		fusion_data.update(user_config)

		return fusion_data
 
	def identify_data(self,fusion_data):
		"""
		根据数据包改变权限
		:params fusion_data:用户数据包
		:return: {"code":200,"msg":""}
		"""
		self.fusion_data = fusion_data
		# 数据包中获取不到qq,可能是心跳包
		if self.fusion_data == {}:
			return -100

		user_id = fusion_data["user_id"]
		level = fusion_data["level"]
		limit = int(fusion_data["limit"])
		# 两者相同代表第一次发送消息被机器人记录
		# 本次消息的时间戳
		tt = int(fusion_data["tt"])
		# 上次消息的时间戳
		timestamp = int(fusion_data["timestamp"])
		# 获取到的是str
		in_blacklist = fusion_data["in_blacklist"]
		remind_enable = fusion_data["remind_enable"]
		illegal_count = int(fusion_data["illegal_count"])
		print("FusionData",fusion_data)

		# 黑名单成员忽略
		if in_blacklist == str(True):
			return -1

		# 暂时使用in_blacklist判定
		# level -1
		# if level == -1:
			# 暂不处理
			# return -1

		# level 0 中间等级
		# 有限制的level(10) --> level 0
		if level == "0":
			# 正常调用.恢复权限
			if timestamp + limit < tt:
				# self.configer.update_section(user_id, (10,10,tt))
				self.configer.update_section(user_id, {"level":"10","limit":"10","timestamp":tt,"illegal_count":"0","remind_enable":"False"})
				return 10
			# 非法调用,未经过limit秒内再调用
			# level 0再次过早调用,转level 1
			# 更新用户最后一次消息时间戳
			if timestamp + limit > tt:
				# self.configer.update_section(user_id, (1,limit,tt))
				# 修改remind_enable为True,并提示一次,level调整为1
				self.configer.update_section(user_id, {"level":"1","limit":limit,"timestamp":tt})
				return 1

		# level 1 中间等级
		if level == "1":
			# 正常调用,limit秒后再调用,恢复用户数据为初始数据
			if timestamp + limit < tt:
				# self.configer.update_section(user_id, (10,10,tt))
				self.configer.update_section(user_id, {"level":"10","limit":"10","timestamp":tt,"illegal_count":"0"})
				return 10

			# 再次非法调用,保持level 1 limit 20;
			if timestamp + limit > tt:
				# 如何告诉用户level 10等待10秒,累计3次转level 0/1,等待20秒
				self.configer.update_section(user_id, {"level":"1","limit":str(self.illegal_time),"timestamp":tt})
				return 1

		# 普通用户列表,需要在全局变量(模块)中定义
		# if level in user_level_list:
		# level 10 
		if level == "10":
			# 正常调用,更新时间戳,暂不做其他处理
			# 可以做关键词检测,检测是否有违规词?
			if timestamp + limit < tt:
				self.configer.update_section(user_id, {"timestamp":tt})
				# self.waiting_time = 0 
				return 10  
			# 非法调用,未经过limit秒内再调用
			elif timestamp + limit > tt:
				# 非法调用计数达到3次
				if illegal_count == 3:
					# 在调整为level 0前提示一次
					self.configer.update_section(user_id, {"level":"0","limit":limit,"timestamp":tt,"remind_enable":"True"})
					return 0
				else:	
					# 如何告诉用户level 10等待10秒,累计3次转level 0/1,等待20秒
					# 距离下次调用还有{}秒,当前非法调用:{}次
					self.configer.update_section(user_id, {"timestamp":tt,"illegal_count":illegal_count + 1})
					self.waiting_time = timestamp + limit - tt
					return 10

		# 普通用户列表,需要在全局变量(模块)中定义
		# if level in vip_level_list:
		# level 50
		if level == "50":
			return 50

		# level 999
		if level == "999":
			# executor管理员命令解析模块

			return 999

	def Church2Executor(self):
		"""
		搭桥,Church与Executor
		"""
		from executor import Executor
		executor = Executor()
		a = executor.task_parse(self.eval_cqp_data)

		if a["message"] != "":
			requests.get(url=qunliao, params=a)
			print("cqp 发送信息为:",a,"\n")
			return "1"

	def hand(self,eval_cqp_data):
		"""
		入口,流程函数
		"""
		self.eval_cqp_data = eval_cqp_data
		# analysis_fusion构造数据包
		# 造数据并由identify_data判断出结果
		status = self.identify_data(self.analysis_fusion())
		print("status",status)

		# 心跳包,黑名单,未知原因跳过
		if status in [-100,-1]:
			print(get_time(),[i["description"] for i in CHURCH_IDENTIFY_MSG if i["code"] == status][0])
			# 黑名单用户信息打印
			if status == -1:
				print(get_time(),
					"user_id:{} group_id:{} level:{}".format(
						self.fusion_data.get("user_id","Null"),
						self.fusion_data.get("group_id","Null"),
						self.fusion_data.get("level","Null")
					))

		# 暂时先判断status为0
		if status == 0:
			# "当前非法调用达到3次,请等待{limit}秒后再使用..."
			pass



# =================监听接口开始================
app = Flask(__name__)
pope = Church()
executor = Executor()

# 需要加入全局变量
# search_image_group_list = bot_config.search_image_group_list
# search_image_group_list = []
# search_img_timeout_limit = 60
# def get_time():
# 	return '[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/',methods=['POST'])
def bot_function():
	# 获取机器人推送的内容
	cqp_push_data = request.get_data()
	# 转换推送内容为字典格式
	eval_cqp_data = json.loads(cqp_push_data.decode('utf-8'))
	pope.hand(eval_cqp_data)
	return " "
	# church统一回复酷Q
	# executor只需要执行功能,包装并返回消息
	# monitor对消息进行过滤,包括是否放行到executor以及添加黑名单,接触限制等

# =================监听接口结束================

# ===== 删除 =====
# 计时器--搜图
# 每60秒检查一次,定时清除处于搜图模式的空闲用户
# 用户被清除需要提示,机器人往群聊发消息
# def cycle():
# 	while True:
# 		if search_image_group_list != []:
# 			for u in search_image_group_list[::-1]:
# 				if u["timestamp"] + search_img_timeout_limit < int(time.time()):
# 				# if u["timestamp"] + 10 < int(time.time()):
# 					print("{} Search Image List Remove: {}".format(get_time(),u))
# 					search_image_group_list.remove(u)
# 					# return search_img_timeout_msg
# 		print("{} Search Image List Now: {}".format(get_time(),search_image_group_list))
# 		time.sleep(30)
# ===== 删除 =====

def flask_app():
	app.config['JSON_AS_ASCII'] = False
	app.run( port='5000')


if __name__ == '__main__':
	flask_app()


	# ===== 删除 =====
    # app.config['JSON_AS_ASCII'] = False
    # app.run( port='5000')
    # 任务队列,启动多线程
	# task_list = ["cycle","flask_app"]
	# thread_list = []
	# for t in task_list:
	# 	t = Thread(target=eval(t))
	# 	t.setDaemon(True)
	# 	thread_list.append(t)

	# for t in thread_list:
	# 	t.start()
	# ===== 删除 =====

	# setDaemon设置为True,主线程执行完毕后会将子线程回收掉
	# True表示该线程是不重要的,进程退出时不需要等待这个线程执行完成。
	# False表示主进程执行结束时不会回收子线程
	# 不采用join方法,采用isAlive来判断子线程是否完成
	# while 1:
	# 	alive = False
	# 	for i in thread_list:
	# 		alive = alive or i.isAlive()
	# 	if not alive:
	# 		break