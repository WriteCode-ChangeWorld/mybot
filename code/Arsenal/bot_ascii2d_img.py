import requests
from lxml import etree

from Arsenal.basic.BNConnect import baseRequest
# from Arsenal.basic.log_record import logger

class Ascii2d_Img:
	"""Ascii2d搜图站点插件,返回色彩检索及特征检索的结果"""
	def __init__(self):
		self.host = "https://ascii2d.net"
		self.color = "https://ascii2d.net/search/color/"
		self.bovw = "https://ascii2d.net/search/bovw/"
		self.testing = "https://ascii2d.net/search/url/{}"
		self.headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like G\
					ecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
		}

		# 数据包字段
		self.eval_cqp_data = {}
		self.user_id = ""
		self.msg = ""
		self.message_type = ""

	def parse(self, eval_cqp_data):
		# executor传入方法
		# 解析群聊/私聊
		self.eval_cqp_data = eval_cqp_data
		self.user_id = self.eval_cqp_data.get("user_id","")
		self.msg = self.eval_cqp_data.get("message","")
		self.message_type = self.eval_cqp_data.get("message_type","")

		# if self.message_type == "group":
		# 	return self.search()
		# elif message_type == "private":
		# 	return self.img_private()

		u = "https://i0.hdslb.com/bfs/article/6d4b2d9eb84f2d8df99918a077493fc9afd54092.jpg"
		# u = "https://i.pximg.net/img-master/img/2019/01/18/20/12/54/72722796_p0_master1200.jpg"
		# 异常
		# u = "https://ascii2d.net/thumbnail/c/a/2/3/ca23fd4753e51d0b95692f67bebd740c.jpg"
		# u = "https://ascii2d.net/thumbnail/f/a/3/f/fa3fc57e31c46f2c5c29d621344c2023.jpg" pass
		u = "https://ascii2d.net/thumbnail/c/2/8/7/c2870ad3cb956814f6930467ecc9d4b6.jpg" # pass
		# u = "https://ascii2d.net/thumbnail/a/0/d/b/a0db9fa34bcbb5306fb33af142b5627b.jpg" pass
		# u = "https://ascii2d.net/thumbnail/3/a/d/7/3ad7d4c277736b3e10f39c573660371f.jpg" # pass
		# u = "https://ascii2d.net/thumbnail/8/5/e/0/85e01e50f430404d1b3e180b15e7f71a.jpg" pass

		# target = self.testing.format(u)
		self.search(self.testing.format(u))

	def search(self,target):
		# 先色合检索再特征检索
		resp = baseRequest(target)
		if "color" not in resp.url:
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
		bovw_resp = baseRequest(img_bovw_url)
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

Bot_Ascii2d_Img = Ascii2d_Img()