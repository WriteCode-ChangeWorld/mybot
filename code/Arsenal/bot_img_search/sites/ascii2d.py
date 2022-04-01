# -*- encoding: utf-8 -*-
'''
@File    :   ascii2d.py
@Time    :   2022/03/31 22:47:24
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
# import requests
from httpx import options
from lxml import etree
from requests_toolbelt import MultipartEncoder

from Arsenal.basic.log_record import logger
from Arsenal.basic.BNConnect import scraperRequest, general_headers
from Arsenal.basic.msg_temp import IMG_SEARCH_TEMP_GENG

from Arsenal.bot_img_search.utils import Ascii2dResp

class Ascii2d:
	def __init__(self, 
				 bovw: bool = True,
				 nums: int = 5,
				 )->None:
		self.host = "https://ascii2d.net"
		self.color = "https://ascii2d.net/search/color/"
		self.bovw = "https://ascii2d.net/search/bovw/"
		self.search_url = "https://ascii2d.net/search/url/{}"
		self.search_file = "https://ascii2d.net/search/file"

		self.bovw = bovw
		self.nums = nums
		self.color_url = ""
		self.bovw_url = ""

	# TODO
	@staticmethod
	def _err_code(code:int):
		code_info = {
			"429": "Too many request - 太多请求,请稍后再试",
			"403": "Forbidden,or token unvalid - 服务器拒绝或api_key未设置",
			"413": "Request Entity Too Large - 图片大小过大",
			"430": "Request Entity Too Large -- 图片大小过大",
			"500": "",
			"503": "Request Entity Too Large -- 图片大小过大",

			"998": "ascii2d访问超时, 请稍后再试",
			"999": "未知错误,请联系管理员",
		}
		if str(code) in code_info:
			return code_info[str(code)]
		else:
			return "Unknown err code"

	def search(self, 
				url:str = None,
				file:str = None)->Ascii2dResp or str:
		"""
		通过Ascii2D进行反向图像搜索

		Params
		-----------
		:param url: network img url
		:param file: local img url

		Return Ascii2dResp or str
		attributes
		-----------
		+ .results = Parsed data
		+ .results_bovw = bovw Parsed data
			若未指定特征检索, 则results_bovw为[].
			否则则results_bovw为数据结构与results一致.
		+ .results[0] = First index of Parsed data
		+ .results[0].info = 图片信息
		+ .results[0].pic_link = 图片链接
		+ .results[0].pic_name = 图片名称
		+ .results[0].author_link = 作者链接
		+ .results[0].author = 作者名称
		+ .results[0].thumb = 缩略图
		+ .results[0].type = 类型

		str - err message to client
		"""
		logger.debug(IMG_SEARCH_TEMP_GENG["param_err"].format(
			f"<url>:{url} - <file>:{file}"
		))

		ascii2d_resp = self.exec(url, file)
		if isinstance(ascii2d_resp, str):
			return ascii2d_resp
		elif not ascii2d_resp:
			return self._err_code(998)
		
		ascii2d_resp.results_bovw = []
		if self.bovw:
			ascii2d_bovw_resp = self.exec_bovw()
			if isinstance(ascii2d_resp, str):
				ascii2d_resp.results_bovw = []
			else:
				ascii2d_resp.results_bovw = ascii2d_bovw_resp.results

		return ascii2d_resp

	def exec(self,
			 url:str = None,
			 file:str = None)->Ascii2dResp or str:
		logger.info(f"Ascii2d Color Mode Searching")
		# network url
		if url:
			_url = self.search_url.format(url)
			resp = scraperRequest(options={"url": _url})
			# resp = scraper.get(_url, headers=general_headers, timeout=10)
		# local file
		elif file:
			m = MultipartEncoder(
				fields={"file": ("filename",open(file, "rb"),"type=multipart/form-data",)}
			)
			headers = general_headers.copy()
			headers["Content-Type"] = m.content_type

			resp = scraperRequest(
				options={"url": self.search_file, "headers":headers},
				method="POST",
				data=m
			)
			# import cloudscraper
			# scraper = cloudscraper.create_scraper()
			# resp = scraper.post(self.search_file, headers=headers, data=m, timeout=10)
		else:
			return self._err_code(999)


		if not resp:
			return self._err_code(999)
		elif resp.status_code != 200:
			logger.error(f"{self._err_code(resp.status_code)}")
			logger.error(f"{resp.text[:300]}")
			return self._err_code(resp.status_code)
		else:
			self.color_url = resp.url
			self.bovw_url = self.color_url.replace("color", "bovw")
			obj = etree.HTML(resp.text).xpath("""//div[@class="row item-box"]""")[:self.nums]
			ascii2d_resp = Ascii2dResp(obj)
			ascii2d_resp = self.deal_with_resp(ascii2d_resp)
			return ascii2d_resp
	
	def exec_bovw(self)->Ascii2dResp or str:
		logger.info(f"Ascii2d Bovw Mode Searching")
		resp = scraperRequest(options={"url": self.bovw_url})
		# resp = scraper.get(self.bovw_url, headers=general_headers, timeout=10)

		if not resp:
			return self._err_code(999)
		elif resp.status_code != 200:
			logger.error(f"{self._err_code(resp.status_code)}")
			logger.error(f"{resp.text[:300]}")
			return self._err_code(resp.status_code)
		else:
			obj = etree.HTML(resp.text).xpath("""//div[@class="row item-box"]""")[:self.nums]
			ascii2d_resp = Ascii2dResp(obj)
			ascii2d_resp = self.deal_with_resp(ascii2d_resp)
			return ascii2d_resp
	
	def deal_with_resp(self, ascii2d_resp:Ascii2dResp)->Ascii2dResp or str:
		return ascii2d_resp

	def search_backup(self,target):
		# 先色合检索再特征检索
		# res = httpx.post(target, data=data, **self.requests_kwargs)
		resp = baseRequest(options={"url": target})
		if "color" not in resp.url:
			print(resp.url)
			print("请求出错")
			return 

		# 结果过滤
		print("色合检索")
		result1 = self.find_result(resp)

		img_color_url = resp.url
		# color_resp = resp.text
		img_hash = img_color_url.split("/")[-1]
		img_bovw_url = self.bovw + img_hash

		# 结果过滤
		bovw_resp = baseRequest(options={"url": img_bovw_url})
		print("\n特征检索")
		result2 = self.find_result(bovw_resp)

		print("\nhash",img_hash)
		print(result1,result2)

	def find_result(self,html):
		"""
		20200621
		针对色合和特征都只匹配到tw或pixiv,前者匹配到tw则记录,特征匹配时跳过tw
		{'thumb_url': 'xxx', 'info': []}
		info为空,说明匹配到的是登录详细之类的
		"""
		obj = etree.HTML(html.text.replace("\n",""))

		# 对返回结果进行判断,优先选取pixiv和twitter,次之是Danbooru,yande,最后默认选取第一个
		select_site_ex = """//div[@class="row item-box"]//div[@class="detail-box gray-link"]"""
		sites = []
		gray_link = obj.xpath(select_site_ex)

		# 页面显示: 失敗,現在この画像は検索できません
		if gray_link == []:
			res = {}
			return res

		# 获取所有搜索结果中的site
		for g in gray_link:
			# 只取一条搜索结果中的前两条
			site = g.xpath(""".//h6/small/text()""")[:2]
			# pixiv,tw,niconico匹配不到
			if site == []:
				try:
					site = g.xpath("../div[@class='pull-xs-right']/a/@href")
					if site != []:
						site = site[0].split(r"//")[-1].split(r".")[0]
				except Exception as e:
					print(g.xpath("../div[@class='pull-xs-right']/a/@href"))
					print(e)
					site = []

			# 去重
			if type(site) == type([]):
				site = list(set(site))
			sites.append(site)
		# print(sites)


		# 判断site是否在预定站点内
		# 默认是第一个搜图结果,0是需要搜的图
		num = 1
		# danbooru.donmai.us / kagamihara.donmai.us / konachan.com
		# gelbooru.com / yande.re
		# 尚未遇见的:https://xbooru.com https://rule34.xxx
		extra_sites = ["danbooru.donmai.us","yande.re","kagamihara.donmai.us","konachan.com","gelbooru.com"]
		for index,site in enumerate(sites):
			if site == []:
				continue

			if True in [True if s == "pixiv" else False for s in site]:
				# 加入判断,判断该id是否存在
				num = index
				break
			if True in [True if s == "twitter" else False for s in site]:
				num = index
				break
			# 不满足pixiv和tw的,应该是没有来源信息和作者信息,只有右侧的图站链接
			if True in [True if site[0] in i else False for i in extra_sites]:
				num = index
				break
		# print(num,sites[num],'\n')

		# 匹配结果
		res = {}
		# 正常状态下是pixiv,tw,niconico等,异常下对yande,Danbooru等站点的图进行检测
		item = obj.xpath("""//div[@class="row item-box"]""")[num]
		# 预览图
		try:
			res["thumb_url"] = self.host + item.xpath("""./div[contains(@class,"image-box")]/img/@src""")[0]
		except Exception as e:
			res["thumb_url"] = ""

		# 匹配方式
		# 第一种为图站,异常
		# 第二种为pixiv,tw,niconico
		if True in [True if sites[num][0] in i else False for i in extra_sites]:
			res["source_url"] = item.xpath(""".//div[@class="pull-xs-right"]/a/@href""")[0]
		else:

			res_info = []
			# 只取一条搜索结果中的前两条
			info = item.xpath(""".//div[@class="detail-box gray-link"]//h6""")[:2]
			for i in info:
				data = {}
				# 来源标题
				try:
					data["source_text"] = i.xpath("""./a[1]/text()""")[0].replace("\u3000","")
				except:
					data["source_text"] = ""
				# 来源地址
				try:
					data["source_url"] = i.xpath("""./a[1]/@href""")[0]
				except:
					data["source_url"] = ""
				# 作者
				try:
					data["username"] = i.xpath("""./a[2]/text()""")[0].replace("\u3000","")
				except:
					data["username"] = ""
				# 作者地址: Author
				try:
					data["user_url"] = i.xpath("""./a[2]/@href""")[0]
				except:
					data["user_url"] = ""

				res_info.append(data)
			res["info"] = res_info

		# 格式化输出
		# print(res)
		print("预览图:\n{}".format(res.get("thumb_url","")))
		if res.get("info") == None:
			print("来源地址: {}".format(res.get("source_url")))
		else:
			for r in res.get("info"):
				print("来源标题: {}\n来源地址: {}".format(r.get("source_text"),r.get("source_url")))
				print("作者: {}\n{}".format(r.get("username"),r.get("user_url")))
				print("="*30)

		return res