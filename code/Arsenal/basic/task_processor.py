# -*- encoding: utf-8 -*-
'''
@File    :   task_processor.py
@Time    :   2021/11/26 10:25:03
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import time


from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.msg_temp import TASK_PROCESSOR_TEMP

class TaskProcessor:
    def __init__(self):
        self.task_status_temp = ["completed", "ongoing", "waiting", "error"]
        self.all_flag = "all"
    
    def create_tasks(self,insert_data):
        """
		根据insert_data创建task记录
		:params insert_data: 任务信息, key顺序必须与数据库字段一样
		:return: True or False
		"""
        logger.debug(f"<insert_data> - {insert_data}")
        result = tool.db.insert_records(cqp_data=None, table="tasks", **{"insert_data": insert_data})
        return result
        
    def get_tasks(self,nums=0,filter=None):
        """
        从tass表中根据优先级获取1~10个/全部waiting状态的任务
        :params nums: 获取的任务数量
			range:1~10 0 -> all
		:return: tasks_dict
		"""
        # result数量
        if 1 <= nums <= 10:
            limit = nums
        elif nums == 0:
            limit = 0
        else:
            limit = 10

        # 任务状态筛选
        if filter in self.task_status_temp:
            filter_dict = {"task_status": filter}
        elif filter == self.all_flag:
            filter_dict = {}
        else:
            filter_dict = {"task_status": "waiting"}

        result = tool.db.select_records(table="tasks",limit=limit,**filter_dict)
        result = sorted(result, key=lambda x: x["task_level"], reverse=True)
        return result

    """
    TODO 2021年12月8日23:45:17写下
    1. 后续版本再处理数据表执行任务
      当前可参考Executor.cycle_task_detect
    2. 移植到Executor内
    """ 
    @logger.catch
    def exec_tasks(self,task):
        """
        执行任务
        :params task: task任务体及信息
		:return: None
		"""
        while True:
            # 执行前校验数据
            # ==== exec_time ====
            # exec_time值是否存在
            if not task.get("exec_time",""):
                logger.info(TASK_PROCESSOR_TEMP["NULL_VALUE"].format("exec_time"))
                return False

            try:
                # exec_time格式化格式是否正确
                task["exec_time"].strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                logger.info(e)
                logger.info(TASK_PROCESSOR_TEMP["NOT_DATETIME_DATA"].format("exec_time"))
                return False

            # 判断是否为datetime.datetime对象
            # if not isinstance(task["exec_time"],datetime.datetime):
            #     logger.info(TASK_PROCESSOR_TEMP["NOT_DATETIME_DATA"].format("exec_time"))
            #     return False
            # ==== exec_time ====

            # ==== exec_task ====
            if not task["exec_task"]:
                logger.info(TASK_PROCESSOR_TEMP["NULL_VALUE"].format("exec_task"))
                return 

            # ==== exec_task ====
            try:
                result = eval(task["exec_task"])
            except Exception as e:
                logger.warning(f"<thread task exception> - {e}| <exec_task> - {task['exec_task']}")
            else:
                print(result)

            # break判断
            # 根据task_type判断是否跳出
            if task.get("task_type","once") == "once":
                break
            elif task.get("task_type","once") == "cycle":
                pass
            else:
                break

            time.sleep(10)

    @staticmethod
    def task_count(task_list):
        _count_result = {}
        for _ in task_list:
            if _["task_status"] not in _count_result.keys():
                _count_result[_["task_status"]] = 1
            else:
                _count_result[_["task_status"]] += 1
        return _count_result

    

taskprocessor = TaskProcessor()