# coding=utf8
"""
__time__:2020/07/15 11:22
__author__:Coder-Sakura
BNConnect,格式化输出及一个健壮的,可拓展的基本网络请求函数
"""
import time
import requests
# 强制取消警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 0502 暂时
import os
from loguru import logger
root_path = r"D:\Code\mybot\code\log"
# root_path = os.getcwd()
logger.add(
    os.path.join(root_path,"{time}.log"),
    encoding="utf-8",
    rotation="12:00"
    )
# 0502

headers = {
	"Host": "www.pixiv.net",
	"referer": "https://www.pixiv.net/",
	"origin": "https://accounts.pixiv.net",
	"accept-language": "zh-CN,zh;q=0.9",	# 返回translation,中文翻译的标签组
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

def log_str(*args,end=None):
	global logger
	for i in args:
		text = '[{}] {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"),i)
		# print(text,end=end)
		logger.debug(text)


def baseRequest(options,method="GET",data=None,params=None,retry_num=5):
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

	下面这行列表推导式作用在于：
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
	# log_str(options["url"])
	base_headers = [options["headers"] if "headers" in options.keys() else headers][0]

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
		if retry_num > 0:
			return baseRequest(options,data,params,retry_num=retry_num-1)
		else:
			# log_str(DM_NETWORK_ERROR_INFO.format(self.class_name,options["url"],e))
			print("网络请求出错 url:{}".format(options["url"]))
			return 