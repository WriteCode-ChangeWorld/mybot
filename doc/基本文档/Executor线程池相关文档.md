### 主动调用(线程池任务)

[TOC]

---

> 归属：module: executor

### **线程池初始化**

同一个进程内，线程池初始化。通过机器人内部将线程任务添加到线程任务表(tasks)



~~判断队列是否为空，EXECUTOR.pool.q.empty()不可靠~~

```python
# 初始化
def init_thread_pool(self,max_num=8):
    """初始化线程池"""
    try:
        if hasattr(tool,"pool"):
            tool.pool.close()
    except Exception as e:
        logger.debug(MYBOT_ERR_CODE.format(e))
    finally:
        tool.pool = ThreadPool(max_num=max_num)
        return tool.pool
```



### 线程池启停控制

> 通过Executor.init_thread_pool将tool.pool.terminal更改为True，来中断线程任务执行，再重新实例化一个ThreadPool线程池



```python

```







### **线程池轮询检测任务**

> 轮询线程任务表里是否存在任务状态为waiting的任务

```python
# 轮询检测
# 将任务监测线程加入到线程池中执行
# 可通过设置tool.pool.terminal来中断任务进行

@logger.catch
def cycle_task_detect(self,cycle=10):
    while True:
        # 判断中断条件
        if tool.pool.terminal:
            break

        tasks_list = self.get_tasks()
        if not tasks_list:
            logger.info("TABLE:tasks has no tasks")
        else:
            self.exec_tasks(tasks_list)

        print(f"cycle {tool.pool.terminal}")
        time.sleep(cycle)
```



### 线程池创建任务

> module: ./Arsenal/basic/task_processor

插入数据

```json
// 插入数据 1
{
    "creator_id": 123,
    "group_id": 123,
    "task_type": "cycle",
    "by_plugin": "",
    "create_time": "2021-11-26 10:13:14",
    "task_status": "waiting",
    "task_level": 5,
    "exec_task": "",
    "exec_time": "2021-11-26 10:13:14",
    // 报告人及群组未定义则默认报告creator
    "report_user_id": "",
    "report_group_id": ""
}

// 插入数据 2
{
    "creator_id": 123,
    "group_id": 123,
    "task_type": "cycle",
    "by_plugin": "",
    "create_time": "2021-11-26 10:13:14",
    "task_status": "waiting",
    "task_level": 5,
    "exec_task": "",
    "exec_time": "2021-11-26 10:13:14",
    // 报告人及群组未定义则默认报告creator
    "report_user_id": 0,
    "report_group_id": -1
}
```

传参数据

```json
// 传参数据
{
    "creator_id": 123,
    "group_id": 123,
    "task_type": "cycle",
    "by_plugin": "",
    "create_time": "2021-11-26 10:13:14",
    "task_status": "waiting",
    "task_level": 5,
    "exec_task": "",
    "exec_time": "2021-11-26 10:13:14",
    // 报告人及群组未定义则默认报告creator
    "report_user_id": "",
    "report_group_id": ""
}
```





**线程池执行任务**

> module: ./Arsenal/basic/task_processor

+ 初始化时

+ 插件调用

  + 重复使用：定时清理搜图队列闲置用户（添加/更新`task`任务信息）
    新增：无对应`user_id+group_id`，且`task_type`为`img_search_cycle`(根据实际定义)类型的`task`
    更新：更新对应`user_id+group_id`，且`task_type`为`img_search_cycle`的`task`

  + 一次性任务：备忘录

    ```python
    while True:
        func()
        
    func()
    ```

    



### **线程池及应用**

检测长时间处于搜图模式（1分钟超时）的用户，定期清理搜图队列

```python
# 加入搜图队列时新建task,1分钟后从搜图列队中移除该用户


# 当用户发送[CQ:image]类型的CQ码,则更新exec_time(从当前时间往后延长1分钟)
```



### 测试

```python
cd D:\Code\mybot\code
python

from executor import Executor,tool
E = Executor() # 初始化线程池并启动任务检测线程
print(tool.pool.terminal)
print(tool.pool.max_num)
print(tool.pool.q.empty())

E.init_thread_pool(max_num=20) # 将旧线程池的任务全部中断，并启动新线程池
print(tool.pool.terminal)
print(tool.pool.max_num)
print(tool.pool.q.empty())


tool.pool.put(E.cycle_task_detect, ())
print(tool.pool.terminal)
print(tool.pool.max_num)
print(tool.pool.q.empty())
print(tool.pool.q.qsize())
```

