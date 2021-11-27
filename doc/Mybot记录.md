问题点收集

### 刷屏用户如何判别和区分?

> 归属：module: level_manager.func

a.判断机制: 连续5次发送相同消息,判断为刷屏用户(相同消息使用md5进行判断)
【消息记录表】   select raw_message from 
b.触发点: 用户管理插件应在Church-权限/黑名单检查后进行监测
c.处罚机制: 接下来1分钟内丢弃该账号所有的信息!



---

### 随机发言插件

> 归属：folder: Arsenal目录

(用于获取群组气氛)(仅群组)

【消息次数记录表】每3天清除count为1的消息,相同消息若存在则count+1,不存在则创建记录

【触发】成员发言后,有1.25%概率进行复读或从count>5的消息中(无则跳过)

【其他】触发概率要求可在线调整



---

###  合并转发 ( 群 )

> 归属：module: /basic/bot_tool.func

API

```
127.0.0.1:5700/send_group_forward_msg?group_id=813614458&messages=[{"type":"node","data":{"id":"966216748"}}]
```

CQ code

```
[{"type":"node","data":{"id":"966216748"}}]
```



---

### 主动式插件与被动式插件的区分和作用

+ 主动式插件作为功能插件，包括用户发起查询、搜索、随机索取，总而言之就是用户发送包括特定关键字与值的语句，从而命中插件的`parse`函数解析的结果
+ 被动式插件更像一种地下工作者，其作用包括但不限于：监控、日志写入、每日签到、数据收集、数据统计、用户发言习惯统计等；使用被动式插件可以无声无息的收集用公开数据 ，以作出更多优化与新功能



**区分**  

主动式插件



被动式插件



---

### bot_tool新增时间数据相关的函数

新增func：时间格式转换、时间偏移

时间格式转换

```python
import datetime

def change_timedata(datetime_obj=None, str=None, temp_format='%Y-%m-%d %H:%M:%S'):
    """
    将datetime/str类型的时间数据转换为str/datetime类型的时间数据.支持自定义format转换格式
    :params datetime_obj: datetime格式的时间数据
    :params str: str格式的时间数据
    :return: datetime/str类型的时间数据 or None
    """
    # 只允许同时转换一种obj
    if not datetime_obj and not str:
        return None
    elif datetime_obj and str:
        return None
    
    if datetime_obj:
        try:
            return datetime_obj.strftime(temp_format)
        except:
            return None
    
    if str:
        try:
            return datetime.datetime.strptime(str,temp_format)
        except:
            return None
```

时间偏移

```python
import datetime

def change_timedelta(datetime_obj,offset_dict={}):
    """给定一个datetime_obj和推移条件,返回一个推移后的datetime_obj"""
    if not offset_dict:
        return None
    
    k,v = list(offset_dict)[0],int(offset_dict[k])
    try:
        offset = datetime.timedelta(eval(f"{k}={v}"))
    except Exception as e:
        return None
    return datetime_obj += offset
```

---

### 2021年10月28日18:54:32随笔

1、发完图后，机器人补发。卡尔类型的图，比如xxx给你发图了，多说谢谢xxx；
解禁语句：谢谢xxx
2、不发则加入is_qqBlocked，每次检查该用户的发言是否是解禁语句
3、vip或试用群用户可免除该项
具体怎么处理待确认

1、来点插画，输出模式选择可以提上日程



---

### 搜图模式

**指定搜图方式**

1、问答式搜图

触发词

```markdown

```

注意点

```markdown

```



2、回复式搜图

触发词

```markdown

```

注意点

```markdown

```



3、连续搜图触发词

```markdown

```

注意点

```markdown

```



**指定搜图引擎**

默认为：`saucenao`

+ -s：`saucenao`
+ -a：`ascii2d`
+ -y：`yandex`



**结果匹配**

`saucenao`

```python

```

`ascii2d`

自己有写[demo](D:\Code\Thunder\爬虫相关\1、抓包\搜图相关_iwara\ascii2d.net\demo.py)，也可以参考[这个](https://github.com/FloatTech/AnimeAPI/blob/main/ascii2d/ascii2d.go)

```python

```

`yandex`

```python

```

---

### 随机插画模式

+ 反代直链
+ 二维码（↓）
+ 字符画
+ 幻影坦克
+ master1200展示（增加服务端api模块:random-info接口返回字段:urls）
+ 





---

### 控制普通群与测试群

1、每日签到插画

测试群：`regular` + 不模糊
普通群：`regular` + 高斯模糊`radius=10`

**实现**

每日签到插画插件针对不同权限进行不同形式的展示

插件基础使用权限：10（被拉黑名单



---

### 插件热重载

dynamic_import，重新导入

---

### 主动调用(线程池任务)——**bot_tool**

> 归属：module: executor

具体文档参照：[Executor线程池相关文档](.\基本文档\Executor线程池相关文档.md)













