# -*- encoding: utf-8 -*-
'''
@File    :   level_manager.py
@Time    :   2021/11/30 15:18:46
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   权限管理
'''

# here put the import lib
import random

from Arsenal.basic.log_record import logger
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.datetime_tool import datetime_now, datetime_offset, str2datetime
from Arsenal.basic.msg_temp import USER_MSG_TEMP,USER_LIMIT_TEMP,DB_TEMP


class Monitor:
	"""用户/群组 的权限 查看/更新"""
	def __init__(self):
		self.judge_data = {}
		self.db_update_judge_data = {}
		self.wait_seconds = 1

	def filter_msg(self, mybot_data):
		""" 
		是否过滤消息
		:paramas mybot_data: mybot内部消息结构
		:return : 是 - True / 否 - False
		"""
		if not mybot_data:
			return True

		uid = mybot_data["sender"]["user_id"]
		gid = mybot_data["sender"]["group_id"]
		message = mybot_data["arrange"]["message"]
		self.db_update_judge_data = {"uid": uid, "gid": gid}

		# with UserData(**self.judge_data) as mybot_data:
			# tool.mybot_data = mybot_data

		# 屏蔽 / 黑名单
		if mybot_data["user_info"]["is_qqBlocked"] == DB_TEMP["is_qqBlocked"]:
			if mybot_data["sender"]["type"] == "group":
				logger.info(USER_MSG_TEMP["qqBlocker_group_msg"].format(gid,uid,message))
			elif mybot_data["sender"]["type"] == "private":
				logger.info(USER_MSG_TEMP["qqBlocker_user_msg"].format(uid,message))
			return True

		# 普通用户调用频率限制
		if tool.user_limit_flag:
			_ = self.user_limit(mybot_data)
			if not _:
				if mybot_data["sender"]["type"] == "group":
					logger.info(USER_MSG_TEMP["general_group_msg"].format(gid,uid,message))
				elif mybot_data["sender"]["type"] == "private":
					logger.info(USER_MSG_TEMP["general_user_msg"].format(uid,message))
				else:
					logger.info(USER_MSG_TEMP["general_unknown_msg"].format(gid,uid,message))
				return False
			elif _:
				# 向用户发送提示
				self._limit_prompt_info(mybot_data)
				return True

		# 防止无返回值 默认不过滤False
		if mybot_data["sender"]["type"] == "group":
			logger.info(USER_MSG_TEMP["general_group_msg"].format(gid,uid,message))
		elif mybot_data["sender"]["type"] == "private":
			logger.info(USER_MSG_TEMP["general_user_msg"].format(uid,message))
		else:
			logger.info(USER_MSG_TEMP["general_unknown_msg"].format(gid,uid,message))
		return False

	def user_limit(self, mybot_data):
		"""
		普通用户调用频率限制,判断是否对其限制
		:params mybot_data: mybot消息体
		:return: 是 - True or 否 - False
		"""
		now_time = datetime_now()
		logger.debug(f"<mybot_data> - {mybot_data}")

		# 高级用户
		if int(mybot_data["user_info"]["user_level"]) > int(tool.level["general_user_level"]):
			return False

		# 调用超出限制
		if int(mybot_data["user_info"]["user_call_count"]) >= int(mybot_data["user_info"]["user_limit_count"]):
			self.wait_seconds = (mybot_data["user_info"]["cycle_expiration_time"] - now_time).seconds
			return True


		# 第一次插入数据时,cycle_expiration_time为str类型
		# 后续为datetime.datetime,需要进行转换
		cycle_expiration_time = mybot_data["user_info"]["cycle_expiration_time"]
		if type(cycle_expiration_time) != type(now_time):
			cycle_expiration_time = str2datetime(cycle_expiration_time)

		# 更新cycle_expiration_time
		if now_time > cycle_expiration_time:
			future_time = datetime_offset(now_time, tool.config["Level"]["user_limit"]["seconds"])
			mybot_data["user_info"]["user_call_count"] = 0
			mybot_data["user_info"]["cycle_expiration_time"] = future_time
			tool.db.update_records(**{
				"update_data": mybot_data["user_info"], 
				"judge_data": self.db_update_judge_data
			})
			return False

	def _limit_prompt_info(self, mybot_data):
		"""发送提示,请稍后再试"""
		mybot_data["message"] = USER_LIMIT_TEMP[random.choice(list(USER_LIMIT_TEMP))].format(self.wait_seconds)
		status = tool.auto_send_msg(mybot_data)
		if not status:
			logger.warning(f"发送<用户调用限制>提示信息失败")