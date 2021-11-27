# -*- encoding: utf-8 -*-
'''
@File    :   task_processor.py
@Time    :   2021/11/26 10:25:03
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
from Arsenal.basic.db_pool import DBClient
from Arsenal.basic.log_record import logger


class TaskProcessor:
    def __init__(self):
        pass
    
    def create_tasks(self,insert_data):
        """
		根据insert_data创建task记录
		:params insert_data: 任务信息, key顺序必须与数据库字段一样
		:return: True or False
		"""
        logger.debug(f"<insert_data> - {insert_data}")
        result = DBClient.insert_records(cqp_data=None, table="tasks", **{"insert_data": insert_data})
        return result
        
    def get_tasks(self,nums=0):
        """
        从tass表中根据优先级获取nums个waiting状态的任务
        :params nums: 获取的任务数量
			range:1~10 0 -> all
		:return: tasks_dict
		"""
        if nums == 0:
            limit = -1
        elif 1 <= nums <= 10:
            limit = nums
        else:
            limit = 10
        result = DBClient.select_records(table="tasks",limit=limit,**{"task_status":"waiting"})
        result = sorted(result, key=lambda x: x["task_level"], reverse=True)
        logger.debug(f"<result> - {result}")
        return result

    def exec_tasks(self,tasks_list):
        pass
    

taskprocessor = TaskProcessor()