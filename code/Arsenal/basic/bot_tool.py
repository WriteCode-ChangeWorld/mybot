# -*- encoding: utf-8 -*-
'''
@File    :   bot_tool.py
@Time    :   2021/05/20 11:13:31
@Author  :   Coder-Sakura
@Version :   1.2
@Contact :   1508015265@qq.com
@Desc    :   bot配置 CQ码转换等可复用方法
'''
# here put the import lib·
import os

from Arsenal.basic.db_pool import DBClient
from Arsenal.basic.log_record import logger
from Arsenal.basic.file_handler import loadFile
from Arsenal.basic.BNConnect import baseRequest
from Arsenal.basic.msg_temp import CONFIG_CQ_CODE,TOOL_TEMP

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
			"..","..","config.yaml")
default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
			"..","..","temp","resource","default.yaml")


def init_config():
	"""初始化mybot配置文件"""
	if not os.path.exists(config_path):
		with open(config_path,"w") as f1:
			with open(default_path) as f2:
				f1.write(f2.read())
	config_yaml = loadFile.by_yaml(config_path)
	return config_yaml


class Config:
	"""
	全局变量配置
	"""
	def __init__(self):
		# 初始化
		self.config = init_config()
		self.user_limit_flag = self.config["Level"]["user_limit"]["enable"]
		self.level = self.read_level_info()
		# 统一使用bot_tool的db
		self.db = DBClient

		# ===== 初始化log ===== 
		logger.info(TOOL_TEMP["load_config_success"])
		logger.warning(TOOL_TEMP["debug_status"].format(self.config['Debug']))
		logger.debug(TOOL_TEMP["config_info"].format(self.config))
		logger.debug(TOOL_TEMP["config_path_info"].format(config_path))

		# 通信
		# HTTP or WebSocket
		self.protocol = "http://" # or ws://
		self.coolq_http_api_ip = self.get_items('["Bot"]["http"]["coolq_http_api_ip"]')
		self.coolq_http_api_port = self.get_items('["Bot"]["http"]["coolq_http_api_port"]')
		self.comm_address = f"{self.protocol}{self.coolq_http_api_ip}:{self.coolq_http_api_port}"

		self.send_group_url = TOOL_TEMP["cq_http_send_group_url"].format(self.comm_address)
		self.send_private_url = TOOL_TEMP["cq_http_send_private_url"].format(self.comm_address)

		# admin uid
		self.admin = int(self.get_items('["Bot"]["admin"]["uid"]'))

		# ===== PLUGIN =====
		# saucenao
		self.saucenao_api_key = self.get_items('["Plugin"]["saucenao"]["api_key"]')

		# 标志位 - 实验性
		# PLUGIN_BLOCK
		# 主动式插件消息命中解析规则返回
		# self.PLUGIN_BLOCK = 0
		# PLUGIN_IGNORE
		# 主动式插件消息未命中解析规则
		# 被动式插件跳过自身
		# self.PLUGIN_IGNORE = 1
		# ===== PLUGIN =====

	def get_items(self,value_path="",obj="self.config"):
		"""
		获取配置文件中value
		:params obj: 指定获取数据的对象
		:params value_path: 字段路径
		:return: value/None

		exp: 
			get_items(value_path='["Bot"]["mysql"]["db_user"]') - 'pixiv'
			get_items(value_path='["Other"]["mysql"]["db_user"]') - None
		"""
		try:
			return eval("{}{}".format(obj,value_path))
		except:     
			return None

	def reload_bot_config(self):
		"""重新加载配置文件"""
		return init_config()

	def read_level_info(self):
		"""加载配置文件中的权限设置"""
		return {
			"general_user_level": int(self.config["Level"]["user"]["general"]),
			"vip_user_level": int(self.config["Level"]["user"]["vip"]),
			"admin_user_level": int(self.config["Level"]["user"]["admin"]),
			"general_group_level": int(self.config["Level"]["group"]["general"]),
			"vip_group_level": int(self.config["Level"]["group"]["vip"])
		}

	# === API start===
	# TODO 测试后删除 2022/1/17
	def send_group_msg(self,params,url=None):
		"""
		私聊先留空
		发送群聊信息到go-cqhttp接口
		"""
		if not url:
			url = self.send_group_url
		return baseRequest({"url":url},params=params)

	# TODO 测试后删除 2022/1/17
	def send_private_msg(self,params,url=None):
		"""
		发送私聊信息到go-cqhttp接口
		"""
		if not url:
			url = self.send_private_url
		return baseRequest({"url":url},params=params)

	def auto_report_err(self,err_msg,channel="cq"):
		"""
		向管理员实时汇报err信息
		"""
		status = {}
		# 选择qq通知需在config.yaml中填写
		# 路径为 ["Bot"]["admin"]["uid"]
		if channel == "cq":
			params = self.private_msg_temp(
				self.admin,
				err_msg
			)
			status = self.send_private_msg(params=params)
			logger.info(f"<status> - {status}")
			return status
	
	def auto_send_msg(self, mybot_data)->bool:
		"""
		根据mybot_data进行群组/私聊信息发送
		"""
		# 群聊信息
		if mybot_data["sender"]["type"] == "group":
			params = self.group_msg_temp(mybot_data)
			self.send_cq_client(params, api="cq_http_send_group_url")
		# 私聊信息
		elif mybot_data["sender"]["type"] == "private":
			params = self.private_msg_temp(mybot_data)
			self.send_cq_client(params, api="cq_http_send_private_url")
		else:
			return False

		return True

	def send_cq_client(self,params,api=None,url=None):
		"""
		获取go-cq接口数据
		"""
		# 直接指定url
		if url:
			api_url = url

		# 通过接口名
		if api:
			api_url = TOOL_TEMP[api].format(self.comm_address)

		return baseRequest({"url": api_url}, params=params)

	def group_msg_temp(self, mybot_data)->dict:
		"""
		群聊消息
		"""
		if mybot_data["at"]:
			mybot_data["message"] = self.CQ_AT(int(mybot_data["sender"]["user_id"])) + \
				"\n" + mybot_data["message"]
		group_msg = {
			"group_id": int(mybot_data["sender"]["group_id"]),
			"message": mybot_data["message"]
		}
		logger.debug(f"<group_msg> - {group_msg}")
		return group_msg

	def private_msg_temp(self, mybot_data)->dict:
		"""
		私聊消息
		"""
		if mybot_data["at"]:
			mybot_data["message"] = self.CQ_AT(int(mybot_data["sender"]["user_id"])) + \
				"\n" + mybot_data["message"]
		user_msg = {
			"user_id": int(mybot_data["sender"]["user_id"]),
			"message": mybot_data["message"]
		}
		logger.debug(f"<user_msg> - {user_msg}")
		return user_msg

	# # === API end===
	# === CQ code start ===

	def CQ_IMG_URL(self,img_url):
		"""
		CQ码: 网络图片链接
		:parmas img_url: 图片链接
		"""
		return CONFIG_CQ_CODE["reply_img"].format(img_url)

	def CQ_IMG_LOCAL(self,img_path):
		"""
		CQ码: 本地图片
		:parmas img_path: 本地图片路径
		"""
		return CONFIG_CQ_CODE["reply_local_img"].format(img_path)

	def CQ_AT(self,user_id):
		"""
		CQ码: @
		:parmas user_id: 用户id
		"""
		return CONFIG_CQ_CODE["reply_at"].format(user_id)

	def CQ_AUDIO_URL(self,audio_url):
		"""
		CQ码: 网络语音
		:parmas audio_url: 网络语音url
		"""
		return CONFIG_CQ_CODE["reply_audio"].format(audio_url)

	def CQ_AUDIO_LOAL(self,audio_path):
		"""
		CQ码: 本地语音
		:parmas audio_path: 本地语音路径
		"""
		return CONFIG_CQ_CODE["reply_local_audio"].format(audio_path)
	
	# === CQ code end ===


tool = Config()