# Mybot:robot:开发文档 

2021年2月7日21:48:54

[TOC]



## 使用前的准备

---

### 数据库方面

Mysql







## 项目结构

---

:file_folder: `mybot`

```
.
|-- Readme.md // 尚未编写
|-- backup 	// 2.0版本备份(不作上传)
|-- code 	// mybot代码
|-- doc 	// 相关文档
|-- others 	// 存放以前的文档及1.0版本服务器文件(不作上传)
|-- test 	// 意愿为测试代码,目前为杂项(不作上传)
```

+ :file_folder: code

存放mybot机器人的代码，其子目录结构如下：

```
# 20210207
.
|-- Arsenal			// 功能插件
|	-- basic		// 基础插件
|-- res				// 公共资源及插件工作目录
|-- temp			// 配置模板文件,如default.yaml
|-- church.py		// 上层主程序,启动程序
|-- config.yaml 	// 机器人配置文件
|-- executor.py 	// 事件处理器
|-- bishop.py		// 权限监控及更改
|-- test.conf		// 实验性记录用户信息(未处理)
|-- dynamic_import.py // 插件引擎
|-- 更新日志.md 	// 未处理
```



### 基础模块 

---

+ 网络模块——BNConnect √
  + 网络请求——baseRequests
  + 文件下载——download_file（流处理）参考之前的脚本或iwara
+ 插件工作目录获取——plus_res_directory
+ 日志记录——log_record √
+ 数据库操作相关——db_pool √
  + PyMysql+DBUtils
+ 文件处理——fileHandler √
  + json读写√
  + yaml读写√
+ 错误处理(用于向管理员报告错误日志、触发语句):flags:
+ 线程池——thread_pool √
+ 定时任务——sched_task(未编写:flags:)
+ 获取系统状态——sys_info (优先级降低)
+ Bot配置及全局变量管理——bot_tool
+ 短链接集成——short_link (优先级降低)
+ 模板消息——msg_temp (doing)



### 功能模块

---

+ 搜图插件
  + Saucenao搜图——bot_saucenao_img（待优化）
  + Ascii2d搜图——bot_ascii2d_img（待优化）
  + Yandex搜图——yandex_upload_demo（未编写）:flags:
+ 图片报时——bot_report_time
+ 每日涩图——bot_day_illust（被动式插件）
+ 随机涩图——bot_color_img
  + 反代直链
  + 图片-幻影坦克——bot_phantom_img:flags:
  + 图片-二维码——bot_qr_img——:flags:有demo，未编写（优先级低）
  + 高斯模糊——bot_gaussianblur_img
  + 字符画——old_img2ascii / img2ascii——:flags:
+ 碧蓝航线秘书舰——bot_blhx_prediction（目前下架，维护优先级低）
+ What Anime搜番——bot_anime（未从原脚本改变为模块:flags:)
+ 直链获取
  + pixiv 插画信息获取——bot_pid_info（未编写:flags:)
  + d站直链:flags::flags
  + y站直链:flags:
  + s站直链:flags:
  + k站直链:flags:
  + g站直链:flags:
+ 碧蓝航线模拟建造插件——bot_blhx_build_pool
+ 宝可梦杂交——bot_pokenman（目前下架，维护优先级低）
+ 小鸡词典——bot_jiki（未从原脚本改变为模块:flags:）
+ 管理员模块
  + to be continue

### 上层模块

---

+ 事件处理——church
+ 命令解析器——executor
+ 权限监控——level_manager（用户权限、插件权限等）
+ Bot配置——config.yaml
+ 插件动态导入——dynamic_import（单向被Executor引用）



## event—0926

难点处理流程：业务上层—功能插件—数据库交互插件—数据表设计

### 消息的生命周期

```
发送方 - TX Server - go-cqhttp - mybot
```

`mybot`主要接收`go-cqhttp`上报的事件与消息，通过与上层业务模块或插件模块交互，通过业务流处理消息，从而进行响应动作。

1. 经过`level_manager`对消息进行`filter`

   - 关键字消息过滤(针对特定关键字消息进行过滤)

   - 黑名单消息过滤(针对用户/群组进行过滤)等

     ```mysql
     # 指定群组用户
     SELECT COUNT(1) FROM users WHERE 1 = 1 AND uid={uid} AND gid={gid} AND is_qqBlocked=
     {is_qqBlocked};
     # 指定群组 --> 查群组表
     SELECT COUNT(1) FROM groups WHERE 1 = 1 AND gid={gid} AND is_groupBlocked=
     {is_qqBlocked};
     # 指定用户
     SELECT COUNT(1) FROM users WHERE 1 = 1 AND uid={uid} AND is_qqBlocked=
     {is_qqBlocked};
     ```

     

2. 







### 数据库交互场景

1. 新信息进入时，获取**消息发送方**在数据库中的信息
2. 

- 【Event】[群成员增加](https://docs.go-cqhttp.org/event/#群成员增加)—他人加入
- 【Event】[群成员减少](https://docs.go-cqhttp.org/event/#群成员减少)—踢出群成员、群成员退群
- 【API】获取当前群列表（根据本地配置文件，判断vip群）
- 

### 接口和事件

[go-cqhttp 帮助中心](https://docs.go-cqhttp.org/api)

- 发送私聊消息 send_private_msg
- 发送群消息 send_group_msg
- 撤回消息 delete_msg
- 群组踢人 set_group_kick(通过`获取群成员列表`判断是否成功)（Bot->admin admin command）
- 获取群成员列表 get_group_member_list
- 设置与取消群管理员 set_group_admin（Bot->admin admin command）
- 获取群列表 get_group_list



### 管理员指令

- 测试命令发送 将测试内容回发到原来的会话(默认)

```
测试 + 测试内容
测试 [CQ:image,file=http://baidu.com/1.jpg,type=show,id=40004]
```

- 测试发送

```

```





---



```python
# 用于统计各个增加概率的节点的概率总和和文字输出

a = {"limit":1,"power":2,"prob":3}
the_sum = sum(a.values())
# 6
the_sum_word = "\n".join(["{}: {}".format(k,str(v)) for k,v in a.items()])
# limit: 1\npower: 2\nprob: 3
```
