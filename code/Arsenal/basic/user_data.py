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
	def __init__(self, eval_cqp_data):
		self.judge_data = self.get_judge_data(eval_cqp_data)
		self.mybot_data = {
			"arrange": eval_cqp_data,
			"user_info": {},
			"sender": {
				"user_id": int(self.judge_data.get("uid", 0)),
				"group_id": int(self.judge_data.get("gid", 0)),
				"type": self.judge_data.get("message_type", 0),
			},
			"at": self.kwargs.get("at", True),
			# 回复消息
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
			group_result = tool.db.select_records(table="group_chats", **{"gid":self.kwargs.get("gid", 0)})
			if group_result:
				group_level = int(group_result.get("group_level", tool.level["general_group_level"]))
			else:
				group_level = tool.level["general_group_level"]
			# group_level = int(tool.db.select_records(table="group_chats", **{"gid":self.kwargs["gid"]})["group_level"])

			if group_level >= tool.level["vip_group_level"]:
				result:dict = tool.db.insert_records(self.mybot_data, **{"level": tool.level["vip_user_level"]})
			else:
				result:dict = tool.db.insert_records(self.mybot_data)
		else:
			result:dict = select_result[0]

		self.mybot_data["user_info"] = result
		return self.mybot_data

	def __exit__(self,exc_type,exc_value,exc_trackback):
		pass

	def get_judge_data(self, eval_cqp_data):
		message = eval_cqp_data.get("message", "")
		uid = eval_cqp_data.get("user_id",0)
		gid = eval_cqp_data.get("group_id",0)
		message_type = eval_cqp_data.get("message_type", "")

		judge_data = {"uid": uid, "gid": gid, "message_type": message_type, "message": message}
		
		for k in list(judge_data.keys()):
			if not judge_data[k]:
				del judge_data[k]

		if not judge_data:
			return {}
		return judge_data
