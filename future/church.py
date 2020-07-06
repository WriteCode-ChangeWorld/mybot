# -*- coding: utf-8 -*-
"""
__time__:2020/07/03 10:18
__author__:Coder-Sakura
church(教会),观察者(Monitor)与执行者(Executor)交互
重构cqp.py
"""

from flask import Flask, request,jsonify
import requests
import json
import random,os

from jiki import jk
from check_user import limit_manager
from anime import tra_anime,group_tra_anime
from image import tra_images,tra_images_group,cat2pixiv
from reply import reply_search ,reply_anime , reply_group ,reply_anime_group ,reply_image,reply_image_group
from error import error

# 配置文件
config = json.load(open("config.json",encoding='utf-8-sig'))
api_key = config['api_key']					# saucenao api_key
tarce_message = config['tarce_message']  	# 搜番
search_message = config['search_message']   # 搜图
setu_message = config['setu_message']  		# 来点x图命令
setu_path = config['setu_path']  			# x图地址,后续取消
count_setu = config['count_setu']  			# 统计x图
search_pid_info = config['search_pid_info'] # 查询pid
coolq_http_api_ip = config['coolq_http_api_ip']
coolq_http_api_port = config['coolq_http_api_port']

# url
# 酷Q http插件私聊推送url
siliao = "http://{}:{}/send_private_msg?".format(coolq_http_api_ip,coolq_http_api_port)
# 酷Q http插件群聊推送url
qunliao = "http://{}:{}/send_group_msg?".format(coolq_http_api_ip,coolq_http_api_port)
# saucenao
# search_image_url = "https://saucenao.com/search.php?db=999&output_type=2&\
# 					testmode=1&numres=16&api_key={}&&url={}"
search_image_url = "https://saucenao.com/search.php?db=999&output_type=2&\
					testmode=1&numres=16&"
# trace.moe
# trace_moe_url = 'https://trace.moe/api/search?url={}'
trace_moe_url = 'https://trace.moe/api/search?url'

# 变量
user_private_list = []  		 # 搜索番剧发送者QQ号的列表
user_group_list = [] 			 # 搜索番剧 群搜图 群号
search_acg_image_list = [] 		 # 搜索图片发送者QQ号的列表
search_acg_image_group_list = [] # 搜索图片 群搜图 群号


app = Flask(__name__)

@app.route('/',methods=['POST'])
def bot_function():
	cqp_push_data = request.get_data()  #获取机器人推送的内容
    eval_cqp_data = json.loads(cqp_push_data.decode('utf-8')) #转换推送内容为字典格式


	# church统一回复酷Q
	# executor只需要执行功能,包装并返回消息
	# monitor对消息进行过滤,包括是否放行到executor以及添加黑名单,接触限制等










if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run( port='5000')