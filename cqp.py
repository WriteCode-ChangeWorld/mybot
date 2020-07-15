# -*- coding: utf-8 -*-
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

config = json.load(open("config.json",encoding='utf-8-sig'))
api_key = config['api_key']
tarce_message = config['tarce_message']  # 搜番剧的命令
search_message = config['search_message']  # 搜图片的命令
setu_message = config['setu_message']  # 来点涩图命令
setu_path = config['setu_path']  # 涩图地址
count_setu = config['count_setu']  # 统计涩图数量的命令
search_pid_info = config['search_pid_info'] # 查询pid信息
coolq_http_api_ip = config['coolq_http_api_ip']
coolq_http_api_port = config['coolq_http_api_port']

app = Flask(__name__)
siliao = 'http://'+ coolq_http_api_ip + ':'+ coolq_http_api_port +'/send_private_msg?' #酷Q http插件私聊推送url
qunliao = 'http://'+ coolq_http_api_ip + ':'+ coolq_http_api_port +'/send_group_msg?' #酷Q http插件群聊推送url
trace_moe_url = 'https://trace.moe/api/search?url='  #trace.moe的api地址
search_image_url = 'https://saucenao.com/search.php?db=999&output_type=2&testmode=1&numres=16&' #saucenao的API地址
api_key = api_key #saucenao的api key
user_private_list = []  #暂存 搜索番剧发送者QQ号的列表
user_group_list = [] #暂存搜索番剧 群搜图 群号
search_acg_image_list = [] #暂存 搜索图片发送者QQ号的列表
search_acg_image_group_list = []#暂存 搜索图片 群搜图的群号
user_name_txt = "user.txt"


@app.route('/',methods=['POST'])
def tarce_amine():
    cqp_push_data = request.get_data()  #获取机器人推送的内容
    eval_cqp_data = json.loads(cqp_push_data.decode('utf-8')) #转换推送内容为字典格式
    private_number = 0
    group_number = 0
    search_acg_number = 0
    search_acg_group_number = 0

    from future.executor import Executor
    executor = Executor()
    a = executor.task_parse(eval_cqp_data)
    requests.get(url=qunliao, params=a)

#####################################私聊 只发文字 后发图 识别番剧####################################################
    if eval_cqp_data['message_type'] == 'private':
        if eval_cqp_data['message'] == tarce_message:  # 私聊搜索番剧截图  replace 删除换行符跟回车
            if eval_cqp_data['user_id'] not in user_private_list:
                user_private_list.append(eval_cqp_data['user_id'])
                requests.get(url=siliao, params=reply_search(eval_cqp_data))

        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in user_private_list:
                if eval_cqp_data['user_id'] == c:
                    message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
                    trace_url = trace_moe_url + message_url
                    print(trace_url)
                    requests.get(url=siliao , params=reply_anime(eval_cqp_data))
                    requests.get(url=siliao, params=tra_anime(trace_url,eval_cqp_data))
                    user_private_list.pop(private_number)
                    break
                private_number = private_number + 1
#####################################私聊 只发文字 后发图 识别番剧####################################################
#
# #####################################私聊 发文字带图片###################################################################
        elif tarce_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]   #切片内容 把图片的url切片出来
            trace_url=trace_moe_url + message_url
            requests.get(url = siliao,params=reply_anime(eval_cqp_data))
            requests.get(url = siliao,params=tra_anime(trace_url,eval_cqp_data))
# #####################################私聊 发文字带图片###################################################################

#####################################群聊 只发文字 后发图 识别番剧####################################################
    if eval_cqp_data['message_type'] == 'group':
        if eval_cqp_data['message'] == tarce_message:  # 私聊搜索番剧截图  replace 删除换行符跟回车
            if eval_cqp_data['user_id'] not in user_group_list:
                user_group_list.append(eval_cqp_data['user_id'])
                requests.get(url=qunliao, params=reply_group(eval_cqp_data))

        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in user_group_list:
                if eval_cqp_data['user_id'] == c:
                    message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[
                        1]  # 切片内容 把图片的url切片出来
                    trace_url = trace_moe_url + message_url
                    requests.get(url=qunliao, params=reply_anime_group(eval_cqp_data)) #返回"番剧识别中"
                    requests.get(url=qunliao, params=group_tra_anime(trace_url,eval_cqp_data))  #返回结果
                    user_group_list.pop(group_number)
                    break
                group_number = group_number + 1
#####################################群聊 只发文字 后发图 识别番剧####################################################
#
# #####################################群聊 发文字带图片 识别番剧###################################################################
        elif tarce_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            message_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
            trace_url = trace_moe_url + message_url
            kaifuku = {
                "group_id": eval_cqp_data['group_id'],
                "message": "番剧截图识别中 请稍后......"
            }
            requests.get(url=qunliao, params=kaifuku)
            requests.get(url=qunliao, params=group_tra_anime(trace_url,eval_cqp_data))
# #####################################群聊 发文字带图片 识别番剧###################################################################
# 
# 
# 
# 
#                                               ↓识别图片↓                                                            #
######################################################################################################################
#####################################私聊 只发文字 后发图 搜索图片######################################################
    if eval_cqp_data['message_type'] == 'private':

        if eval_cqp_data['message'] == count_setu:
            res = str(len(os.listdir(setu_path)))
            search_results = {
                "user_id": eval_cqp_data['user_id'],
                "message": "当前涩图库有" + res + "张涩图~"
            }
            requests.get(url=siliao, params=search_results)

        if eval_cqp_data['message'] == setu_message:
            name = random.choice(os.listdir(setu_path))
            if "-" in name:
                n = name.index("-") # 横杠索引
                m = name.index(".") # 点索引
                d = name[n+1:m]
                name = name[:n+1] + str(int(d)+1) + name[m:]

            res = "https://pixiv.cat/" + name
            search_results = {
                "user_id": eval_cqp_data['user_id'],
                "message": res
            }
            requests.get(url=siliao, params=search_results)

        if eval_cqp_data['message'] == search_message:
            if eval_cqp_data['user_id'] not in search_acg_image_list: #如果发送命令的QQ号不存在user_private_list表当中
                search_acg_image_list.append(eval_cqp_data['user_id']) #将QQ号暂存至user_private_list表当中
                requests.get(url=siliao, params=reply_search(eval_cqp_data))

        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in search_acg_image_list:
                if eval_cqp_data['user_id'] == c:
                    trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
                    search_image = search_image_url + 'api_key=' + api_key + '&url=' +trace_image_url
                    requests.get(url=siliao , params=reply_image(eval_cqp_data))
                    requests.get(url=siliao, params=tra_images(search_image,eval_cqp_data))
                    search_acg_image_list.pop(search_acg_number)
                    break
                search_acg_number = search_acg_number + 1
#####################################私聊 只发文字 后发图 搜索图片######################################################
#
######################################私聊 发文字带图片 搜索图片###############################################################
        elif search_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
            search_image = search_image_url + 'api_key=' + api_key + '&url=' + trace_image_url
            requests.get(url=siliao, params=reply_image(eval_cqp_data))
            requests.get(url=siliao, params=tra_images(search_image,eval_cqp_data))

#####################################群聊 只发文字 后发图 搜索图片#############################
    if eval_cqp_data['message_type'] == 'group':
        # jiki
        if "jiki" in eval_cqp_data["message"] and \
          "jiki " == eval_cqp_data["message"][:5] and \
          eval_cqp_data["message"].count("jiki") == 1 :
            jk_res = jk.check(eval_cqp_data)
            search_results = {
                "group_id": eval_cqp_data['group_id'],
                "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]" + "\n"
                            + "jiki到【{}】".format(jk_res["title"]) + "\n"
                            + "释义:" + jk_res["res"] + "\n"
                            + jk_res["complete"]
            }
            requests.get(url=qunliao, params=search_results)

        # pid
        if eval_cqp_data['message'][:6] == search_pid_info:
            try:
                # 验证是否能转为int类型
                # pid
                w = int(eval_cqp_data['message'].split(":")[-1].split("-")[0])
                # 额外参数
            except:
                res = error(eval_cqp_data,m=1)
                requests.get(url=qunliao, params=res)
            else:
                try:
                    extra = int(eval_cqp_data['message'].split(":")[-1].split("-")[-1])
                except:
                    extra = None
                if extra not in [1,]:
                    extra = None
                print(w,extra,type(extra))
                info = cat2pixiv(w,extra,ecd=eval_cqp_data)
                if "网络出错" in str(info):
                    info = "网络出错啦！"
                search_results = {
                    "group_id": eval_cqp_data['group_id'],
                    "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]" + "\n"
                                + "pid: {}".format(w) + "\n"
                                + info
                }
                requests.get(url=qunliao, params=search_results)
        
        # 有多少
        if eval_cqp_data['message'] == count_setu:
            res = str(len(os.listdir(setu_path)))
            search_results = {
                "group_id": eval_cqp_data['group_id'],
                "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]"
                            + "\n"  
                            + "当前涩图库有" + res + "张涩图~"
            }
            requests.get(url=qunliao, params=search_results)

        # 命中来点x图命令:
        if eval_cqp_data['message'] == setu_message:
            name = random.choice(os.listdir(setu_path))
            if "-" in name:
                n = name.index("-") # 横杠索引
                m = name.index(".") # 点索引
                d = name[n+1:m]
                name = name[:n+1] + str(int(d)+1) + name[m:]

            res = "https://pixiv.cat/" + name
            search_results = {
                "group_id": eval_cqp_data['group_id'],
                "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]"
                            + "\n" +res
            }
            requests.get(url=qunliao, params=search_results)

        # 私聊搜索番剧截图  replace 删除换行符跟回车
        if eval_cqp_data['message'] == search_message:  
            if eval_cqp_data['user_id'] not in search_acg_image_group_list :
                search_acg_image_group_list.append(eval_cqp_data['user_id'])
                requests.get(url=qunliao, params=reply_group(eval_cqp_data))

        elif eval_cqp_data['message'].split(',')[0] == '[CQ:image':
            for c in search_acg_image_group_list:
                if eval_cqp_data['user_id'] == c:
                    trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[
                        1]  # 切片内容 把图片的url切片出来
                    search_image = search_image_url + 'api_key=' + api_key + '&url=' + trace_image_url
                    requests.get(url=qunliao, params=reply_image_group(eval_cqp_data))
                    requests.get(url=qunliao, params=tra_images_group(search_image,eval_cqp_data))
                    search_acg_image_group_list.pop(search_acg_group_number)
                    break
                    search_acg_group_number = search_acg_group_number + 1
#####################################群聊 只发文字 后发图 搜索图片#############################
#
#####################################群聊 发文字带图片 搜索图片###################################
        elif  search_message in eval_cqp_data['message'] and "[CQ:image" in eval_cqp_data['message']:
            print(eval_cqp_data['message'])
            trace_image_url = eval_cqp_data['message'].split('[')[1].split(']')[0].split('url=')[1]  # 切片内容 把图片的url切片出来
            search_image = search_image_url + 'api_key=' + api_key + '&url=' + trace_image_url
            requests.get(url=qunliao, params=reply_image_group(eval_cqp_data))
            requests.get(url=qunliao, params=tra_images_group(search_image,eval_cqp_data))
    return (cqp_push_data)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run( port='5000')
    
