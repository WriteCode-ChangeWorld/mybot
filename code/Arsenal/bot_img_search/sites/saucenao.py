# -*- encoding: utf-8 -*-
'''
@File    :   saucenao.py
@Time    :   2022/02/20 02:10:46
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
from requests_toolbelt import MultipartEncoder

from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.BNConnect import baseRequest
from Arsenal.basic.msg_temp import IMG_SEARCH_TEMP_GENG

from Arsenal.bot_img_search.utils import SauceNaoResp
from Arsenal.bot_img_search.img_search_tool import DB_id


class SauceNao:
	def __init__(self, 
				 api_key: str =  None,
				 db: int = 999,
				 output_type: int = 2,
				 testmode: int = 0,
				 numres: int = 5,
				)->None:
		# saucenao doc: https://saucenao.com/user.php?page=search-api
		self.search_url = "https://saucenao.com/search.php"
		self.min_similarity = 60

		params = {
			"testmode": testmode,
			"numres": numres,
			"output_type": output_type,
			"db": db
		}
		self.api_key = tool.config["Plugin"]["saucenao"]["api_key"] if not api_key else api_key
		if self.api_key:
			params["api_key"] = self.api_key

		self.params = params

	@staticmethod
	def _err_code(code:int):
		code_info = {
			"429": "Too many request - 太多请求,请稍后再试",
			"403": "Forbidden,or token unvalid - 服务器拒绝或api_key未设置",
			"413": "Request Entity Too Large - 图片大小过大",
			"430": "Request Entity Too Large -- 图片大小过大",
			"500": "",
			"503": "Request Entity Too Large -- 图片大小过大",

			# 自定义
			"997": "短时(30秒)搜索次数为零,请等待30秒后重试或使用其他搜图引擎~",
			"998": "长时(24小时)搜索次数为零,请等待24小时后重试或使用其他搜图引擎~",
			"999": "未知错误,请联系管理员",
		}
		if str(code) in code_info:
			return code_info[str(code)]
		else:
			return "Unknown err code"

	def search(self, 
				url:str = None,
				file:str = None)->SauceNaoResp or str:
		"""
		通过SauceNao进行反向图像搜索

		Params
		-----------
		:param url: network img url
		:param file: local img url

		Return SauceNaoResp or str
		attributes
		-----------
		+ .short_limit = 剩余搜索次数/30s
		+ .long_limit = 剩余搜索次数/24h
		+ .results = Parsed data
		+ .results[0] = First index of Parsed data
		+ .results[0].index_id = 数据库id
		+ .results[0].similarity = 相似度
		+ .results[0].thumbnail = 缩略图url
		+ .results[0].title = 图片标题 / 漫画标题
		+ .results[0].url = 图片链接 / 原始链接
		+ .results[0].member_name = 作者名称
		+ .results[0].pixiv_id = pixiv插画id
		+ .results[0].member_id = pixiv作者uid
		+ .results[0].doujinName = 同人本名称
		+ .results[0].anilist_id = anilist番剧id

		str - err message to client
		"""
		params = self.params
		options = {"url": self.search_url}

		# network url
		if url:
			params["url"] = url
			logger.debug(f"SauceNao.params - {params}")
			resp = baseRequest(options=options, params=params)
		# local file
		elif file:
			m = MultipartEncoder(fields={
					"file": ("filename", open(file, "rb"),  "type=multipart/form-data")
				}
			)
			options["headers"] = {'Content-Type': m.content_type}
			logger.debug(f"SauceNao.params - {params}")
			resp = baseRequest(method="POST", options=options, data=m, params=params)
		else:
			logger.warning(IMG_SEARCH_TEMP_GENG["saucenao_param_err"].format(
				f"<url>:{url} - <file>:{file}"
			))
			return self._err_code(999)

		if not resp:
			logger.warning(IMG_SEARCH_TEMP_GENG["saucenao_param_err"].format(
				f"<url>:{url} - <file>:{file}"
			))
			return self._err_code(999)
		elif resp.status_code != 200:
			logger.error(f"{self._err_code(resp.status_code)}")
			logger.error(f"{resp.text}")
			return self._err_code(resp.status_code)
		else:
			saucenao_resp = SauceNaoResp(resp.json())
			saucenao_resp = self.deal_with_resp(saucenao_resp)
			return saucenao_resp

	def deal_with_resp(self, saucenao_resp:SauceNaoResp)->SauceNaoResp or str:
		logger.debug(f"Length-saucenao_resp.results - {len(saucenao_resp.results)}")
		[logger.debug(i.__dict__) for i in saucenao_resp.results]

		# 短时次数
		if saucenao_resp.short_limit <= 0:
			return self._err_code(997)
		# 长时次数
		if saucenao_resp.long_limit <= 0:
			return self._err_code(998)

		# db:all 第一个结果为非pixiv网站时,给予pixiv额外权重
		if self.params["db"] == DB_id["all"] and \
			saucenao_resp.results[0].index_id != DB_id["pixiv"]:
			for _ in saucenao_resp.results:
				# pixiv 1.03x权重
				if _.index_id == DB_id["pixiv"]:
					_.similarity = float(_.similarity * 1.03)
				# doujin 0.97x权重
				if _.index_id == DB_id["doujin"]:
					_.similarity = float(_.similarity * 0.97)

		# 尝试丢弃盗图者或已删除的记录 - 实验性功能
		first_result = saucenao_resp.results[0]
		if first_result.index_id == DB_id["pixiv"]:
			_pixivList = [_ for _ in saucenao_resp.results\
				if _.index_id == DB_id["pixiv"] and _.similarity >= first_result.similarity-5.0]
			# TODO 待校验该逻辑是否合理
			if len(_pixivList) == 1:
				saucenao_resp.results = [first_result]
				return saucenao_resp
			else:
				second_result = saucenao_resp.results[0]
				# 画师不同, 前者pid大于后者 - 选择后者
				if first_result.member_name != second_result.member_name and \
					first_result.pixiv_id > second_result.pixiv_id:
					saucenao_resp.results = [second_result]
					return saucenao_resp

			# second_result.index_id == DB_id["pixiv"] and \
			# saucenao_resp.results

		return saucenao_resp


		














"""
	# ========== DELETE ==========
	def parse(self, eval_cqp_data):
		# executor解析方法
		self.eval_cqp_data = eval_cqp_data
		self.user_id = self.eval_cqp_data.get("user_id", "")
		self.msg = self.eval_cqp_data.get("message", "")
		self.message_type = self.eval_cqp_data.get("message_type", "")

		if self.message_type == "group":
			return self.img_group()
		# 暂时不做私聊
		elif self.message_type == "private":
			return self.img_private()

	def img_group(self):
		# 群聊搜图方法动作触发
		print("当前调用QQ:{},群组搜图列表:{}".format(self.user_id,self.search_image_group_list))

		# 消息 == 开启搜图模式命令
		if self.msg == SEARCH_IMG_MSG["search_image_enable"]:
			# 判断是否在搜图名单中,以及恶意开启
			# 开启搜图,未在搜图名单中 --> 添加
			if self.user_id not in self.search_image_group_list:
				self.search_image_group_list.append(self.user_id)
				return self.SEARCH_IMG_MSG["reply_image"].format(self.user_id)
			# 开启搜图,已在搜图名单中 --> 提示
			else:
				return self.SEARCH_IMG_MSG["reply_tip"].format(self.user_id)
		# 消息 == 图片
		elif self.msg.split(',')[0] == '[CQ:image':
			for i in self.search_image_group_list:
				if self.user_id == i:
					msg_url = self.msg.split("url=")[-1].replace("]", "")
					api_key = random.choice(self.saucenao_api_key_list)
					img_url = self.search_image_url.format(api_key, msg_url)
					# 搜图函数组装好搜图结果,返回文字信息
					return self.search_img(img_url, self.eval_cqp_data)
		# 消息 == 关闭搜图
		elif self.msg == SEARCH_IMG_MSG["search_image_quit"]:
			# 判断是否在搜图名单中,以及恶意关闭
			# 关闭搜图,在名单中,删除
			if self.user_id in self.search_image_group_list:
				for i in self.search_image_group_list[::-1]:
					if i == self.user_id:
						self.search_image_group_list.remove(i)
						return self.SEARCH_IMG_MSG["reply_image_quit"].format(self.user_id)
			# 关闭搜图,不在名单中,提示
			else:
				return self.SEARCH_IMG_MSG["reply_enable_search"].format(self.user_id)
		# 消息 == 其他
		else:
			# 搜图模式发送非图片信息,自动关闭
			# print(msg)
			if self.user_id in self.search_image_group_list:
				if self.msg.split(',')[0] != "[CQ:image":
					for i in self.search_image_group_list[::-1]:
						if i == self.user_id:
							self.search_image_group_list.remove(i)
							return self.SEARCH_IMG_MSG["reply_bot_quit"].format(self.user_id)

	# TODO(Coder-Sakura): 2020/07/13 16:09 私聊搜图待添加
	# 2020年9月20日17:59:34 暂时不做私聊
	def img_private(self):
		# 私聊搜图方法动作触发
		pass

	# TODO(Coder-Sakura) 2020/07/13 16:19 headers请求头待验证
	def search_img(self, img_url):
		# 搜图功能函数
		# saucenao,ascii2d等
		# 前五个,60%相似度以上,原图链接多个取前三个,优先pixiv
		try:
			resp = json.loads(requests.get(img_url, timeout=5).text)
		except Exception as e:
			# TODO(Coder-Sakura) 2020/07/13 16:22 异常类统一处理返回结果
			print(e)
			return e

		status = resp["header"].get("status","200")
		# 30秒搜索6次到达限制,待验证
		if status == -2:
			pass

		# >>>>>>>>>> 增加结果可信度 <<<<<<<<<<
		# 按照相似度,整体排序
		resp["results"].sort(key = lambda i:float(i["header"]["similarity"]),reverse = True)
		# 取相似度大于60%的前五个
		results = [i for i in resp["results"] if float(i["header"]["similarity"]) > 60][:5]
		# 根据规则加减分
		for _ in results:
			similarity = float(_["header"]["similarity"])
			source = _["data"].get("source","")

			if _["data"].get("pixiv_id","") != "":
				similarity += 1

			similarity += len(_["data"]["ext_urls"])

			if "pixiv" in source.lower():
				similarity += 1

			if "twitter" in source.lower():
				similarity += 1
			_["header"]["similarity"] = similarity
		# 再排序
		results.sort(key = lambda i:float(i["header"]["similarity"]),reverse = True)
		# 此时取第一个,可信度大
		res = results[0]

		# 缩略图地址
		thumbnail = res["header"].get("thumbnail","")
		# 相似度
		similarity = "{}%".format(res["header"].get("similarity",0.00))
		similarity_res = "相似度: {}\n".format(similarity)
		# 作者/创建者/空
		name = res["data"].get("member_name","")
		if name == "":
			name = res["data"].get("creator","")
		name_res = name if name != "" else ""
		# 作者uid/空
		uid = "{}".format(res["data"].get("member_id",""))
		uid_res = "(%s)"%uid if uid != "" else ""
		name_uid_res = "上传者: {}{}\n".format(name_res,uid_res)
		# 作品标题/空
		title = res["data"].get("title","")
		title_res = "作品标题: {}\n".format(title) if title != "" else ""
		# 作品pid/空
		pixiv_id = str(res["data"].get("pixiv_id",""))
		pixiv_id_res = "作品pid: {}\n".format(pixiv_id) if pixiv_id != "" else ""
		# 作品链接/空
		ext_urls = "\n".join(res["data"].get("ext_urls",[]))
		ext_urls_res = "作品链接:\n{}\n".format(ext_urls) if ext_urls != [] else ""

		# 模板消息
		message = "[CQ:image,file={}]\n".format(thumbnail) +\
				  similarity_res +\
				  name_uid_res +\
				  title_res +\
				  pixiv_id_res +\
				  ext_urls_res

	def reverse_pixiv(self):
		# pixiv直链反代
		pass

# image = Img()

"""