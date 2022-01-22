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
# 强制取消警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from Arsenal.basic.log_record import logger



headers = {
	"Host": "www.pixiv.net",
	"referer": "https://www.pixiv.net/",
	"origin": "https://accounts.pixiv.net",
	"accept-language": "zh-CN,zh;q=0.9",	# 返回translation,中文翻译
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


def baseRequest(options,
		method="GET",
		data=None,
		params=None,
		retry_num=5
		):
	'''
	:params options 请求参数
		{"method":"get/post","url":"example.com"}
	:params method
		"GET"/"POST"
	:params data
	:params params
	:params retry_num 重试次数
	:return response对象/False

	如果options中有定义了headers参数,则使用定义的;否则使用默认的headers

	下面这行列表推导式作用在于:
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
	base_headers = [options["headers"] if "headers" in options.keys() else headers][0]

	if "pixiv" in options["url"] and not options["headers"]:
		base_headers = headers

	logger.debug(f"<options> - {options}")
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
		logger.info(f"<err> - network requests err | <Exception> - {e}")
		if retry_num > 0:
			time.sleep(0.1)
			return baseRequest(options,data,params,retry_num=retry_num-1)
		else:
			logger.info(f"<options> - {options}")
			logger.info(f"<err> - network requests err | no retry times")
			return 