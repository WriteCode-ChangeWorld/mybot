# -*- encoding: utf-8 -*-
'''
@File    :   level_manager.py
@Time    :   2021/11/30 15:18:46
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
from Arsenal.basic.bot_tool import tool


pass


class Monitor(object):
	"""用户/群组的权限查看/更新"""
	def __init__(self):
		# 默认权限
		self.general_user_level = int(tool.get_items('["Bot"]["level"]["user"]["general"]'))
		self.vip_user_level = int(tool.get_items('["Bot"]["level"]["user"]["vip"]'))
		self.admin_user_level = int(tool.get_items('["Bot"]["level"]["user"]["admin"]'))
		self.general_gruop_level = int(tool.get_items('["Bot"]["level"]["gruop"]["general"]'))
		self.vip_gruop_level = int(tool.get_items('["Bot"]["level"]["gruop"]["vip"]'))

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