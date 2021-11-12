### 用户数据表——table:users

| 名称                  | 描述                                                         | 类型             |
| :-------------------- | ------------------------------------------------------------ | ---------------- |
| id                    | 自增id                                                       | int              |
| uid                   | 用户id                                                       | int(20)          |
| gid                   | 群组id                                                       | int(20)          |
| ~~cid~~               | ~~用户卡，user_id+"_"+group_id~~                             | varchar(40)      |
| user_level            | 用户权限等级，默认为10 :star2:                               | int(5)           |
| user_limit_cycle      | 用户调用次数的更新时间周期，默认为10秒:star2:                | int(3)           |
| user_limit_count      | 用户可调用次数， 默认为3次:star2:                            | int(3)           |
| user_call_count       | 用户目前已调用次数，默认为0次                                | int(3)           |
| magic_thing           | 魔方(虚拟货币)的数量，默认为0个                              | int(8)           |
| is_remind             | 每日插件是否触发，默认为0；0为False，1为True                 | tinyint(1)       |
| is_koi                | 是否为天选之人，默认为0；0为False，1为True                   | tinyint(1)       |
| is_qqBlocked          | 是否为黑名单人员，默认为1；0为False(拉黑)，1为True           | tinyint(1)       |
| retention_prob        | 保留的每日抽卡概率，默认为0                                  | float(5,3)       |
| ~~msg_count~~         | ~~当天发言次数，默认为0~~                                    | ~~int(5)~~       |
| ~~year_msg_count~~    | ~~一年总发言次数(记录创建时到目前的发言次数)，默认为0~~      | ~~int(10)~~      |
| ~~week_info~~         | ~~本周的抽卡情况~~                                           | ~~varchar(200)~~ |
| ~~year_info~~         | ~~一年中的抽卡情况(记录创建时到目前的抽卡情况)~~             | ~~varchar(200)~~ |
| daily_date            | 每日插件更新时间, 如:2021-05-19 15:18:35                     | DATETIME         |
| create_date           | 该记录创建的时间, 如:2021-05-19 15:18:35                     | DATETIME         |
| last_call_date        | 上一次调用机器人的时间(主动式插件), 如:2021-05-19 15:18:35，创建时默认为create_date | DATETIME         |
| cycle_expiration_time | 用户调用时间周期的到期时间, 如: 2021-05-19 15:18:45，创建时默认为create_date+user_limit_cycle | DATETIME         |

#### **date**

+ 收到信息，未存在对应用户记录时，`is_remind`为False，不用判断`date`；此时`date`为当前日期
+ 收到信息，存在对应用户记录时
  1. 判断记录中`date` 与今日`date`是否一致；不一致则`is_remind`为False，执行；一致则判断第2点
  2. 判断`is_remind`是否为False；False，执行



#### **dateall_date**

+ 创建用户时，`last_call_date`与`create_date`相同
+ 存在用户记录时，由插件主动去更新

```python
# 时间偏移
import datetime
# 当前时间
now = '2021-05-19 15:18:35'
# 转化为datetime对象 
now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
# 获取10秒后的timedelta对象 ※
offset_seconds = datetime.timedelta(seconds=10)
# 未来时间 ※
future = now + offset_seconds
转化为str
future = datetime.datetime.strptime(future, "%Y-%m-%d %H:%M:%S")

# 时间对比
a = datetime.datetime(2021, 5, 21, 18, 0, 22, 174963)
b = '2021-05-19 15:18:35'
b = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
print(a>b)
# True
```







#### week_info

```python
# week_info默认temp
# 每周清空一次,数据累加到year_count
week_info = {
    "ur":0,
    "ssr":0,
    "sr":0,
    "r":0,
    "extra_magic_thing":0,
    "extra_magic_get":0,
    "extra_magic_lost":0
}
# year_info默认temp
year_info = {
    "ur":0,
    "ssr":0,
    "sr":0,
    "r":0,
    "extra_magic_thing":0,
    "extra_magic_get":0,
    "extra_magic_lost":0
}
```

```python
# week_info模拟数据
week_info = {
    "ur":7,
    "ssr":7,
    "sr":7,
    "r":7,
    "extra_magic_thing":100,
    "extra_magic_get":100,
    "extra_magic_lost":100
}
```



#### 测试数据获取

```python
import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor

pool = PooledDB(
    creator=pymysql,
    maxconnections=8,	# 连接池允许的最大连接
    mincached=1,	# 连接池中的初始空闲连接数
    maxcached=1,	# 连接池中最大闲置连接数
    blocking=True,
    host="127.0.0.1",user="root",passwd="Huawei",db="mybot",port=3306,charset="utf8mb4"
)

conn = pool.connection()
cur = conn.cursor(DictCursor)
sql_1 = "SELECT * FROM user LIMIT 1"
cur.execute(sql_1)
res = cur.fetchall()

# str转json -- week_info,year_info
import json
week_info = json.loads(res[0]["week_info"])
week_info = json.loads(res[0]["year_info"])
# 转换datetime对象 -- date,create_date,last_call_date字段
import datetime
d = res[0]["date"]
d = d.strftime('%Y-%m-%d')
c = res[0]["create_date"]
c = c.strftime('%Y-%m-%d %H:%M:%S')
l = res[0]["last_call_date"]
l = l.strftime('%Y-%m-%d %H:%M:%S')
```

```python
res
"""
[{'id': 1,
  'user_id': 123456789,
  'group_id': 199999,
  'user_card': '123456789_199999',
  'user_level': 10,
  'user_limit': 10,
  'user_limit_count': 3,
  'user_call_count': 0,
  'magic_thing': 0,
  'is_remind': 0,
  'is_koi': 0,
  'is_qqBlocked': 0,
  'retention_prob': '0.0',
  'msg_count': 0,
  'year_msg_count': 0,
  'week_info': '{\r\n    "ur":0,\r\n    "ssr":0,\r\n    "sr":0,\r\n    "r":0,\r\n    "extra_magic_thing":0,\r\n    "extra_magic_get":0,\r\n    "extra_magic_lost":0\r\n}',
  'year_info': '{\r\n    "ur":0,\r\n    "ssr":0,\r\n    "sr":0,\r\n    "r":0,\r\n    "extra_magic_thing":0,\r\n    "extra_magic_get":0,\r\n    "extra_magic_lost":0\r\n}',
  'date': datetime.datetime(2021, 5, 19, 0, 0),
  'create_date': datetime.datetime(2021, 5, 19, 15, 18, 35),
  'last_call_date': datetime.datetime(2021, 5, 19, 15, 18, 35)}]
"""
```







---



### 每日数据表able:day_info

| 名称             | 描述              | 类型          |
| ---------------- | ----------------- | ------------- |
| id               | 自增id            | int           |
| date             | 日期YY:MM:DD      | DATETIME      |
| user_id          | 用户id            | INT(20)       |
| group_id         | 群组id            | INT(20)       |
| msg_count        | 当天发言次数      | INT(5)        |
| card             | 抽卡情况          | varchar(1024) |
| extra_magic_get  | 随机事件-魔方获得 | varchar(1024) |
| extra_magic_lost | 随机事件-魔方丢失 | varchar(1024) |

