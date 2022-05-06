# -*- encoding: utf-8 -*-
'''
@File    :   ascii2d.py
@Time    :   2022/03/31 22:47:24
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import os
import re
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

		self.limit_byte = 5 * 1024 * 1024

	@staticmethod
	def _err_code(code:int):
		code_info = {
			"429": "Too many request - 太多请求,请稍后再试",
			"403": "Forbidden,or token unvalid - 服务器拒绝或api_key未设置",
			"413": "Request Entity Too Large - 图片大小过大",
			"430": "禁止访问,请重试.",
			"500": "服务端(ascii2d.net)错误",
			"520": "空白、未知、意外响应或图片大小过大",

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

		if not ascii2d_resp:
			return self._err_code(998)

		# err_code text
		if isinstance(ascii2d_resp, str):
			return ascii2d_resp

		
		ascii2d_resp.results_bovw = []
		if self.bovw:
			ascii2d_bovw_resp = self.exec_bovw()
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
		# local file
		elif file:
			if os.path.getsize(file) >= self.limit_byte:
				logger.warning(f"{self._err_code(413)} - {file}")
				return self._err_code(413)
				
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
		else:
			return self._err_code(999)


		if not resp:
			logger.warning(f"No Resp - {resp}")
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
		logger.debug(f"Length-ascii2d_resp.results - {len(ascii2d_resp.results)}")
		[logger.debug(i.__dict__) for i in ascii2d_resp.results]

		# 去除空数据的box4
		new_results = [r for r in ascii2d_resp.results \
              if not (r.pic_link == "unknown" and r.pic_name == "unknown" and \
             r.author_link == "unknown" and r.author == "unknown" and r.type == "unknown")]

		# 更新筛选后的box
		if not new_results:
			ascii2d_resp.results = ascii2d_resp.results[1]
		else:
			ascii2d_resp.results = new_results

		# 提高相同分辨率,size更大的box的权重
		if len(ascii2d_resp.results) != 1:
			_info = ascii2d_resp.results[0].info
			_resolution = _info.split(" ")[0]
			_size = int(re.sub("[a-zA-Z]", "", _info.split(" ")[-1]))

			for i in range(len(ascii2d_resp.results)):
				i_list = ascii2d_resp.results[i].info.split(" ")
				if i_list[0] == _resolution and int(re.sub("[a-zA-Z]", "", i_list[-1])) > _size:
					ascii2d_resp.results[0], ascii2d_resp.results[i] = ascii2d_resp.results[i], ascii2d_resp.results[0]

		return ascii2d_resp