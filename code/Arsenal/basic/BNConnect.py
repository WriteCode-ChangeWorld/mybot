# -*- encoding: utf-8 -*-
'''
@File    :   BNConnect.py
@Time    :   2020/07/15 11:22
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import time
import requests
import cloudscraper
# 强制取消警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from Arsenal.basic.log_record import logger

# pixiv
pixiv_headers = {
	"Host": "www.pixiv.net",
	"referer": "https://www.pixiv.net/",
	"origin": "https://accounts.pixiv.net",
	"accept-language": "zh-CN,zh;q=0.9",	# 返回translation,中文翻译
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


general_headers = {
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


def baseRequest(options,
		method = "GET",
		data = None,
		params = None,
		retry_num = 5
		):
	'''
	:params options: 请求参数
		{"headers":"your headers","url":"example.com"}
	:params method:
		"GET"/"POST"
	:params data: POST data
	:params params: GET params
	:params retry_num 重试次数
	:return response or False

	options支持自定义headers,否则使用默认的headers

	添加referer时,referer需要是上一个页面的url,比如:画师/作品页面的url时,则可以自定义请求头
	demo如下:
	demo_headers = headers.copy()
	demo_headers['referer']  = 'www.example.com'
	options ={
		"url": origin_url,
		"headers": demo_headers
	}
	baseRequest(options = options)
	这样baseRequest中使用的headers则是定制化的headers,而非默认headers
	'''
	if "headers" in options.keys():
		base_headers = options["headers"]
	elif "pixiv" in options["url"] and "headers" not in options.keys():
		base_headers = pixiv_headers
	elif "headers" not in options.keys():
		base_headers = general_headers

	logger.debug(f"<options> - {options}")
	logger.debug(f"<base_headers> - {base_headers}")
	try:
		response = requests.request(
				method,
				options["url"],
				data = data,
				params = params,
				cookies = options.get("cookies",""),
				headers = base_headers,
				verify = False,
				timeout = options.get("timeout",5),
			)
		response.encoding = "utf8"
		return response
	except Exception as e:
		logger.warning(f"<err> - network requests err | <Exception> - {e}")
		if retry_num > 0:
			time.sleep(0.2)
			return baseRequest(options, method, data, params, retry_num=retry_num-1)
		else:
			logger.info(f"<options> - {options}")
			logger.warning(f"<err> - network requests err | no retry times")
			return 

def scraperRequest(options,
		method = "GET",
		scraper = None,
		data = None,
		params = None,
		retry_num = 5
		):
	'''
	:params options: 请求参数
		{"headers":"your headers","url":"example.com"}
	:params method:
		"GET"/"POST"
	:params scraper: cloudscraper.CloudScraper
	:params data: POST data
	:params params: GET params
	:params retry_num 重试次数
	:return response or False

	options支持自定义headers,否则使用默认的headers
	'''
	if "headers" in options.keys():
		base_headers = options["headers"]
	elif "pixiv" in options["url"] and "headers" not in options.keys():
		base_headers = pixiv_headers
	elif "headers" not in options.keys():
		base_headers = general_headers

	logger.debug(f"<options> - {options}")
	logger.debug(f"<base_headers> - {base_headers}")

	if not scraper:
		scraper = cloudscraper.create_scraper()

	try:
		response = scraper.request(
				method,
				options["url"],
				data = data,
				params = params,
				cookies = options.get("cookies",""),
				headers = base_headers,
				# verify = False,
				timeout = options.get("timeout",10),
			)
		response.encoding = "utf8"
		return response
	except Exception as e:
		logger.warning(f"<err> - network requests err | <Exception> - {e}")
		if retry_num > 0:
			time.sleep(0.2)
			return scraperRequest(options, method, scraper, data, params, retry_num=retry_num-1)
		else:
			logger.info(f"<options> - {options}")
			logger.warning(f"<err> - network requests err | no retry times")
			return 