## db_tool功能

---

[TOC]

---

### 创建数据库连接池√

`create_tool`

---

### 获取数据库链接√

`get_conn`

---

### 检测记录是否存—isExists_records√

```mysql
SELECT COUNT(1) FROM table WHERE 1 = 1 AND uid = 123456
```

---

### 查找记录—select_records√

```mysql
SELECT * FROM table WHERE uid = 123456 AND gid = 00000 LIMIT 1
```

---

### 更新记录update

update_recordsd_sql

```mysql
sql = "UPDATE {} SET (tag=%s,pageCount=%s,illustType=%s,viewCount=%s,bookmarkCount=%s,likeCount=%s,commentCount=%s,path=%s) WHERE pid=%s"

sql = "UPDATE {} SET ({}) WHERE 1 = 1 "
```



---

### 插入记录insert√

insert_sql

```mysql
INSERT INTO <table> (keys) VALUES(<values>)
```



```ini
1508015265,
835006809,
"1508015265_835006809",
10,
10,
3,
0,
0,
0,
0,
0,
0,
"2021-07-19",
"2021-07-19 15:18:35",
"2021-07-19 15:18:35",
"2021-07-19 15:18:45"
```



---

### 删除记录delete

 delete_records

```mysql
DELETE FROM 表名称 WHERE 删除条件;

# 删除id为2的行
DELETE FROM students WHERE id=2;
# 删除所有年龄小于21岁的数据
DELETE FROM students WHERE age<21;
# 删除表中的所有数据
DELETE FROM students;
```

~~在考虑做不做~~  功能实现后，使用的时候再调整

---

## 使用到数据库的场景

### 预先检查

1. `level_manager`对入方向数据的发送者进行`check_user`，包括：
   
   + 数据库中user表是否有该用户（user_id，group_id共同判定）
     
     + func：isExists_records
     + 无该用户，return False
     + 有该用户，return True
     + 执行sql失败，return False
     + 异常错误，return False
     
   + 判断是否过滤该用户信息，调用`filter_msg`函数去判断
     
     ```mysql
     SELECT COUNT(1) FROM users WHERE 1 = 1 AND uid={uid} AND gid={gid} AND is_qqBlocked={is_qqBlocked};
     ```
     
     + is_qqBlocked为0代表Ture，已拉黑用户，消息忽略；返回`{}`
     + 1则为继续转发消息，Pass跳过；

### 用户的权限进行管理

1. `level_manager`对用户的权限进行管理，包括：
   + 提高权限（永久）
   + 降低权限（永久）
   + 拉黑用户
     + 修改`is_qqBlocked`为0
     + 若已拉黑则返回已拉黑，不操作用户数据
   + 取消拉黑用户
     + 修改`is_qqBlocked`为1
     + 若未拉黑则返回
   + 临时权限

### 黑名单过滤

demo_sql

```mysql
SELECT COUNT(1) FROM users WHERE 1 = 1 AND uid={uid} AND gid={gid} AND is_qqBlocked=0;
```



