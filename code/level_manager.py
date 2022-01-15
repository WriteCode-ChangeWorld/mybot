# -*- encoding: utf-8 -*-
'''
@File    :   level_manager.py
@Time    :   2021/11/30 15:18:46
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   权限管理
'''

# here put the import lib
from asyncio.log import logger
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.msg_temp import USER_MSG_TEMP


class UserData:
	def __init__(self,**kwargs):
		self.kwargs = kwargs
 
	def __enter__(self):
		if tool.db.isExists_records(): 
			return tool.db.select_records(self.kwargs)
		else:
			return tool.db.insert_records()

	def __exit__(self):
		pass


class Monitor:
	"""用户/群组 的权限 查看/更新"""
	def __init__(self):
		pass

	# def get_user_record(self, **kwargs):
	# 	return DBClient.select_records(**kwargs)

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
			return 

		with UserData(**kwargs) as user_info:
			# 屏蔽 / 黑名单
			if user_info["is_qqBlocked"] == 0:
				if eval_cqp_data["message_type"] == "group":
					logger.info(USER_MSG_TEMP["qqBlocker_group_msg"].format(gid,uid,msg))
				elif eval_cqp_data["message_type"] == "private":
					logger.info(USER_MSG_TEMP["qqBlocker_user_msg"].format(uid,msg))
				return True
			# level = 1
			elif int(user_info["user_level"]) == 1:
				if eval_cqp_data["message_type"] == "group":
					logger.info(USER_MSG_TEMP["limit_group_msg"].format(gid,uid,msg))
				elif eval_cqp_data["message_type"] == "private":
					logger.info(USER_MSG_TEMP["limit_user_msg"].format(uid,msg))
				return True
			else:
				if eval_cqp_data["message_type"] == "group":
					logger.info(USER_MSG_TEMP["general_group_msg"].format(gid,uid,msg))
				elif eval_cqp_data["message_type"] == "private":
					logger.info(USER_MSG_TEMP["general_user_msg"].format(uid,msg))
				else:
					logger.info(USER_MSG_TEMP["general_unknown_msg"].format(gid,uid,msg))
				return False


	def change_level(self, level, **kwargs):
		"""
		change user/group level
		:paramas level: new level
		:paramas kwargs: new level
		:return : 新包
		"""
		pass