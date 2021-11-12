import os
import time
import random
from lxml import etree
# pip3 install PyExecJS 
# import execjs,datetime

from basic.plus_res_directory import pdr

def return_value(name1,name2):
	try:
		h = etree.parse('poken.html')
	except:
		print('将poken.html放在同一目录/修改打开路径')
		exit()

	o = h.xpath('//div[@class="list"]//option')	

	res = []	# 记录value
	res1 = {}	# 记录隐藏text和value

	for i in o:
		value_dict = {}
		# 获得name对应的value
		if str(i.xpath('./text()')[0]) == name1:
			value_dict[name1] = int(i.xpath('./@value')[0]) # n1 v1
		if str(i.xpath('./text()')[0]) == name2:
			value_dict[name2] = int(i.xpath('./@value')[0]) # n2 v2
		if value_dict:
			res.append(value_dict)
	print("res",res)

	if len(res) < 2 and name1 != name2:
		print('两只宝可梦中存在暂不支持的宝可梦')
		exit()

	o1 = h.xpath('//div[@class="name1"]//option')
	for i in o1:
		if int(i.xpath('./@value')[0]) == res[0]:
			res1[str(i.xpath('./text()')[0])] = res[0]
			break

	o2 = h.xpath('//div[@class="name2"]//option')
	for i in o2:
		if int(i.xpath('./@value')[0]) == res[1]:
			res1[str(i.xpath('./text()')[0])] = res[1]
			break

	return res,res1


class Pokenman:
	"""宝可梦杂交"""
	def __init__(self):
		self.bot_name = type(self).__name__
		self.workspace = pdr.get_plus_res(self.bot_name)

		self.blend_path = os.path.join(self.workspace,"blend")
		self.raw_path = os.path.join(self.workspace,"raw")
		self.blend_img = "https://images.alexonsager.net/pokemon/fused/{}/{}.{}.png"
		self.raw_img = "https://images.alexonsager.net/pokemon/{}.png"

		self.html_path = os.path.join(self.workspace,"poken.html")
		self.html_options = self.pokenman_parse()

	def pokenman_parse(self,class_name="list"):
		"""解析并获得宝可梦名单"""
		h = etree.parse(self.html_path)
		o = h.xpath('//div[@class="{}"]//option'.format(class_name))
		return o

	def get_spirit_data(self,spirit_list=None):
		"""
		获取两个宝可梦的数据
		:return:
			spirit_data = {
					'father': {'name': '超梦', 'value': '150', 'path': '150.png'},
					'mother': {'name': '超梦', 'value': '150', 'path': '150.png'}
			}
		"""
		spirit_data = {"father":{},"mother":{}}
		# 未指定两个杂交的宝可梦名称
		if not spirit_list:
			for i in range(2):
				item = {}
				option = random.choice(self.html_options)
				item["name"] = option.xpath("./text()")[0]
				value = option.xpath("./@value")[0]
				item["value"] = value
				item["path"] = os.path.join(self.raw_path,"{}.png".format(value))

				if spirit_data["father"] != {}:
					spirit_data["mother"] = item
				else:
					spirit_data["father"] = item
				# spirit_data.append(item)
		# 指定spirit_list
		else:
			for spirit in spirit_list:
				def find_spirit(spirit):
					item = {}
					for option in self.html_options:
						if option.xpath('./text()')[0] == spirit:
							item["name"] = option.xpath("./text()")[0]
							value = option.xpath("./@value")[0]
							item["value"] = value
							item["path"] = os.path.join(self.raw_path,"{}.png".format(value))
							# item[spirit] = int(option.xpath('./@value')[0])
							break
					return item
				item = find_spirit(spirit)
				if spirit_data["father"] != {}:
					spirit_data["mother"] = item
				else:
					spirit_data["father"] = item
				# spirit_data.append(item)
		
		return spirit_data

	def blend(self,name1=None,name2=None):
		"""
		根据指定的2个宝可梦合成信息
		:params name1: 宝可梦1
		:params name2: 宝可梦2
		:return:
			spirit_data = {
					'father': {'name': '超梦', 'value': '150', 'path': '150.png'},
					'mother': {'name': '超梦', 'value': '150', 'path': '150.png'}
			}
			blend_path = "150.150.png"
		"""
		spirit_list = None
		if name1 and name2:
			spirit_list = [name1,name2]

		spirit_data = self.get_spirit_data(spirit_list=spirit_list)
		# print("spirit_data_father",spirit_data["father"]["name"])
		# print("spirit_data_mother",spirit_data["mother"]["name"])

		blend_data = {}
		# 杂交后命名 father在前
		blend_name = ""
		for options in self.pokenman_parse(class_name="name1"):
			if options.xpath('./@value')[0] == spirit_data["father"]["value"]:
				blend_name += options.xpath('./text()')[0]
				break

		for options in self.pokenman_parse(class_name="name2"):
			if options.xpath('./@value')[0] == spirit_data["mother"]["value"]:
				blend_name += options.xpath('./text()')[0]
				break


		# 杂交后的img mother在前
		blend_filename = "{}.{}.png".format(
			spirit_data["mother"]["value"],
			spirit_data["father"]["value"]
			)
		blend_data["name"] = blend_name
		blend_data["path"] = os.path.join(self.blend_path,blend_filename)
		

		return spirit_data,blend_data

	def service_func(self,eval_cqp_data):
		if eval_cqp_data.get('message_type','') == 'group':
			group_id = eval_cqp_data["group_id"]
			user_id = eval_cqp_data["user_id"]
			message = eval_cqp_data['message']
			keyword = "宝可梦杂交"

			# 未触发关键词
			if message != keyword:
				return 

			spirit_data,blend_data = self.blend()
			
			# father在前
			data_raw_spirit = {
                "group_id": group_id,
                "message": "[CQ:at,qq={}]\n本次杂交实验目标\n[CQ:image,file=file:///{}]\n\n[CQ:image,file=file:///{}]".format(
					user_id,spirit_data["father"]["path"],
					spirit_data["mother"]["path"])
            }

			blend_result_text = "杂交成功！得到了新的宝可梦!"
			if spirit_data["father"]["value"] == spirit_data["mother"]["value"]:
				blend_result_text = "杂交失败...得到了'新'的宝可梦?"

			# 杂交公式
			blend_spirit_text = "杂交公式:\n{} + {} = {}".format(
				spirit_data["father"]["name"],
				spirit_data["mother"]["name"],
				blend_data["name"]
				)
			print(blend_spirit_text)

			data_blend_spirit = {
                "group_id": group_id,
                "message": "[CQ:at,qq={}]\n{}\n{}\n[CQ:image,file=file:///{}]".format(
					user_id,blend_result_text,blend_spirit_text,blend_data["path"]
					)
            }
			# print(data_raw_spirit,"\n",data_blend_spirit)
			return data_raw_spirit,data_blend_spirit

	# 前期素材准备
	def download_img(self):
		# 目前一共151位宝可梦
		# 杂交结果...
		import requests
		headers = {
			"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (\
				KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
		}
		# blend_img = "https://images.alexonsager.net/pokemon/fused/{}/{}.{}.png"
		# raw_img = "https://images.alexonsager.net/pokemon/{}.png"
		# blend_path = os.path.join(self.workspace,"blend")
		# raw_path = os.path.join(self.workspace,"raw")

		# 原始图像
		for i in range(1,152):
			now_raw_path = os.path.join(self.raw_path,"{}.png".format(i))
			if not os.path.exists(now_raw_path):
				resp = requests.get(self.raw_img.format(i),headers=headers).content
				with open(now_raw_path,"wb") as f:
					f.write(resp)
			# print(now_raw_path)

		# 杂交图像
		for i in range(1,152):
			for j in range(1,152):
				now_blend_path = os.path.join(self.blend_path,"{}.{}.png".format(i,j))
				if not os.path.exists(now_blend_path):
					resp = requests.get(self.blend_img.format(i,i,j),headers=headers).content
					with open(now_blend_path,"wb") as f:
						f.write(resp)
				print(now_blend_path)
				# break
			# break


Bot_Pokenman = Pokenman()
# Bot_Pokenman.blend()
# Bot_Pokenman.blend("超梦","梦幻")
# Bot_Pokenman.blend("梦幻","超梦")
# Bot_Pokenman.blend("超梦","超梦")
# Bot_Pokenman.service_func({"group_id":1122334,"user_id":1508015265,"message_type":"group","message":"宝可梦杂交"})
# Bot_Pokenman.download_img()
			


# if __name__ == '__main__':
# 	o = test_list()
# 	n1 = input('第一位宝可梦:')
# 	n2 = input('第二位宝可梦:')

# 	if n1 == '' or n2 == '' or n1.isdecimal() == True or n2.isdecimal() == True:
# 		print('宝可梦名字不能为空/数字')
# 		exit()
# 	res,res1 = return_value(n1,n2)
# 	result = ''.join(r for r in res1)
# 	# img_url = "https://images.alexonsager.net/pokemon/fused/58/58.21.png"
# 	img_url = "https://images.alexonsager.net/pokemon/fused/{}/{}.{}.png".\
# 		format(res[-1].values,res[-1],res[0])
# 	print(result,res,res1)
# 	print(img_url)


	# for n1 in o:
	# 	for n2 in o:
	# 		try:
	# 			res = return_value(n1,n2)
	# 			res = ''.join(r for r in res)	# new_name
	# 			# print	(res)	# new_name
	# 			with open('result.txt','a') as f:
	# 				f.write(res)
	# 				f.write('\n')
	# 		except:
	# 			print(n1,n2)

	# j = open('poken.js','r')
	# c = execjs.compile(j.read())
	# j.close()
	# res = c.call('p',r1,r2,v1,v2)

	# print(res)