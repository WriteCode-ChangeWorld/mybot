# -*- encoding: utf-8 -*-
'''
@File    :   cqp_anime.py
@Time    :   2021/05/12 19:59:05
@Author  :   Coder-Sakura
@Version :   1.0
@Contact :   1508015265@qq.com
@Desc    :   None
'''

# here put the import lib
from json.decoder import JSONDecodeError
import os
import json
import time
import requests
from PIL import Image
from requests.api import options
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# cqp service
# from error import error
# from future.Arsenal.BNConnect import baseRequest
# from future.Arsenal.BNConnect import logger
# from future.Arsenal.url_985so import so985

# from future.Arsenal.url_dlj import LiDuanlian
# from future.Arsenal.url_suolink import SuoLink

# dev环境
from Arsenal.basic.plugin_res_directory import pdr
from Arsenal.basic.BNConnect import baseRequest
from Arsenal.basic.log_record import logger
# 2021年12月12日23:21:55
# from Arsenal.basic.url_985so import so985
# 导入上层temp模板
# from msg_printers import WHATANIME_MSG

class WhatAnime:
    """适配21.5.12更新后的WhatAnime接口
        1.获取用户发送图片
            -gif动图 --> anime_post_api
            -静态图 --> anime_search_api
        2.静态图anime_search_api出错则转换
    """
    def __init__(self):
        self.bot_name = type(self).__name__
        # 服务器端需要注意
        self.workspace = pdr.get_plus_res(self.bot_name)
        # self.workspace = ""
        self.gif_res = os.path.join(self.workspace,"gif")
        if not os.path.exists(self.gif_res):os.mkdir(self.gif_res)

        self.cache_res = os.path.join(self.workspace,"cache")
        if not os.path.exists(self.cache_res):os.mkdir(self.cache_res)

        # ===== headers start =====
        # 基础
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        }
        # WhatAnime番剧上传上传 分隔符
        self.boundary = "----WebKitFormBoundaryHmkx7DSnkXBVibSV"
        # WhatAnime番剧上传上传请求头 文件流
        self.anime_headers = {
            "content-type": "multipart/form-data; boundary=%s" % self.boundary,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest',
        }
        # anilist请求头
        self.anilist_headers = {
           "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "content-type":"application/json"
        }
        # ===== headers end =====

        # WhatAnime番剧上传接口 -- 本地文件
        self.anime_post_api = "https://api.trace.moe/search?info=advanced&cutBorders=1&anilistID="
        # WhatAnime番剧搜索接口 -- 网络图片链接
        self.anime_search_api = "https://api.trace.moe/search?url={}"
        
        # anilist查询番剧
        self.anilist_api = "https://trace.moe/anilist/"
        self.temp = "({}%) EP#{} {}\r\n" + \
                    "番剧名称: {}\r\n" + \
                    "中文名称: {}\r\n" + \
                    "[CQ:image,file=file:///{}]\r\n" +\
                    "预览链接: {}"
                    

        self.end_temp = "相似番剧推荐: {}\n[CQ:image,file=file:///{}]"

        # self.end_temp = "预览链接: {}\n\n" + \
        #                 "番剧推荐\n{}\n[CQ:image,file=file:///{}]"
        """
        self.temp = "({}%) EP#{} {}\n" + \
                    "AnilistId: {}\n" + \
                    "番剧名称: {}\n" + \
                    "中文名称: {}\n" + \
                    "[CQ:image,file={}]\n" + \
                    "预览链接: {}\n\n" + \
                    "番剧推荐\n{}\n[CQ:image,file={}]"
        """


    def anime_gif(self,img_url):
        """
        判断img_url的文件类型
            gif进行下载
            其他类型图片返回img_url
        :params img_url: 图片网络连接
        :return: False/gif本地路径/img_url

        """
        try:
            options = {"url":img_url,"headers":self.headers}
            resp = baseRequest(options)
            # resp = requests.get(img_url, headers=headers)
            file_type = resp.headers["Content-Type"].split("/")[-1]
        except Exception as e:
            logger.info("anime gif: Exception: {}".format(e))
            logger.info("anime gif: Error Url: {}".format(img_url))
            return False
        else:
            # gif则下载图片到本地,并返回文件名称
            if file_type == "gif":
                filename = "{}.{}".format(int(time.time()), file_type)
                gif_path = os.path.join(self.gif_res,filename)
                with open(gif_path, "wb") as f:
                    f.write(resp.content)
                return gif_path
            else:
                return img_url

    def force_conver(self,gif_path):
        """
        强转gif为png --> 取第一帧
        :params new_filename: 需要转换的gif路径
        :return: png路径
        """
        filename = os.path.split(gif_path)[-1]
        new_filename = filename.replace("gif", "png")
        new_gif_path = os.path.join(os.path.split(gif_path)[0], new_filename)
        img = Image.open(gif_path)
        img.convert('RGB')
        img.save(new_gif_path)
        img.close()
        # # 删除原来的gif
        os.remove(gif_path)
        return new_gif_path

    def encode_multipart(self,params):
        # 用于POST boundary文件上传
        # boundary = "----xxxx"
        # headers = {"xx":"xxx; boundary=------xxxx}
        data = []
        for k, v in params.items():
            data.append("--%s" % self.boundary)
            if hasattr(v, "read"):
                content = v.read()
                decoded_content = content.decode('ISO-8859-1')
                data.append(
                    'Content-Disposition: form-data; name="image"; filename="blob"')
                data.append('Content-Type: image/jpg\r\n')
                data.append(decoded_content)
            else:
                data.append(
                    'Content-Disposition: form-data; name="%s"\r\n' % k)
                data.append(v if isinstance(v, str) else v.decode('utf-8'))
        data.append("--%s--\r\n" % self.boundary)
        return '\r\n'.join(data)

    def anime_search_file(self,data):
        """
        POTS传参,以form-data和boundary形式上传文件流到WhatAnime并返回json
        :params data: POST数据
        # :params eval_cqp_data: 酷Q数据包
        :return: json/含错误信息的json
        """
        try:
            resp = requests.post(
                self.anime_post_api, 
                headers=self.anime_headers, 
                data=data, 
                verify=False
            )
        except Exception as e:
            # res = error(eval_cqp_data)
            # return res
            logger.info(e)
            logger.info(data)
            return {"error_msg": "WhatAnime返回数据有误!请重试"}
        else:
            # return resp
            resp.encoding = 'utf-8'
            try:
                json_data = json.loads(resp.text)
            except json.decoder.JSONDecodeError as e:
                logger.info(e)
                logger.info(resp.text)
                return {"error_msg": "网络出错惹!请重试"}

            if json_data["error"] == "Failed to process image":
                return {"error_msg": "WhatAnime无法处理图像!请重试"}
            elif json_data.get("result", "") == "":
                return {"error_msg": "网络出错惹(json)!请重试"}
            else:
                return json_data

    def anime_search_network(self,img_url):
        u = self.anime_search_api.format(img_url)
        options = {
            "url": u,
            "headers": self.headers,
            "timeout":10
        }
        resp = baseRequest(options=options)
        try:
            json_data = json.loads(resp.text)
        except Exception as e:
            logger.info("JSONDecodeError url: ".format(u))
            return {"error_msg": "网络出错惹(json)!请重试"}
        else:
            return json_data

    def get_anilist_info(self,anime_id):
        """
        根据WhatAnime的anime_id在anilist中查找番剧信息
        :parmas anime_id: 番剧id,由WhatAnime返回
        :return: json/None
        """
        payload = {
            "query": """query ($ids: [Int]) {
                Page(page: 1, perPage: 1) {
                    media(id_in: $ids, type: ANIME) {
                        id
                        title {
                            native
                            romaji
                            english
                            }
                        type
                        format
                        status
                        startDate {
                            year
                            month
                            day
                            }
                        endDate {
                            year
                            month
                            day
                            }
                        season
                        episodes
                        duration
                        source
                        coverImage {
                            large
                            medium
                            }
                        bannerImage
                        genres
                        synonyms
                        isAdult
                        recommendations(perPage: 5, sort: [RATING_DESC, ID]) {
                        pageInfo {
                          total
                        }
                        nodes {
                          id
                          rating
                          userRating
                          mediaRecommendation {
                            id
                            title {
                                native
                                romaji
                                english
                            }
                            format
                            type
                            status(version: 2)
                            bannerImage
                            coverImage {
                              large
                            }
                          }
                          user {
                            id
                            name
                            avatar {
                              large
                            }
                          }
                        }
                      }
                        externalLinks {
                            id
                            url
                            site
                            }
                        siteUrl
                        }
                    }
                }""",
            "variables": {"ids": [str(anime_id)]}
        }
        options = {"url":"https://trace.moe/anilist/","headers":self.anilist_headers,"timeout":10}
        resp = baseRequest(options=options, method="POST", data=json.dumps(payload))
        if not resp:
            logger.info("resp is None|animeid: {}".format(anime_id))
            return None
        
        anime_result = json.loads(resp.text)["data"]["Page"]["media"]
        return anime_result

    def download_pic(self,cache_url):
        new_cover_path = os.path.join(self.cache_res,"{}.jpg".format(time.time()))
        with open(new_cover_path,"wb") as f:
            f.write(baseRequest({"url":cache_url,"headers":self.headers,"timeout":10}).content)

        # from PIL import Image
        # img = Image.open(new_cover_path)
        # img.save(new_cover_path, quality=95)
        return new_cover_path

    # 群聊 搜索番剧截图
    def group_tra_anime(self,trace_url,eval_cqp_data):
        """暂时都使用POST上传,先迎合1.0的逻辑,再重构出一个2.0的插件
        CQ直接将消息传入该func
        1.开始搜番 连续搜图
        2.搜番 单张
        
        :params trace_url: img_url,图片链接
        :params eval_cqp_data: 酷Q数据包
        :return: 待定
        """
        temp = 'https://trace.moe/api/search?url='
        img_url = trace_url.replace(temp, "")
        logger.info("搜番图片: {}".format(img_url))
        # 判断是否为gif
        decision_result = self.anime_gif(img_url)
        if decision_result:
            # 非gif
            if decision_result == img_url:
                logger.info("img | not gif")
                result = self.anime_search_network(img_url)
            # gif
            else:
                logger.info("img | gif")
                new_gif_path = self.force_conver(decision_result)
                with open(new_gif_path, "rb") as f:
                    params = {
                        "image": f,
                        "filter": "",
                        "trial": "0",
                    }
                    data = self.encode_multipart(params)
                    result = self.anime_search_file(data)
        else:
            # 并入msg_printer
            search_results = {
                "group_id": eval_cqp_data.get('group_id',""),
                "message": "网络爆炸惹~请重试!"
            }
            return search_results,""

        # 排除WhatAnime中的异常状况
        if result:
            if result.get("error_msg","") != "":
                search_results = {
                    "group_id": eval_cqp_data.get('group_id',""),
                    "message": "网络爆炸惹~请重试!"
                }
                logger.info("group_tra_anime | Have Error Msg")
                logger.info("error_msg: {}".format(result.get("error_msg","")))
                return search_results,""
            # anime_search_network | Failed to fetch image
            elif result.get("error","") != "":
                search_results = {
                    "group_id": eval_cqp_data.get('group_id',""),
                    "message": "Failed to fetch image~请重试!"
                }
                logger.info("group_tra_anime | Failed to fetch image")
                logger.info("error: {} | url: {}".format(result.get("error",""),trace_url))
                return search_results,""
        else:
            search_results = {
                "group_id": eval_cqp_data.get('group_id',""),
                "message": "网络爆炸惹~请重试!"
            }
            logger.info("group_tra_anime | result is None")
            logger.info("result: {}".format(result))
            return search_results,""

        # 向anilist发送请求
        whatanime_result = result["result"][0]
        anime_id = whatanime_result["anilist"]
        anime_result = self.get_anilist_info(anime_id)
        anime_info = anime_result[0]
        logger.info("result: {}".format(result))
        logger.info("anime_result: {}".format(anime_result))


        # === 格式化并返回 ===
        # Anilist_id
        anilist_id = whatanime_result.get("anilist","无")
        # 相似度
        similarity = whatanime_result.get("similarity", "")
        similarity = round(similarity*100, 2) if similarity != "" else ""
        # EP
        episode = whatanime_result.get("episode", "")
        # 时间点
        st = whatanime_result.get("from", "")
        time_text = "{}分{}秒".format(int(st / 60), int(st % 60)) if st != "" else ""
        # 视频预览链接
        try:
            preview_url = whatanime_result["video"]
            # preview_url = so985().get_slink(preview_url)
            preview_url = preview_url.replace("http://","")
            logger.info("short url: {}".format(preview_url))
        except Exception as e:
            preview_url = "链接获取失败"
            logger.info("short url error: {}".format(e))
        
        
        # 动画名称
        native = anime_info["title"].get("native","")
        native = native if native else "无"
        chinese = anime_info["title"].get("chinese","")
        chinese = chinese if chinese else "无"
        # 番剧封面
        cover = anime_info["coverImage"].get("medium","")
        # cover = anime_info["coverImage"].get("large","")
        # 番剧推荐(第一部)
        if anime_info["recommendations"]["nodes"] == []:
            recommen_name = ""
            recommen_cover = ""
        else:
            recommen_anime = anime_info["recommendations"]["nodes"][0]
            recommen_name = recommen_anime["mediaRecommendation"]["title"]["native"]
            recommen_cover = recommen_anime["mediaRecommendation"]["coverImage"]["large"]

        # search_results = {
        #         "group_id": eval_cqp_data['group_id'],
        #         "message": self.temp.format(
        #             similarity,episode,time_text,
        #             anilist_id,native,chinese,
        #             cover,preview_url,recommen_name,recommen_cover
        #         )
        #     }

        search_results = {
                "group_id": eval_cqp_data.get('group_id',""),
                "message": self.temp.format(
                    str(similarity),str(episode),str(time_text),
                    str(native),str(chinese),self.download_pic(str(cover)),str(preview_url)
                    # str(preview_url),str(recommen_name),self.download_pic(str(recommen_cover))
                )
            }

        end_results = {
                "group_id": eval_cqp_data.get('group_id',""),
                "message": ""
            }
        if recommen_name == "" and recommen_cover == "":
            search_results["message"] += "\n\n暂无相似番剧推荐"
            end_results = ""
        else:
            end_results["message"] = self.end_temp.format(
                    str(recommen_name),self.download_pic(str(recommen_cover))
                )

        logger.info("search_results: {}".format(search_results))
        logger.info("end_results: {}".format(end_results))
        return search_results,end_results
        # return search_results

Bot_WhatAnime = WhatAnime()