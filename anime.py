# import cqp
import requests
import json

from error import error


def tra_anime(trace_url,eval_cqp_data):   #私聊 搜索番剧截图
    try:
        response = requests.get(trace_url,timeout=10)  # 获取trace.moe的返回信息
    except Exception as e:
        res = error(eval_cqp_data)
        return res
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    result = json.loads(response.text)
    # result = response.json()  # 转换成json格式
    print(result)
    print(response.url)
    try:
        name = result["docs"][0]["title_chinese"]  # 切片番剧名称
        similarity = result["docs"][0]["similarity"]  # 切片相似度
        try:
            decimal = "." + str(similarity * 100).split('.')[1][:2]  # 切片小数点后的内容 如果为空则不返回
        except IndexError:
            decimal = ""

        time = result["docs"][0]["at"]  # 切片时间
        episode = result["docs"][0]["episode"]  # 切片集数
        search_results = {
            "user_id": eval_cqp_data['user_id'],
            "message": "番剧名称：" + name + " 第" + str(episode) + "集" + '\n' +
                        "相似度：" + str(similarity * 100).split('.')[0] + decimal + "%" + '\n' +
                        "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[0] + '秒'
        }
        return search_results
    except Exception as e:
        search_results = {
            "user_id": eval_cqp_data['user_id'],
            "message": "出错了..." + "\n" + 
                       "错误原因：" + str(e) + "\n" + str(response)
        }
        return search_results

def group_tra_anime(trace_url,eval_cqp_data):   #群聊 搜索番剧截图
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
    try:
        response = requests.get(trace_url,timeout=10)  # 获取trace.moe的返回信息
    except Exception as e:
        print(trace_url)
        res = error(eval_cqp_data)
        return res
    response.encoding = 'utf-8'  # 把trace.moe的返回信息转码成utf-8
    # result = response.json()  # 转换成json格式
    try:
        result = json.loads(response.text)
        animename = result["docs"][0]["title_chinese"]  # 切片番剧名称
        similarity = result["docs"][0]["similarity"]  # 切片相似度
        try:
            decimal = "." + str(similarity * 100).split('.')[1][:2]  # 切片小数点后的内容 如果为空则不返回
        except IndexError:
            decimal = ""
        time = result["docs"][0]["at"]  # 切片时间
        episode = result["docs"][0]["episode"]  # 切片集数
        search_results = {
            "group_id": eval_cqp_data['group_id'],
            "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id'])+"]" +'\n' +
                       "番剧名称：" + animename + " 第" + str(episode) + "集" + '\n' +
                       "相似度：" + str(similarity * 100).split('.')[0] + decimal + "%" + '\n' +
                       "时间：" + str(time / 60).split('.')[0] + '分' + str(time % 60).split('.')[0] + '秒'
        }
        return search_results
    except Exception as e:
        search_results = {
            "group_id": eval_cqp_data['group_id'],
            "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id'])+"]" +'\n' +
                       "出错了..." + "\n" + 
                       "错误原因：" + str(e) + "\n" + str(response)
        }
        return search_results