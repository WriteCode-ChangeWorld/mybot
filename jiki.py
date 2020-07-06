"""
jiki一下
"""
import requests
import json
import re
import random

from error import error

class Jiki:
	def __init__(self):
		self.headers = {
			"Content-Type":"application/json;charset=UTF-8",
			"Client":"web",
			"Client-Version":"2.1.66a",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
		}
		self.auto_complete = "https://api.jikipedia.com/go/auto_complete"
		self.api = "https://api.jikipedia.com/go/search_definitions"
		self.eval_cqp_data = ""

	def check(self,eval_cqp_data):
		"""
		判断是否为jiki命令
		使用方法为jiki关键词
		如：jiki百度
		"""
		self.eval_cqp_data = eval_cqp_data
		word = eval_cqp_data["message"].split("jiki ")[-1]
		if len(word) > 10 and "[CQ:" in word:
			return {"res":"不支持该类型消息"}
			# print("不支持该类型消息")
		else:
			i = {}
			i["title"],i["res"] = self.jiki(word)
			i["complete"] = self.complete(word)
			return i

	def jiki(self,word):
		"""
		:params word: 查询关键词
		:return : 错误返回/正确返回结果,处理
		"""
		data = {
			"phrase":word,
			"page":1
		}
		try:
			resp = requests.post(self.api,headers=self.headers,data=json.dumps(data),timeout=10)
		except:
			res = error(self.eval_cqp_data)
			return res
		resp.encoding = "utf8"
		try:
			resp = json.loads(resp.text)["data"]
			# resp = json.loads(resp.text)["data"][0]
			for i,j in enumerate(resp):
				# print(resp[i]["term"]["title"])
				if word == resp[i]["term"]["title"]:
					title = resp[i]["term"]["title"]
					# res = resp["content"].replace("]","")
					res = re.sub(r"\[.*?:","",resp[i]["content"].replace("]",""))
					break
			else:
				i = random.randint(1,len(resp))-1
				title = resp[i]["term"]["title"]
				# res = res[0]["content"].replace("]","")
				res = re.sub(r"\[.*?:","",resp[i]["content"].replace("]",""))
		except Exception as e:
			print(e)
			return "","查找不到相关释义"
		else:
			return title,res
			# return res.replace("\n","")
		
	def complete(self,word):
		"""
		:params word: 关键字
		:return :联想字
		"""
		data = {
			"phrase":word
		}
		try:
			resp = requests.post(self.auto_complete,headers=self.headers,data=json.dumps(data),timeout=10)
		except:
			res = error(self.eval_cqp_data)
			return res
		resp.encoding = "utf8"
		d = json.loads(resp.text)["data"]
		if d == []:
			return "联想词:无"
		else:
			return "联想词为:\n{}".format(",".join([i["word"] for i in d[:10]]))


jk = Jiki()