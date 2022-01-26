from Arsenal.coding.error import error
import requests
#import cqp
import json
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sarch_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Cookie': '__cfduid=da7d9e4e44293fcec7a0cf6367dae02521615470919; token=60520d109310b; user=35027; auth=d58aa9c3a26cfe55c65224d17e16c56bb5367ded'
}


def tra_images(images_url, eval_cqp_data):
    try:
        # print("images_url",images_url)
        response = requests.get(
            images_url, headers=sarch_headers, timeout=60)  # 获取saucenao的返回信息
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

    if pixiv_id == "":
        get_cat = "暂无直链"
    else:
        try:
            get_cat = cat2pixiv(pixiv_id, extra=1, ecd=eval_cqp_data)
            if "网络出错" in get_cat:
                get_cat = "网络出错啦!"
        except:
            get_cat = "响应失败"
    search_results = {
        "user_id": eval_cqp_data['user_id'],
        # 返回图片的CQ码给酷Q air版无法发送图片
        "message": "[CQ:image,file=" + str(mini_image) + "]" + '\n' +
                   "相似度: " + str(similarity) + '%' + '\n' +
                   "作者名称: " + str(member_name) + '\n' +
                   "P站id: " + str(pixiv_id) + '\n' +
                   "图片链接: " + '\n' + str(ext_urls) + "\n" +
                   str(get_cat)
    }
    return search_results


def cat2pixiv(pid, extra=None, ecd=None):
    # 获取pid的原图链接并反代
    u = "https://www.pixiv.net/ajax/illust/{}".format(str(pid))
    print(u)
    headers = {"accept-language": "zh-CN,zh;q=0.9"}
    try:
        res = json.loads(requests.get(u, headers=headers, timeout=10).text)
    except Exception as e:
        res = error(ecd)
        return res
    if res["error"] == True:
        return "id({})请求错误,错误原因{}".format(str(pid), res["message"])
    else:
        pageCount = res["body"]["pageCount"]
        illustType = res["body"]["illustType"]
        original = res["body"]["urls"]["original"]
        file_type = original.split(".")[-1]

        if pageCount > 1:
            o = "https://pixiv.cat/{}-{}.{}".format(pid, "1", file_type)
            # o = "https://pixiv.cat/ {}-{}.{}".format(pid,"1",file_type)
        else:
            o = "https://pixiv.cat/{}.{}".format(pid, file_type)
            # o = "https://pixiv.cat/ {}.{}".format(pid,file_type)

        # o = res["body"]["urls"]["original"]
        # o = re.sub(r"pximg.net","pixiv.cat",o)
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
            return res
            # r = "反代直链:" + '\n' + o
        # 自定义模式
        else:
            userName = res["body"]["userName"]
            userId = res["body"]["userId"]
            bookmarkCount = res["body"]["bookmarkCount"]
            viewCount = res["body"]["viewCount"]

            r = "作者:{}|{}".format(userName, userId) + "\n" + \
                "{}|收藏:{}".format(t, bookmarkCount) + "\n" +\
                "反代直链:" + "\n" + o

        return r


def tra_images_group(images_url, eval_cqp_data):
    try:
        print("images_url", images_url)
        response = requests.get(
            images_url, headers=sarch_headers, timeout=60)  # 获取saucenao的返回信息
    except Exception as e:
        print(e)
        res = error(eval_cqp_data)
        return res
    response.encoding = 'utf-8'  # 把saucenao的返回信息转码成utf-8

    # saucenao 525 服务器错误
    if response.status_code != 200:
        search_results = {
            "group_id": eval_cqp_data['group_id'],
            "message": "[CQ:at,qq={}]\n".format(str(eval_cqp_data['user_id'])) +
                       "saucenao内部错误:\n{}".format(response)
        }
        return search_results

    result = response.json()  # 转换成json格式
    # print(result)

    # 目前碰到的情况是空间外链导致无法引用
    # if result.get("result","") == "":
    # TestUrl http://gchat.qpic.cn/gchatpic_new/3021321332113231213211279722743/1072951237655-285798123387-A5FE7DE5AAA4670ACDEA6B5EAE71B123C22/0?term=2pi
    if result.get("results", "") == "" or result.get("results", "") == None:
        err_msg = 'Specified file no longer exists on the remote server!'
        # 确认为空间外链导致的无法引用
        if result["header"]["status"] == -3 and result["header"].get("message", "") == err_msg:
            print("image_group_err")
            search_results = {
                "group_id": eval_cqp_data['group_id'],
                "message": "[CQ:at,qq={}]\n".format(str(eval_cqp_data['user_id'])) +
                           # "[CQ:image,file={}]\n".format("      ") + # 返回图片的CQ码给酷Q air版无法发送图片
                           "由于图片为空间外链或其他原因导致Saucenao无法引用到,故引发该错误." + "\n" +
                           "请重新截图裁剪,再次搜图~"
            }
            print(search_results)
            return search_results

    # print(len(result.get("results",[])))
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
            ext_urls = "https://www.pixiv.net/i/" + str(pixiv_id)
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
            get_cat = cat2pixiv(pixiv_id, extra=1, ecd=eval_cqp_data)
            if "网络出错" in str(get_cat):
                get_cat = "网络出错啦！"
        except:
            get_cat = "响应失败"

    search_results = {
        "group_id": eval_cqp_data['group_id'],
        "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id']) + "]" +
                   # 返回图片的CQ码给酷Q air版无法发送图片
                   "[CQ:image,file=" + str(mini_image) + "]" + '\n' +
                   "相似度: " + str(similarity) + '%'
    }
   # 作者名称
   # "作者:" + str(member_name) + '\n' +
   # 图片名称
   # "" + str(title) + '' + str(jp_name) + '】\n' +
   # "P站id: " + str(pixiv_id) + '\n' +
   # "图片链接: " + '\n' + str(ext_urls.replace('[', '').replace(']', '').replace("'", '')) + '\n' +
   # str(get_cat)}

    if str(member_name) != "":
        search_results["message"] += "\n作者:" + str(member_name)  # + '\n'

    # if str(title) != "":
    #     search_results["message"] += "图片名称:" + str(title) + '\n'

    if str(pixiv_id) != "":
        search_results["message"] += "\npid:" + str(pixiv_id)  # + '\n'

    if str(jp_name) != "":
        search_results["message"] += "\n本子名称:" + str(jp_name)  # + '\n'

    if str(ext_urls) != "":
        search_results["message"] += "\n图片链接:\n" + \
            str(ext_urls.replace('[', '').replace(']', '').replace("'", ''))

    if str(get_cat) != "该id暂无直链":
        search_results["message"] += "\n"
        search_results["message"] += str(get_cat)

    print(search_results)
    return search_results
