# -*- encoding: utf-8 -*-
'''
@File    :   user_data.py
@Time    :   2022/01/19 11:04:33
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
from Arsenal.basic.bot_tool import tool

class UserData:
	def __init__(self,**kwargs):
		self.kwargs = kwargs
		self.mybot_data = {
			"arrange": {},
			"user_info": {},
			"sender": {
				"user_id": self.kwargs.get("uid", 0),
				"group_id": self.kwargs.get("gid", 0),
				"type": self.kwargs.get("message_type", 0),
			},
			"at": self.kwargs.get("at", True),
			"message": "",
			"plugin": {},
		}
 
	def __enter__(self):
		# 非新用户
		_kwargs = {"uid": self.kwargs.get("uid", 0), "gid": self.kwargs.get("gid", 0)}
		select_result:dict = tool.db.select_records(**_kwargs)
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

	def __exit__(self,exc_type,exc_value,exc_trackback):
		pass