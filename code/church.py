# -*- encoding: utf-8 -*-
'''
@File    :   church.py
@Time    :   2021/05/08 18:21:37
@Author  :   Coder-Sakura
@Version :   1.1
@Desc    :   Mybot消息-生命周期事件处理
'''

# here put the import lib
# import copy
import json
from flask import Flask, request, jsonify

from executor import Executor
from level_manager import Monitor
from Arsenal.basic.user_data import UserData
from Arsenal.basic.log_record import logger


class Church:
	"""Mybot消息-生命周期事件处理"""

	def hand(self,eval_cqp_data):
		with UserData(eval_cqp_data) as mybot_data:
			if not monitor_control.filter_msg(mybot_data):
				# mybot_data = copy.deepcopy(tool.mybot_data)
				executor_control.exec(mybot_data)



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
	return ""

# =================  END  ================


if __name__ == '__main__':
	app.config['JSON_AS_ASCII'] = False
	app.run( port='5000')