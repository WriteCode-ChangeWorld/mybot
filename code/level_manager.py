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
from Arsenal.basic.datetime_tool import datetime_now,datetime_offset
from Arsenal.basic.user_data import UserData
from Arsenal.basic.msg_temp import USER_MSG_TEMP,USER_LIMIT_TEMP


class Monitor:
	"""用户/群组 的权限 查看/更新"""
	def __init__(self):
		self.judge_data = {}
		self.wait_seconds = 1

	def filter_msg(self, eval_cqp_data):
		""" 
		是否过滤消息
		:paramas eval_cqp_data: cq数据包
		:return : 是 - True / 否 - False
		"""
		msg = eval_cqp_data.get("message", "")
		uid = eval_cqp_data.get("user_id",0)
		gid = eval_cqp_data.get("group_id",0)
		message_type = eval_cqp_data.get("message_type", "")

		self.judge_data = {"uid": uid, "gid": gid, "message_type": message_type}
		for k in list(self.judge_data.keys()):
			if not self.judge_data[k]:
				del self.judge_data[k]
		if not self.judge_data:
			return True

		with UserData(**self.judge_data) as mybot_data:
			tool.mybot_data = mybot_data
			# 屏蔽 / 黑名单
			if mybot_data["user_info"]["is_qqBlocked"] == 0:
				if eval_cqp_data["message_type"] == "group":
					logger.info(USER_MSG_TEMP["qqBlocker_group_msg"].format(gid,uid,msg))
				elif eval_cqp_data["message_type"] == "private":
					logger.info(USER_MSG_TEMP["qqBlocker_user_msg"].format(uid,msg))
				return True

			# 普通用户调用频率限制
			if tool.user_limit_flag:
				_ = self.user_limit(mybot_data)
				if not _:
					return False
				elif _:
					# 向用户发送提示
					self._limit_prompt_info(mybot_data)
					return True

			# 防止无返回值 默认不过滤False
			if eval_cqp_data["message_type"] == "group":
				logger.info(USER_MSG_TEMP["general_group_msg"].format(gid,uid,msg))
			elif eval_cqp_data["message_type"] == "private":
				logger.info(USER_MSG_TEMP["general_user_msg"].format(uid,msg))
			else:
				logger.info(USER_MSG_TEMP["general_unknown_msg"].format(gid,uid,msg))
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

		# 更新cycle_expiration_time
		if now_time > mybot_data["user_info"]["cycle_expiration_time"]:
			offset_seconds = datetime_offset(now_time, tool.config["Level"]["user_limit"]["seconds"])
			mybot_data["user_info"]["user_call_count"] = 0
			mybot_data["user_info"]["cycle_expiration_time"] = now_time + offset_seconds
			tool.db.update_records(mybot_data["user_info"], self.judge_data)
			return False

	def _limit_prompt_info(self, mybot_data):
		"""发送提示,请稍后再试"""
		mybot_data["message"] = USER_LIMIT_TEMP[random.choice(list(USER_LIMIT_TEMP))].format(self.wait_seconds)
		status = tool.auto_send_msg(mybot_data)
		if not status:
			logger.warning(f"发送<用户调用限制>提示信息失败")