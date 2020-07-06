"""
处理网络错误
"""

def error(data,m=0):
	if error == None:
		return
	print(data)
	if m == 0:
		message = "网络出错啦！"
	elif m == 1:
		message = "查询的pid错误！"
	else:
		pass

	# 群聊
	if data["message_type"] == "group":
		group_id = data["group_id"]
		at = "[CQ:at,qq=" + str(data['user_id']) + "]"
		
		res = {
			"group_id": group_id,
			"message": at + "\n" + message
		}
	else:
		user_id = data["user_id"]
		res = {
			"user_id": user_id,
			"message": message
		}
	return res
