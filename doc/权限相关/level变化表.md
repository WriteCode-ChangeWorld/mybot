### 用户level说明表

| level | user_limit_count | user_limit_cycle | description                         |
| :---: | :--------------: | :--------------: | :---------------------------------- |
|   1   |      LIMIT       |                  | 惩罚level，防止刷屏                 |
|  10   |        3         |        10        | 普通用户，单位时间内bot可用次数为3  |
|  50   |        -1        |        -1        | 高级用户，单位时间bot可用次数无限制 |
|  999  |        -1        |        -1        | 管理员，单位时间bot可用次数无限制   |

+ 用户调用次数的更新周期（user_limit_cycle），默认10秒，-1代表无限制

+ 用户可调用次数（user_limit_count）指的是用户在单位时间内bot的可用次数，比如10秒内可响应3次；-1代表不做限制

+ 用户每调用一次机器人，用户目前已调用次数（user_call_count）+ 1；

  ```python
  def demo()
      if not user_limit_count == -1:
          user_limit_count += 1
  ```

  

+ 当前消息时间（now_time）大于用户调用时间周期的到期时间 (cycle_expiration_time) 时，重置为now_time+10

  ```python
  if user_limit_cycle == -1:
      pass
  elif now_time > cycle_expiration_time:
      seconds = user_level[level]["user_limit_cycle"]
      offset_seconds = datetime.timedelta(seconds=10)
      now_time += offset_seconds
      cycle_expiration_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
  ```

  

+ 当user_call_count等于user_limit_count且（now_time<cycle_expiration_time）时，发送调用过快提醒，进入超时等待（user_limit_cycle）秒



### 群组level说明表

| level | description | remarks |
| :---: | :---------: | :-----: |
|       |             |         |
|       |             |         |
|       |             |         |



### 插件level说明表

| level | description | remarks |
| :---: | :---------: | :-----: |
|       |             |         |
|       |             |         |
|       |             |         |





### **难点**

**(user_limit)秒内最多调用(单位时间调用阈值)次**
**（在10秒内最多调用3次）**

+ user_limit_cycle= 10
+ user_limit_count = 3
+ user_call_count = 0
+ last_call_date = '2021-05-19 15:18:35'



### **调用datetime函数**

+ strftime——datetime 2 str
+ strptime——str 2 datetime



1. 如何判断3次
2. 如何重置user_call_count为0
3. 重启如何确保上下文状态



### **场景**

+ 第一次在1秒，第二次在11秒
+ 第一次在1秒，第三次在9秒，第四次在11秒
+ 第一次在1秒，第三次在7秒，第四次在9秒



+ 当前调用时间(now_time) > 到期时间(cycle_expiration_time)——刷新数据
+ 当前调用时间(now_time) < 到期时间(cycle_expiration_time)
  + 在周期内，调用次数小于调用限制次数——功能执行
  + 在周期内，调用次数等于调用限制次数——提示用户、功能不执行、刷新数据
  + 由于第二点，所以不存在调用次数大于调用限制次数的情况

> 刷新数据—>

```python
"""
func to limit time and times
Only return True or False
"""
import datetime

user_info = self.db.check_user(eval_cqp_data)
# 未创建用户 | user_info == ""
# user_info["cycle_expiration_time"]为create_date
if not user_info:
    user_info = self.db.create_user(eval_cqp_data)
    
# 非限制权限等级不做限制
# [50,999]
if user_info["user_level"] in self.config.vip_level:
    return True
    
now_time = datetime.datetime.now()
# last_call_date > cycle_expiration_time

# 1.当前时间大于周期的到期时间
# 重置user_call_count,cycle_expiration_time
if now_time > user_info["cycle_expiration_time"]:
    user_info["user_call_count"] = 0
    # now_time + user_limit
    offset_seconds = datetime.timedelta(seconds=int(user_info["user_limit"]))
    user_info["cycle_expiration_time"] = now_time + offset_seconds
    self.db.update_records(user_info)
    return True
# 限时限次判断,是否执行下一步
# 2.当前时间小于等于周期的到期时间
elif now_time <= user_info["cycle_expiration_time"]:
    # 已使用次数 <= 可用次数
    if user_info["user_call_count"] < user_info["user_limit_count"]:
        return True
    # 不存在已使用次数 > 可用次数
    elif user_info["user_call_count"] = user_info["user_limit_count"]:
        user_info[""]
        return False




```









