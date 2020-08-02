import requests
#import cqp
import json
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from error import error

def tra_images(images_url,eval_cqp_data):
    try:
        response = requests.get(images_url,timeout=5)  # 获取saucenao的返回信息
    except Exception as e:
        res = error(eval_cqp_data)
        return res
    response.encoding = 'utf-8'  # 把saucenao的返回信息转码成utf-8
    result = response.json()  # 转换成json格式
    try:
        mini_image = result['results'][0]['header']['thumbnail']  # 缩略图
    except KeyError:
        mini_image = ""
    try:
        similarity = result['results'][0]['header']['similarity']  # 相似度
    except KeyError:
        similarity = ""
    try:
        jp_name = result['results'][0]['data']['jp_name']
    except KeyError:
        jp_name = ""
    try:
        pixiv_id = int(result['results'][0]['data']['pixiv_id'])
    except KeyError:
        pixiv_id = ""
    try:
        ext_urls = result['results'][0]['data']['ext_urls'][0]
        if "https://www.pixiv.net" in ext_urls:
            ext_urls = "https://www.pixiv.net/artworks/" + str(pixiv_id)
    except KeyError:
        ext_urls = ""
    try:
        member_name = result['results'][0]['data']['member_name']
    except KeyError:
        member_name = ""
    try:
        title = result['results'][0]['data']['title']
    except KeyError:
        title = ""
    if pixiv_id == "":
         get_cat = "暂无直链"
    else:
        try:
            get_cat = cat2pixiv(pixiv_id,extra=1,ecd=eval_cqp_data)
            if "网络出错" in get_cat:
                get_cat = "网络出错啦！"
        except:
            get_cat = "响应失败"
    search_results = {
        "user_id": eval_cqp_data['user_id'],
        "message": "[CQ:image,file=" + str(mini_image) + "]" + '\n' +  # 返回图片的CQ码给酷Q air版无法发送图片
                   "相似度: " + str(similarity) + '%' + '\n' +
                   "作者名称: " + str(member_name) + '\n' +
                   "图片名称: " + str(title) + '' + str(jp_name) + '\n' +
                   "P站id: " + str(pixiv_id) + '\n' +
                   "图片链接: " + '\n' + str(ext_urls) + "\n" +
                   str(get_cat)
        }
    return search_results

def cat2pixiv(pid,extra=None,ecd=None):
    # 获取pid的原图链接并反代
    u ="https://www.pixiv.net/ajax/illust/{}".format(str(pid))
    print(u)
    headers = {"accept-language":"zh-CN,zh;q=0.9"}
    try:
        res = json.loads(requests.get(u,headers=headers,timeout=10).text)
    except Exception as e:
        res = error(ecd)
        return res
    if res["error"] == True:
        return "id({})请求错误,错误原因{}".format(str(pid),res["message"])
    else:
        pageCount = res["body"]["pageCount"]
        illustType = res["body"]["illustType"]
        o = res["body"]["urls"]["original"]
        o = re.sub(r"pximg.net","pixiv.cat",o)
        if pageCount == 1:
            if illustType == 2:
                t = "动图"
            else:
                t = "单图"
        else:
                t = "多图"

        # 简略模式
        if extra == 1:
            r = "反代直链:" + '\n' + o
        # 待定
        elif extra == 2:
            r = "反代直链:" + '\n' + o
        # 自定义模式
        else:
            userName = res["body"]["userName"]
            userId = res["body"]["userId"]
            bookmarkCount = res["body"]["bookmarkCount"]
            viewCount = res["body"]["viewCount"]

            r = "作者:{}({})".format(userName,userId) + "\n" + \
                "这是一张{}".format(t) + "\n" +\
                "收藏数/浏览数:" + "\n" +\
                "{}/{}".format(bookmarkCount,viewCount) + "\n" +\
                "反代直链:" + "\n" + o

        return r
        
def tra_images_group(images_url,eval_cqp_data):
    try:
        response = requests.get(images_url,timeout=10)  # 获取saucenao的返回信息
    except Exception as e:
        print(e)
        res = error(eval_cqp_data)
        return res
    response.encoding = 'utf-8'  # 把saucenao的返回信息转码成utf-8
    result = response.json()  # 转换成json格式
    try:
        mini_image = result['results'][0]['header']['thumbnail']  # 缩略图
    except KeyError:
        mini_image = ""
    try:
        similarity = result['results'][0]['header']['similarity']  # 相似度
    except KeyError:
        similarity = ""
    try:
        jp_name = result['results'][0]['data']['jp_name']
    except KeyError:
        jp_name = ""
    try:
        pixiv_id = int(result['results'][0]['data']['pixiv_id'])
    except KeyError:
        pixiv_id = ""
    try:
        ext_urls = result['results'][0]['data']['ext_urls'][0]
        if "https://www.pixiv.net" in ext_urls:
            ext_urls = "https://www.pixiv.net/artworks/" + str(pixiv_id)
    except KeyError:
        ext_urls = ""
    try:
        member_name = result['results'][0]['data']['member_name']
    except KeyError:
        member_name = ""
    try:
        title = result['results'][0]['data']['title']
    except KeyError:
        title = ""         
    if pixiv_id == "":
         get_cat = "该id暂无直链"
    else:
        try:
            get_cat = cat2pixiv(pixiv_id,extra=1,ecd=eval_cqp_data)
            if "网络出错" in str(get_cat):
                get_cat = "网络出错啦！"
        except:
            get_cat = "响应失败"
    search_results = {
        "group_id": eval_cqp_data['group_id'],
        "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]" +
                   "[CQ:image,file=" + str(mini_image) + "]" + '\n' +  # 返回图片的CQ码给酷Q air版无法发送图片
                   "相似度: " + str(similarity) + '%' + '\n' +
                   "作者名称: " + str(member_name) + '\n' +
                   "图片名称: " + str(title) + '' + str(jp_name) + '\n' +
                   "P站id: " + str(pixiv_id) + '\n' +
                   "图片链接: " + '\n' + str(ext_urls.replace('[', '').replace(']', '').replace("'", '')) + '\n' +
                   str(get_cat)
    }
    return search_results
    