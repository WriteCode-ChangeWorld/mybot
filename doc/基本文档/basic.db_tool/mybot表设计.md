## 数据库交互场景梳理

[TOC]

---

### 底层插件



### 业务逻辑

新用户记录添加



### 功能插件

搜索插件检索
包括`Saucenao`、`Ascii2d`、`yandex`、`What anime`

+ 查询是否处于搜图队列
+ 从搜图队列中删除用户记录（uid/gid/startTime/）
+ 



### 业务表需求

#### 用户表——users

| 名称                  | 描述                                                         | 类型       | 备注 |
| :-------------------- | ------------------------------------------------------------ | ---------- | ---- |
| id                    | 自增id                                                       | int        |      |
| uid                   | 用户id                                                       | int(20)    |      |
| gid                   | 群组id                                                       | int(20)    |      |
| user_level            | 用户权限等级，默认为10 :star2:                               | int(5)     |      |
| user_limit_cycle      | 用户调用次数的更新周期，默认为10秒:star2:                    | int(3)     |      |
| user_limit_count      | 用户可调用次数， 默认为3次:star2:                            | int(3)     |      |
| user_call_count       | 用户目前已调用次数，默认为0次                                | int(3)     |      |
| magic_thing           | 魔方(虚拟货币)的数量，默认为0个                              | int(8)     |      |
| is_qqBlocked          | 是否被拉黑，默认为1；0为False(拉黑)，1为True                 | tinyint(1) |      |
| create_date           | 该记录创建的时间, 如:2021-05-19 15:18:35                     | DATETIME   |      |
| last_call_date        | 上一次调用机器人的时间(主动式插件), 如:2021-05-19 15:18:35，创建时默认为create_date | DATETIME   |      |
| cycle_expiration_time | 用户调用时间周期的到期时间, 如: 2021-05-19 15:18:45，创建时默认为create_date+user_limit_cycle | DATETIME   |      |

用户权限到期时间（0为永久，其他为具体时间，从时间维度上进行对比）



#### 群组表——group_chats

| 名称         | 描述               | 类型         | 备注                                                         |
| ------------ | ------------------ | ------------ | ------------------------------------------------------------ |
| id           | 自增id             | int          |                                                              |
| gid          | 群组id             | int(20)      |                                                              |
| group_name   | 群组名称           | VARCHAR(100) |                                                              |
| group_level  | 群组权限；默认为10 | int(5)       | 使用某些插件时，需要当前群组权限与用户权限高于插件最低权限；<br />当前群组权限高于插件最低权限，但使用者用户权限不够，不可使用；<br />当前用户权限高于插件最低权限，但当前群组权限不够，也不可在该群使用； |
| is_qqBlocked | 是否被拉黑         | tinyint(1)   | 群组是否被拉黑，默认为1；0为False(拉黑)，1为True             |
|              |                    |              |                                                              |

##### 获取群列表

`req：127.0.0.1:5700/get_group_list`

resp

```json
{
    "data":[
        {
            "group_create_time":0,
            "group_id":163131570,
            "group_level":0,
            "group_memo":"",
            "group_name":"iACG-二次元资源聚合爬虫项目群",
            "max_member_count":200,
            "member_count":6
        },
        {
            "group_create_time":0,
            "group_id":730772237,
            "group_level":0,
            "group_memo":"",
            "group_name":"工具留档群",
            "max_member_count":200,
            "member_count":7
        },
        {
            "group_create_time":0,
            "group_id":813614458,
            "group_level":0,
            "group_memo":"",
            "group_name":"九号 NK qqbot测试群",
            "max_member_count":200,
            "member_count":6
        },
        {
            "group_create_time":0,
            "group_id":832455123,
            "group_level":0,
            "group_memo":"",
            "group_name":"ToDo For Coder_Sakura",
            "max_member_count":200,
            "member_count":8
        },
        {
            "group_create_time":0,
            "group_id":930858571,
            "group_level":0,
            "group_memo":"",
            "group_name":"永远の21 | qqbot测试群",
            "max_member_count":200,
            "member_count":74
        },
        {
            "group_create_time":0,
            "group_id":1072957655,
            "group_level":0,
            "group_memo":"",
            "group_name":"mybot测试群2_private",
            "max_member_count":200,
            "member_count":8
        }
    ],
    "retcode":0,
    "status":"ok"
}
```



#### 消息表——messages

| 名称             | 描述                 | 类型          | 备注                               |
| :--------------- | -------------------- | ------------- | ---------------------------------- |
| id               | 自增id               | id            |                                    |
| message_type     | 消息类型             | VARCHAR(20)   | 群组消息group<br />私聊消息private |
| user_id          | 用户qq号码           | INT(20)       |                                    |
| user_name        | 用户名称，非群昵称   | VARCHAR(100)  | 注意只取前100                      |
| group_id         | 群组号码             | int(20)       |                                    |
| group_name       | 群组名称，非群备注名 | VARCHAR(100)  | 注意只取前100                      |
| raw_message      | 消息内容             | VARCHAR(1024) |                                    |
| message_datetime | 消息时间             | DATETIME      |                                    |
|                  |                      |               |                                    |



pymysql 查询 1054

```
# pymysql.err.OperationalError
https://blog.csdn.net/qq_42098517/article/details/89300618
https://blog.csdn.net/qq_45701131/article/details/115803260

# repr将参数值全部转化为str,可解决pymysql where查询不到中文字符串/1054问题
```









#### 插件信息表——plugin_info

参考文件：`插件调用与自定义规则.md`

| 名称          | 描述                   | 类型        | 备注                                                         |
| ------------- | ---------------------- | ----------- | ------------------------------------------------------------ |
| id            | 自增id                 | int         |                                                              |
| plugin_name   | 插件名称               | VARCHAR(40) | 由dynamic_import获取<br />`Arsenal`目录下符合规则的插件即可<br />（bot_ascii2d） |
| plugin_type   | 插件类型               | int(3)      | 主动触发式、被动触发式                                       |
| plugin_level  | 使用插件所需的最低权限 | int(5)      | 默认为10                                                     |
| plugin_status | 插件状态               | int(3)      | 0：运行中<br />1：已卸载<br />2：出现错误                    |

获取本地插件列表——dynamic_import
插件所需最低权限——level，用户或该群组达到该权限后即可使用该插件



#### 任务表——tasks

| 名称            | 描述                                 | 类型          | 备注                                                         |
| --------------- | ------------------------------------ | ------------- | ------------------------------------------------------------ |
| id              | 自增id                               | int           |                                                              |
| creator_id      | 创建任务的用户qq号码                 | INT(20)       | 0代表程序内部创建<br />qq号码代表用户                        |
| group_id        | 创建任务的用户所在群组id             | INT(20)       | 0代表程序内部创建<br /><br />1代表私聊创建<br />群组id代表用户所在群组 |
| create_time     | 任务创建时间                         | DATETIME      |                                                              |
| task_status     | 任务状态                             | VARCHAR(20)   | completed代表已完成<br />ongoing代表进行中<br />waiting代表等待中<br />error代表执行出错 |
| task_level      | 任务优先级,越高越先执行              | INT(5)        |                                                              |
| exec_task       | 任务执行语句；可直接使用eval转化运行 | VARCHAR(1024) |                                                              |
| exec_time       | 执行时间<br />YY:MM:DD hh:mm:ss      | DATETIME      |                                                              |
| report_user_id  | 结果报告人id                         | INT(20)       | 0代表报告人为creator_id<br />-1代表无需报告结果<br />其他代表report_user_id |
| report_group_id | 结果报告人所在群组id                 | INT(20)       | 0代表group_id<br />-1代表无需报告结果<br />其他代表report_group_id |



#### 插件表——bot_day_illust

|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |



插件表分表建表

+ 每日签到表——day_illust
+ 图片搜索——image_search（整合



整合基础模块以提供给Arsenal插件模块调用

+ 图片处理类（saucenao、ascii2d、yandex、高斯模糊）
+ 











