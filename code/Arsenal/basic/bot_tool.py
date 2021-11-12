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


from fileHandler import loadFile
from log_record import logger
from BNConnect import baseRequest
from msg_temp import CONFIG_CQ_CODE,TOOL_TEMP


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
			"..","..","config.yaml")
default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
			"..","..","temp","default.yaml")


def init_config():
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
		self.config = init_config()

		logger.info(TOOL_TEMP["load_config_success"])
		logger.warning(TOOL_TEMP["debug_status"].format(self.config['Debug']))
		logger.debug(TOOL_TEMP["config_info"].format(self.config))
		logger.debug(TOOL_TEMP["config_path_info"].format(config_path))
		# saucenao_api_key
		self.saucenao_api_key = self.get_items('["Plugin"]["saucenao"]["api_key"]')
		# PLUGIN_BLOCK
		self.PLUGIN_BLOCK = 0
		# PLUGIN_IGNORE
		self.PLUGIN_IGNORE = 1

	# get value from obj by value_path
	def get_items(self,value_path="",obj="self.config"):
		"""
		获取配置文件中value
		:params obj: 指定获取数据的对象
		:params value_path: 字段路径
		:return: value/None

		示例: 
			get_items(value_path='["Bot"]["mysql"]["db_user"]')
				'pixiv'
			get_items(value_path='["Other"]["mysql"]["db_user"]')
				None
		"""
		try:
			return eval("{}{}".format(obj,value_path))
		except:     
			return None

	def send_group_msg(self,parmas,url=None):
		"""
		私聊先留空
		发送群聊信息到go-cqhttp接口
		"""
		if not url:
			url = self.send_group_url
		return baseRequest({"url":url},parmas=parmas)
		# return requests.get(url,parmas=parmas)

	def send_private_msg(self,parmas,url=None):
		"""
		发送私聊信息到go-cqhttp接口
		"""
		if not url:
			url = self.send_private_url
		return baseRequest({"url":url},parmas=parmas)
		# return requests.get(url,parmas=parmas)

	def group_msg_temp(self,group_id,msg):
		"""
		群聊消息
		:parmas group_id: 群组id
		:parmas msg: 群组消息
		return CQ数据包
		"""
		group_msg = {
			"group_id":group_id,
			"message":msg,
		}
		return group_msg

	def private_msg_temp(self,user_id,msg):
		"""
		私聊消息
		:parmas user_id: 用户id
		:parmas msg: 私聊消息
		return CQ数据包
		"""
		user_msg = {
			"user_id":user_id,
			"message":msg,
		}
		return user_msg

	def network_img(self,img_url):
		"""
		CQ码: 网络图片链接
		:parmas img_url: 图片链接
		"""
		return CONFIG_CQ_CODE["reply_img"].format(img_url)

	def local_img(self,img_path):
		"""
		CQ码: 本地图片
		:parmas img_path: 本地图片路径
		"""
		return CONFIG_CQ_CODE["reply_local_img"].format(img_path)

	def at(self,user_id):
		"""
		CQ码: @
		:parmas user_id: 用户id
		"""
		return CONFIG_CQ_CODE["reply_at"].format(user_id)

	def audio(self,audio_url):
		"""
		CQ码: 网络语音
		:parmas audio_url: 网络语音url
		"""
		return CONFIG_CQ_CODE["reply_audio"].format(audio_url)

	def local_audio(self,audio_path):
		"""
		CQ码: 本地语音
		:parmas audio_path: 本地语音路径
		"""
		return CONFIG_CQ_CODE["reply_local_audio"].format(audio_path)



tool = Config()