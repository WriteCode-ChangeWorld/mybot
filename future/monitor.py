# coding=utf8
pass

pass


class Monitor(object):
	"""观察者,用户权限分配及调度"""
	def __init__(self):
		pass

	# TODO(Coder-Sakura): 2020/07/12 16:09 限制数据采集
	def eyes(self, eval_cqp_data):
		"""
		获取cq数据包中所需字段,重组新包
		:paramas eval_cqp_data: cq数据包
		:return :TBD
		"""
		pass

	# TODO(Coder-Sakura): 2020/07/12 17:11 数据重组
	def assembly(self, eval_cqp_data):
		"""
		以cq数据包重组新包
		:paramas eval_cqp_data: cq数据包
		:return : 新包
		"""
		pass