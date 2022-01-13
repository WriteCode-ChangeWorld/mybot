# -*- encoding: utf-8 -*-
'''
@File    :   executor.py
@Time    :   2022/01/13 15:44:25
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import sys
import time
# sys.path.append("Arsenal")

from dynamic_import import modules_dynamicLoad
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.msg_temp import MYBOT_ERR_CODE, EXECUTOR_TASK_STATUS_INFO, TASK_PROCESSOR_TEMP
from Arsenal.basic.thread_pool import ThreadPool, callback
from Arsenal.basic.task_processor import taskprocessor

class Executor:
	"""事件处理:插件轮询/热重启"""
	def __init__(self):
		# 为tool创建线程池pool
		self.init_thread_pool(8)

		# 启动定时任务检测线程
		# tool.pool.put(self.cycle_task_detect, (), callback)

		# 消息 - 插件解析器
		try:
			self.modules_dynamicLoad = modules_dynamicLoad
			self.module_dicts = self.modules_dynamicLoad.module_dicts
		except Exception as e:
			logger.warning(MYBOT_ERR_CODE["Generic_Exception_Info"].format(e))
			logger.warning("<dynamic_import>模块导入插件出现问题,请检查<dynamic_import>模块或插件后重试.")
			exit()
		
	# thread_pool func start
	def init_thread_pool(self,max_num=8):
		"""
		初始化线程池,暂不考虑reload情况
		< -- not reliable! -- >
		"""
		try:
			if hasattr(tool,"pool"):
				tool.pool.terminal = True
				logger.debug("3秒后重启线程池...")
				time.sleep(3)
		except Exception as e:
			logger.debug(MYBOT_ERR_CODE.format(e))
			return False
		finally:
			# 重置中断标志
			tool.pool = ThreadPool(max_num=max_num)
			tool.pool.terminal = False
			return True

	@logger.catch
	def cycle_task_detect(self,cycle=10):
		"""
		定时(<cycle>秒)监测任务并将任务放入线程池执行
		:params cycle: 监测周期,默认10秒检查一次
		"""
		# 通过terminal来强制中断
		while True:
			logger.debug(TASK_PROCESSOR_TEMP["TASK_START"])
			if tool.pool.terminal:
				logger.info(TASK_PROCESSOR_TEMP["TASK_BREAK_TERMINAL"])
				break

			tasks_list = taskprocessor.get_tasks()
			if not tasks_list:
				logger.debug(TASK_PROCESSOR_TEMP["TASK_NO_RECORD"])
			else:
				tasks_count_info = taskprocessor.task_count(tasks_list)
				[logger.info(EXECUTOR_TASK_STATUS_INFO["info"].format(i,j)) for i,j in tasks_count_info.items()]
				
				for task in tasks_list:
					tool.pool.put(taskprocessor.exec_tasks, (task,), callback)

			logger.debug(TASK_PROCESSOR_TEMP["TASK_END"].format(cycle))
			time.sleep(cycle)

	# thread_pool func end

	def reload_modules(self,
				pathname,
				recursive,
				class_start_with,
				reimport=True):
		"""
		加载插件目录插件
		:params reimport: True -> 重新导入
		:params pathname,recursive,class_start_with: 暂未用到
		"""
		return self.modules_dynamicLoad.import_modules(reimport=reimport)

	def parse(self,eval_cqp_data):
		"""
		使用消息 - 插件解析器解析消息,以匹配出结果
		"""
		msg = eval_cqp_data.get("message", "")
		if msg:
			try:
				self.modules_dynamicLoad.plugin_selector(eval_cqp_data)
			except Exception as e:
				logger.warning(MYBOT_ERR_CODE["Generic_Exception_Info"].format(e))
		else:
			status = tool.auto_report_err(msg)
			logger.info(f"<eval_cqp_data> not found <message> key - {eval_cqp_data}")
			logger.info(f"<status> - {status}")