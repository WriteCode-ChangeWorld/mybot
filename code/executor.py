# -*- encoding: utf-8 -*-
'''
@File    :   executor.py
@Time    :   2022/01/13 15:44:25
@Author  :   Coder-Sakura
@Version :   1.1
@Desc    :   None
'''

# here put the import lib
import time
import json

from dynamic_import import modules_dynamicLoad
from Arsenal.basic.bot_tool import tool
from Arsenal.basic.thread_pool import ThreadPool, callback
from Arsenal.basic.task_processor import taskprocessor
from Arsenal.basic.log_record import logger
from Arsenal.basic.msg_temp import MYBOT_ERR_CODE, EXECUTOR_TASK_STATUS_INFO, TASK_PROCESSOR_TEMP

class Executor:
	"""事件处理:插件轮询/热重启"""
	def __init__(self):
		# 为tool创建线程池pool
		self.init_thread_pool(8)

		# 启动定时任务检测线程 - 实验性
		# tool.pool.put(self.cycle_task_detect, (), callback)

		# 消息 - 插件解析器初始化
		try:
			tool.modules_dynamicLoad = modules_dynamicLoad
		except Exception as e:
			logger.warning(MYBOT_ERR_CODE["Generic_Exception_Info"].format(e))
			logger.warning("<dynamic_import>模块导入插件出错,请检查<dynamic_import>模块/插件")
		
		# 数据库预处理
		DBCheck()


	# thread_pool func start
	def init_thread_pool(self, max_num=8)->bool:
		"""
		初始化线程池,暂不考虑reload情况
		< -- not reliable! -- >
		"""
		try:
			if hasattr(tool,"pool"):
				tool.pool.terminal = True
				logger.debug("reload thread pool in 3s.")
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
	def cycle_task_detect(self, cycle=10):
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

	def reload_modules(self, reimport=True)->dict:
		"""
		加载插件目录插件
		:params reimport: True -> 重新导入
		:params pathname: todo
		:params recursive: todo
		:params class_start_with: todo
		"""
		return tool.modules_dynamicLoad.import_modules(reimport=reimport)

	def exec(self, mybot_data):
		"""
		插件解析器解析消息,以匹配出结果
		"""
		logger.debug(f"<mybot_data> - {mybot_data}")
		msg = mybot_data["arrange"].get("message", "")
		if msg:
			try:
				tool.modules_dynamicLoad.plugin_selector(mybot_data)
			except Exception as e:
				logger.warning(MYBOT_ERR_CODE["Generic_Exception_Info"].format(e))
		else:
			# status = tool.auto_report_err(msg)
			logger.warning(f"<mybot_data> not found <message> - {mybot_data}")
			
class DBCheck:
	"""数据库信息预处理"""
	def __init__(self):
		self.group_check()
		self.plugin_check()

	def group_check(self):
		"""群组信息预处理"""
		params = {}
		group_info = tool.send_cq_client(params=params, api="cq_get_group_list")

		if not group_info or not group_info["data"]:
			logger.warning(f"<group_info err> - {group_info}")
			return

		for _ in group_info["data"]:
			if not tool.db.select_records(table="group_chats", **{"gid": _["group_id"]}):
				insert_data = {
					"gid": int(_["group_id"]),
					"group_level": int(tool.level["general_group_level"]),
					"is_qqBlocked": 0
				}

				tool.db.insert_records(
					table="group_chats",
					**{"insert_data": insert_data}
				)

		result = tool.db.select_records(table="group_chats")
		logger.info(f"群组: {len(result)}个")
		logger.debug(f"group_chats - {result}")

	def plugin_check(self):
		"""插件信息预处理"""
		copy_module_dicts = tool.modules_dynamicLoad.module_dicts

		if not copy_module_dicts:
			logger.warning(f"<copy_module_dicts> - {copy_module_dicts}")
			return 

		for module_name,module_addr in copy_module_dicts.items():
			if not tool.db.select_records(table="plugin_info", **{"plugin_name": module_name}):
				insert_data = {
					"plugin_name": module_name,
					"plugin_nickname": module_addr["plugin_nickname"],
					"plugin_type": module_addr["plugin_type"],
					"plugin_level": module_addr["plugin_level"],
					# 默认运行中 - 0
					"plugin_status": 0,
					# 默认无限制规则 - {}
					"plugin_limit_info": json.dumps({})
				}

				tool.db.insert_records(
					table="plugin_info",
					**{"insert_data": insert_data}
				)

		result = tool.db.select_records(table="plugin_info")
		logger.info(f"数据库插件: {len(result)}个")
		logger.info(f"本地插件: {len(copy_module_dicts)}个")
		logger.debug(f"plugin_info - {result}")
