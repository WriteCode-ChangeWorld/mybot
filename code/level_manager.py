# -*- encoding: utf-8 -*-
'''
@File    :   level_manager.py
@Time    :   2021/11/30 15:18:46
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   权限管理
'''

# here put the import lib
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.msg_temp import USER_MSG_TEMP


class UserData:
	def __init__(self,**kwargs):
		self.kwargs = kwargs
		self.mybot_data = {
			"arrange": {},
			"user_info": {},
			"sender": {
				"user_id": self.kwargs.get("uid", 0),
				"group_id": self.kwargs.get("gid", 0),
				"type": "",
			},
			"at": False,
			"message": "",
			"plugin": {},
		}
 
	def __enter__(self):
		# 非新用户
		select_result:dict = tool.db.select_records(**self.kwargs)
		# 新用户
		if not select_result:
			# 判断是否在里群(level>=50)
			group_result = tool.db.select_records(table="group_chats", **{"gid":self.kwargs["gid"]})
			if group_result:
				group_level = int(group_result.get("group_level", tool.level["general_group_level"]))
			else:
				group_level = tool.level["general_group_level"]
			# group_level = int(tool.db.select_records(table="group_chats", **{"gid":self.kwargs["gid"]})["group_level"])

			if group_level >= tool.level["vip_group_level"]:
				result:dict = tool.db.insert_records(self.mybot_data, **{"lev  el": tool.level["vip_user_level"]})
			else:
				result:dict = tool.db.insert_records(self.mybot_data)
		else:
			result:dict = select_result[0]

		self.mybot_data["user_info"] = result
		return self.mybot_data

	def __exit__(self):
		pass


class Monitor:
	"""用户/群组 的权限 查看/更新"""
	def __init__(self):
		pass

	# TODO(Coder-Sakura): 2020/07/12 16:09 限制数据采集
	def filter_msg(self, eval_cqp_data):
		""" 
		是否过滤消息
		:paramas eval_cqp_data: cq数据包
		:return : 是 - True / 否 - False
		"""
		msg = eval_cqp_data.get("message", "")
		uid = eval_cqp_data.get("user_id",0)
		gid = eval_cqp_data.get("group_id",0)

		kwargs = {"uid": uid,"gid": gid}
		for k in list(kwargs.keys()):
			if not kwargs[k]:
				del kwargs[k]
		if not kwargs:
			return True

		with UserData(**kwargs) as mybot_data:
			# 屏蔽 / 黑名单
			if mybot_data["user_info"]["is_qqBlocked"] == 0:
				if eval_cqp_data["message_type"] == "group":
					logger.info(USER_MSG_TEMP["qqBlocker_group_msg"].format(gid,uid,msg))
				elif eval_cqp_data["message_type"] == "private":
					logger.info(USER_MSG_TEMP["qqBlocker_user_msg"].format(uid,msg))
				return True
			# level = 1 × 没有level 1
			# elif int(user_info["user_level"]) == 1:
			# 	if eval_cqp_data["message_type"] == "group":
			# 		logger.info(USER_MSG_TEMP["limit_group_msg"].format(gid,uid,msg))
			# 	elif eval_cqp_data["message_type"] == "private":
			# 		logger.info(USER_MSG_TEMP["limit_user_msg"].format(uid,msg))
			# 	return True
			# limit:user_call_count

			# 普通用户调用频率限制
			if tool.user_limit_flag:
				if not self.user_limit(mybot_data):
					return False
				else:
					# 向用户发送提示,请稍后再试
					self._limit_prompt_info()
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
		普通用户调用频率限制,判断是否限制
		:params mybot_data: mybot消息体
		:return: 是 - True or 否 - False
		"""
		# 更新cycle_expiration_time
		pass

	def _limit_prompt_info(self):
		"""发送提示,请稍后再试"""
		pass

	def change_level(self, level, **kwargs):
		"""
		change user/group level
		"""
		pass