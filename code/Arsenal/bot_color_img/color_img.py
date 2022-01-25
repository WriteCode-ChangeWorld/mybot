import requests
import json
import random

def get_img(word,limit=None,illust_level=None,num=None,retry_num=3):
	"""
	根据关键字返回1~3张图片

	limit: 最低收藏数
	"""
	api_url = "http://127.0.0.1:1526/api/v2/random"

	if not num:
		num = random.choice(list(range(1,4)))

	data = {
		"num":num,
		# "num":random.choice(list(range(1,6))),
		"extra":word,
		"limit":limit,
		"illust_level":illust_level,
	}
	print(data)
	try:
		resp = requests.post(api_url,data=data,timeout=10)
	except Exception as e:
		if retry_num > 0:
			return get_img(word=word,limit=limit,illust_level=illust_level,num=num,retry_num=retry_num-1)
		else:
			return None
	else:
		# print(resp.text)
		result = json.loads(resp.text)
		return result

# TODO 2020年10月3日17:22:20
# 更新返回模板数据,有tag情况下返回当前tag数据库存量
def parse_img_data(eval_cqp_data):
	msg = eval_cqp_data["message"]
	word = msg[2:-2]

	result = get_img(word)
	# print("result",result)
	if type(result["result"]) != type([]):
		# 无结果返回
		msg = "{}\ntag:{} 暂无数据哦~".format(result["result"]["message"],word)
	else:
		msg = "\n".join([i["reverse_url"] for i in result["result"]])
		# msg = ",".join(['[CQ:image,file={}]'.format(i["reverse_url"]) for i in result["result"]])
		if word:
			msg += "\ntag:{} 共有{}张".format(word,result["count"])
	# print(msg)

	reply_group = {
		"group_id": eval_cqp_data['group_id'],
		"message":"[CQ:at,qq={}]\n".format(eval_cqp_data["user_id"]) + msg
	}
	print("color_img",reply_group)
	return reply_group