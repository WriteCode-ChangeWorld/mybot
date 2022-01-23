# -*- encoding: utf-8 -*-
'''
@File    :   church.py
@Time    :   2021/05/08 18:21:37
@Author  :   Coder-Sakura
@Version :   1.1
@Desc    :   Mybot消息-生命周期事件处理
'''

# here put the import lib
import json
from flask import Flask, request, jsonify

from executor import Executor
from level_manager import Monitor
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.msg_temp import CHURCH_IDENTIFY_MSG
from Arsenal.basic.log_record import logger


class Church:
	"""Mybot消息-生命周期事件处理"""

	def __init__(self):
		pass

	def hand(self,eval_cqp_data):
		if not monitor_control.filter_msg(eval_cqp_data):
			executor_control.exec()


# ================= START ================

app = Flask(__name__)
church_control = Church()
executor_control = Executor()
monitor_control = Monitor()


@app.route('/',methods=['POST'])
@logger.catch
def event():
	cqp_push_data = request.get_data()
	eval_cqp_data = json.loads(cqp_push_data.decode('utf-8'))
	church_control.hand(eval_cqp_data)
	# 返回值?
	return ""

# =================  END  ================


if __name__ == '__main__':
	app.config['JSON_AS_ASCII'] = False
	app.run( port='5000')