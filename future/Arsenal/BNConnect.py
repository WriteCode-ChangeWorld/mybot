# coding=utf8
"""
__time__:2020/07/15 11:22
__author__:Coder-Sakura
BNConnect,格式化输出及一个健壮的,可拓展的基本网络请求函数
"""
import requests
import time

def log_str(*args,end=None):
    for i in args:
        print('[{}] {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"),i),end=end)

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
		base_headers = [options["headers"] if "headers" in options.keys() else self.headers][0]

		try:
			response = requests.request(
					method,
					options["url"],
					data = data,
					params = params,
					cookies = options.get("url",""),
					headers = base_headers,
					verify = False,
					timeout = 10,
				)
			return response
		except  Exception as e:
			if retry_num > 0:
				return self.baseRequest(options,data,params,retry_num-1)
			else:
				log_str(DM_NETWORK_ERROR_INFO.format(self.class_name,options["url"],e))