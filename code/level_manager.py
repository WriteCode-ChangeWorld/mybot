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

pass


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
		过滤消息 - 黑名单功能
		:paramas eval_cqp_data: cq数据包
		:return :TBD
		"""
		# 查询数据库中是否有该用户
		# if DBClient.isExists_records
		kwargs = {
			"uid": eval_cqp_data.get("user_id",0),
			"gid": eval_cqp_data.get("group_id",0),
		}
		for k in list(kwargs.keys()):
			if not kwargs[k]:
				del kwargs[k]

		with UserData(kwargs) as user_info:
			pass

	def change_level(self, level, **kwargs):
		"""
		change user/group level
		:paramas level: new level
		:paramas kwargs: new level
		:return : 新包
		"""
		pass