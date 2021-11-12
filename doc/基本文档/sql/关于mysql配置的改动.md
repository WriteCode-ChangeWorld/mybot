### 1、mysql 1055错误

**错误原因：**在MySQL5.7之后，sql_mode中默认存在ONLY_FULL_GROUP_BY，SQL语句未通过ONLY_FULL_GROUP_BY语义检查所以报错，会引发1055错误但不影响sql语句的执行。

```mysql
SELECT @@sql_mode;
```

+ 从查询结果中，将`ONLY_FULL_GROUP_BY`去掉，然后复制剩下的值
+ 在mysql配置文件 - sql_mode中粘贴

```mysql
STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
```

