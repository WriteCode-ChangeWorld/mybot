"""
目前是对搜图搜番进行限制
校验用户频率,并添加特殊用户以解除限制
只检查群聊,私聊不检查
"""
import os
import time

limit_text = "解除限制"
delete_text = "添加限制"
check_text = "查看名单"

class Limit:
	"""
	对于群聊使用机器人进行限制，每隔一段时间才能使用机器人功能
	比如,10秒为一个限制周期,第1秒时使用了搜番,则第11秒机器人才响应下一次请求
	"""
	def __init__(self):
	    # 初始化
	    self.data_path = os.path.join(os.getcwd(),"bot_data")
	    if os.path.exists(self.data_path) == False:
	    	os.mkdir("./bot_data")
	    self.nolimit_filename = "unlimit.txt"
	    self.txt_path = os.path.join(self.data_path,self.nolimit_filename)
	    self.master = 1508015265
	    # limit_info数据类型
	    # user(调用者qq),timestamp(时间戳),count(调用次数)
	    self.limit_info = {}

	def read(self):
		"""
		读取非限制名单
		"""
		try:
			with open(self.txt_path,"r",encoding="utf8") as f:
				a = f.readlines()
				a = [i.split("\n")[0] for i in a]
				a = list(set(a))
		except Exception as e:
			a = []
		return a

	def check_repeat(self,qq):
		"""
		检查记录文件中是否已有该账号
		:params qq: qq,str
		:return : 存在返回True,否则False
		"""
		res = self.read()
		return [True if qq in res else False][0]

	def change(self,eval_cqp_data):
		"""
		增加、删除、查看无限制用户
		私聊控制,群聊不处理
		命令格式: [解除限制/添加限制/查看名单][qq/]
		{"message_type":"private","user_id":1508015265,"message":"解除限制1508015265"}
		:parmas eval_cqp_data: 酷Q消息
		:return : 消息体
		"""
		# 私聊 主人
		if eval_cqp_data.get("message_type") == "private" and int(eval_cqp_data.get("user_id")) == self.master:
			msg = eval_cqp_data.get("message")
			if check_text in msg:
				res = self.read()
			elif limit_text in msg or delete_text in msg:
				res = self.add_delete(eval_cqp_data)
			# else:
			# 	# 指令错误,不存在的指令
			# 	search_results["message"] = "[{}]指令错误/不存在的指令".format(extra)
			# 	return search_results

			return res

	def add_delete(self,eval_cqp_data):
		"""
		限制解除&添加限制
		"""
		extra = eval_cqp_data.get("message")[:4]
		qq = eval_cqp_data.get("message")[4:]
		search_results = {
            "user_id": eval_cqp_data.get("user_id"),
		}

		# 验参,指令参数错误,非纯数字
		try:
			int(qq)
		except:
			search_results["message"] = "[{}]指令参数错误".format(qq)
			return search_results

		# 判断名单是否存在
		exist = self.check_repeat(qq)
		print(exist)
		# 解除限制
		if extra == limit_text:
			# 有
			if exist:
				search_results["message"] = "[{}]已在非限制名单中".format(qq)
				return search_results

			try:
				with open(self.txt_path,"a",encoding="utf8") as f:
					f.write("{}\n".format(qq))
				search_results["message"] = "[{}]写入成功".format(qq)

			except Exception as e:
				search_results["message"] = "[{}]写入失败\n错误原因:{}".format(qq,e)

			return search_results

		# 添加限制
		elif extra == delete_text:
			# 无
			if exist == False:
				search_results["message"] = "[{}]不在非限制名单中".format(qq)
				return search_results

			# 原始数据
			back_up_data = self.read()
			# 删除后的数据
			a = [i for i in back_up_data if i != qq]

			try:
				# 重写
				with open(self.txt_path,"w+",encoding="utf8") as f:
					for i in a:
						f.write("{}\n".format(i))
				search_results["message"] = "[{}]删除成功".format(qq)
			except Exception as e:
				# 写入失败回滚
				with open(self.txt_path,"w+",encoding="utf8") as f:
					for i in back_up_data:
						f.write("{}\n".format(i))
				search_results["message"] = "[{}]删除失败,已回滚\n错误原因:{}".format(qq,e)

			return search_results
		

	def trigger_limit(self,eval_cqp_data):
		"""
		群聊,在限制时间内使用机器人功能
		"""
		search_results = {
	        "group_id": eval_cqp_data['group_id'],
	        "message": "[CQ:at,qq=" + str(eval_cqp_data['user_id'])+"]" +'\n' +
	                   "请等待10秒后再调用,目前达到限制"
	    }



limit_manager = Limit()