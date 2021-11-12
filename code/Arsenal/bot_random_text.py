import os
import time
import random
from gtts import gTTS

from basic.plus_res_directory import pdr
from basic.BNConnect import baseRequest

"""
from future.Arsenal.basic.BNConnect import baseRequest
from bot_random_text import Bot_Random_Text
data = {"group_id":112233,"user_id":1508015265,"message_type":"group","message":"骂他[CQ:at,qq=3012797743]"}
Bot_Random_Text.service_func(data)
"""
class Random_Text:
	"""随机文字接口(舔狗日记,彩虹屁,祖安词典)
    非指向性时 --> 转语音
    指向性时 --> 不转语音
    """
	def __init__(self):
		self.bot_name = type(self).__name__
		self.workspace = pdr.get_plus_res(self.bot_name)
		# self.workspace = ""

		self.default_headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }
		self.temp_list = [
            {
                "keyword": ["彩虹屁","舔我","舔他"],
                "api": "https://chp.shadiao.app/api.php",
                "except_word": "正在舔的路上...",
                "specified_word": "舔他"
            },
            {
                "keyword": ["舔狗"],
                "api": "https://api.oick.cn/dog/api.php",
                "except_word": "舔狗炸了...",
                "specified_word": ""
            },
            {
                "keyword": ["祖安词典","骂我","骂他"],
                "api": "https://zuanbot.com/api.php?level=min&lang=zh_cn",
                "except_word": "正在骂的路上...",
                "specified_word": "骂他"
            },
            {
                "keyword": ["毒鸡汤","毒我","毒他"],
                "api": "https://api.oick.cn/dutang/api.php",
                "except_word": "正在煲汤的路上...",
                "specified_word": "毒他"
            }
        ]
        # 祖安词典/毒鸡汤白名单
		self.ugly_specified_words = ["骂他","毒他"]
		self.protection_list = [2076465138,3012797743]
		self.bot_list = [1359453526,3480538398]
		self.safe_text = {
            "protection_raw":"不可以骂尊贵的master们哦",
            "protection":"不可以骂尊贵的master们哦(＾＿－)~",
            "bot_raw":"想让我骂自己? 没门！",
            "bot":"想让我骂自己? 没门！",
        }
        
	def gtts_text2audio(self,word):
		"""
		使用Google TTS实现文字转语音
		:params word: 文字
		:return: audio音频路径
		"""
		tts = gTTS(
            text=word,
            lang='zh-CN',
            )
		# cq发送MP3需安装ffmpeg
		filename = "{}.mp3".format(int(time.time()))
		file_path = os.path.join(self.workspace,filename)
		tts.save(file_path)
		return file_path
    
	def match_temp(self,eval_cqp_data):
		"""
        根据消息匹配出接口并执行
        :parmas eval_cqp_data:
        :return: 返回组装好的数据包
        """
		msg = eval_cqp_data["message"]
		data = {
			"group_id":eval_cqp_data["group_id"],
			"message":""
		}

		for temp in self.temp_list:
		    # 循环遍历是否符合当前temp的关键词
			keyword = ""
			for _ in temp["keyword"]:
			    if _ in msg:
			        keyword = _
			        break
			else:
			    continue

			if keyword:
			    options = {"url":temp["api"], "headers":self.default_headers}
			    resp = baseRequest(options)
			    word = resp.text if resp else temp["except_word"]
			    print("bot_random_text match_temp | word:{}".format(word))
                # 指向性关键词触发->不进行文字转语音
			    if temp["specified_word"] != "" and\
			        temp["specified_word"] in msg and\
			        "[CQ:at,qq=" in msg:
			        user_id = msg.split("]")[0].split("[CQ:at,qq=")[-1]
			        # 白名单-master
			        if int(user_id) in self.protection_list and keyword in self.ugly_specified_words:
			            data["message"] = "[CQ:at,qq={}]\n{}".format(
			                eval_cqp_data["user_id"],self.safe_text["protection"])
			            return data
                    # 白名单-bot
			        elif int(user_id) in self.bot_list and keyword in self.ugly_specified_words:
			            data["message"] = "[CQ:at,qq={}]\n{}\n\n{}".format(
			                eval_cqp_data["user_id"],self.safe_text["bot"],word)
			            return data
			        else:
			            data["message"] = "[CQ:at,qq={}]\n{}".format(user_id,word)
			            return data

                # 文字转语音
			    if resp:
			        try:
			            result = self.gtts_text2audio(word)
			        except Exception as e:
			            print("bot_random_text match_temp Error:{} | word:{}".format(e,word))
			            data["message"] = "[CQ:at,qq={}]\n{}".format(eval_cqp_data["user_id"],word)
			            return data
			        else:
			            data["message"] = "[CQ:record,file=file:///{}]".format(result)
			            return data
        # 无匹配
		return None

	def service_func(self,eval_cqp_data):
		if eval_cqp_data.get('message_type','') == 'group' and\
            eval_cqp_data.get('message','') != '':
			match_text_data = self.match_temp(eval_cqp_data)
			return match_text_data


Bot_Random_Text = Random_Text()