# -*- encoding: utf-8 -*-
'''
@File    :   db_pool.py
@Time    :   2021/06/23 16:44:57
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import pymysql
import datetime
from DBUtils.PooledDB import PooledDB
# DictCursor,返回结果由tuple转为dict
from pymysql.cursors import DictCursor


from Arsenal.basic.log_record import logger, init_config
from Arsenal.basic.msg_temp import DB_TEMP,DB_SQL_TEMP,DB_INSERT_DEFAULT_TEMP


class db_client:
    def __init__(self):
        self.config = init_config()
        self.db_type = "mysql"
        self.db_config = self.config["Bot"].get(self.db_type,"")
        if not self.db_config:
            logger.error(DB_TEMP["db_config_error"].format(self.db_type))
            exit()

        self.pool = self.create_tool()

    def create_tool(self)->PooledDB:
        """
        创建数据库连接池
        :return: PooledDB
        """
        try:
            pool = PooledDB(
                creator=pymysql,
                maxconnections=16,
                mincached=1,
                maxcached=1,
                blocking=True,
                host=self.db_config["db_host"],
                port=self.db_config["db_port"],
                user=self.db_config["db_user"],
                passwd=self.db_config["db_passwd"],
                db=self.db_config["db_database"],
                charset=self.db_config["db_charset"]
            )
        except pymysql.err.OperationalError as e:
            logger.error(DB_TEMP["db_disable"])
            logger.error(e)
            exit()
        return pool

    def get_conn(self):
        conn = self.pool.connection()
        cur = conn.cursor(DictCursor)
        return conn,cur

    def select_records(self,
            mybot_data=None,
            table="users",
            limit=10,
            **kwargs
            )->list:
        """
        精确查询,查询符合kwargs字典组条件的记录并返回
        
        :params mybot_data: mybot_data内部消息体
        :params table:    指定数据表
        :params limit:    自定义返回记录数量, 0 -> ALL return
        :params kwargs:   指定查询条件
            查询条件有字符串需要用引号包括
            {"user_id": 123, "group_id": 456}
        :return: {} or {result}

        DBClient.select_records(table="messages",limit=1,**{"group_name":"测试群组"})
        """
        # 拼接额外参数
        cond = " AND ".join([f"{k} = {repr(v)}" if isinstance(v,str) else f"{k} = {v}" for k,v in kwargs.items()])
        if not cond:
            cond = "1 = 1"

        func_sql = DB_SQL_TEMP["select_sql"]
        # 0 -> ALL
        if isinstance(limit,int) and int(limit) > 0:
            func_sql += f"LIMIT {limit}"
        elif isinstance(limit,int) and int(limit) < 0:
            limit = 10
            func_sql += f"LIMIT 10"

        func_sql = func_sql.format(table,cond)
        logger.debug(func_sql)

        conn,cur = self.get_conn()
        try:
            cur.execute(func_sql)
        # 执行sql出错
        except Exception as e:
            logger.warning(f"Exception - {e}")
            logger.info(f"func_sql - {func_sql}")
            logger.info(f"kwargs - {kwargs}")
            return []
        else:
            res = cur.fetchall()
            logger.debug(f"found {len(res)} recods")
            logger.debug(f"res - {res}")
        finally:
            cur.close()
            conn.close()
        
        # 返回所有查询结果
        if len(res) != 0:
            if limit == 0:
                return res
            else:
                return res[:limit]
        else:
            return []

    def insert_records(self,
            mybot_data=None,
            table="users",
            **kwargs
            )->dict:
        """
        插入数据
        :params mybot_data: mybot_data内部消息体
        :params table: 指定数据表
        :params kwargs: 
            insert_data -> 指定插入数据,需要按照数据表顺序;
            level -> 指定用户level;
        :return: True Or False
        DBClient.insert_records(mybot_data={"user_id": 123,"group_id": 456})
        DBClient.insert_records(mybot_data={"user_id": 123,"group_id": 456}, **{"user_level":50})
        """
        # 无指定的插入数据,使用默认模板插入
        if not kwargs.get("insert_data",""):
            _data = DB_INSERT_DEFAULT_TEMP["New_User"]
            _data["user_id"] = int(mybot_data["sender"]["user_id"])
            _data["group_id"] = int(mybot_data["sender"]["group_id"])

            now_time = datetime.datetime.now()
            # user_limit_cycle
            user_limit_cycle = int(self.config["Level"]["user_limit"]["seconds"])
            offset = datetime.timedelta(seconds=user_limit_cycle)
            create_date = now_time.strftime('%Y-%m-%d %H:%M:%S')
            last_call_date = create_date
            cycle_expiration_time = (now_time + offset).strftime('%Y-%m-%d %H:%M:%S')

            _data["user_limit_cycle"] = user_limit_cycle
            _data["create_date"] = create_date
            _data["last_call_date"] = last_call_date
            _data["cycle_expiration_time"] = cycle_expiration_time

            if kwargs.get("user_level",""):
                _data["user_level"] = kwargs["user_level"]
        else:
            _data = kwargs["insert_data"]
             
        if isinstance(_data, dict):
            _data = tuple(_data.values())
        else:
            logger.warning(f"<_data> unlawful. -{_data}")
            return {}

        
        if not mybot_data and kwargs.get("insert_data",""):
            sql_keys_str = ",".join(kwargs["insert_data"].keys())
        else:
            sql_keys_str = DB_SQL_TEMP["insert_sql_keys_str"]

        # perch = ",".join(["%s" for i in range(len(DB_SQL_TEMP["insert_sql_keys_str"].split(",")))])
        perch = ",".join(["%s" for i in range(len(sql_keys_str.split(",")))])
        insert_sql = DB_SQL_TEMP["insert_sql"].format(table,sql_keys_str,perch)
        
        logger.debug(f"insert_sql - {insert_sql}")
        logger.debug(f"<_data> - {_data}")
        conn,cur = self.get_conn()
        try:
            cur.execute(insert_sql,_data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.warning(f"records insert fail.")
            logger.debug(f"Exception - {e}")
            logger.debug(f"rollback success.")
            return {}
        else:
            logger.debug(f"records insert success.")
            return _data
        finally:
            cur.close()
            conn.close()

    def update_records(self,
            mybot_data=None,
            table="users",
            **kwargs
            )->bool:
        """
        更新数据
        :params mybot_data: mybot_data内部消息体
        :params table:    指定数据表
        :params kwargs:   额外参数
            update_data   更新后的数据
            judge_data    指定判断条件
            **{"update_data":{...}, "judge_data":{...}}
        :return: True Or False

        DBClient.update_records(**{"update_data":{"user_level":20}, "judge_data":{"uid":1508015265, "gid":835006}})
        """
        # 检测update_data是否存在
        if not kwargs.get("update_data"):
            logger.warning(f"Null Value <update_data> - {kwargs}")
            return False

        # 检测judge_data是否存在
        if not kwargs.get("judge_data"):
            logger.warning(f"Null Value <judge_data> - {kwargs}")
            return False
        
        # 拼接更新数据及条件数据
        update_cond = ",".join([f"{k}=%s" for k,v in kwargs.get("update_data",{}).items()])
        judge_cond = " AND ".join([f"{k}=%s" for k,v in kwargs.get("judge_data",{}).items()])
        update_sql = DB_SQL_TEMP["update_sql"]
        update_sql = update_sql.format(table,update_cond,judge_cond)
        
        if isinstance(kwargs.get("update_data"),dict) and isinstance(kwargs.get("judge_data"),dict):
            update_data = tuple(kwargs.get("update_data").values())
            judge_data = tuple(kwargs.get("judge_data").values())
            update_data = update_data + judge_data
        else:
            logger.warning(f"""<update_data> or <judge_data> unlawful.""")
            logger.warning(f"""<update_data> - {kwargs.get("update_data")}""")
            logger.warning(f"""<judge_data> - {kwargs.get("judge_data")}""")
            return False

        logger.debug(f"<update_sql> - {update_sql}")
        logger.debug(f"<update_data> - {update_data}")
        conn,cur = self.get_conn()
        try:
            cur.execute(update_sql,update_data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.warning(f"records update fail.")
            logger.debug(f"Exception - {e}")
            logger.debug(f"rollback success.")
            return False
        else:
            logger.debug(f"records update success.")
            return True
        finally:
            cur.close()
            conn.close()

    def delete_records(self,
            mybot_data=None,
            table="users",
            **kwargs
            )->bool:
        """
        删除数据
        :params mybot_data: mybot_data内部消息体
        :params table: 指定数据表
        :params kwargs: 额外参数
            judge_data 判断条件,只提供=
        :return: True Or False

        DBClient.delete_records(**{"judge_data":{"create_date": "2021-11-09 16:37:25"}})
        """
        # 检测judge_data是否存在
        if not kwargs.get("judge_data"):
            logger.warning(f"Null Value <judge_data>")
            return False
        
        # 拼接条件
        judge_cond = " AND ".join([f"{k}=%s" for k,v in kwargs.get("judge_data",{}).items()])
        delete_sql = DB_SQL_TEMP["delete_sql"]
        delete_sql = delete_sql.format(table,judge_cond)
        
        if isinstance(kwargs.get("judge_data"),dict):
            judge_data = tuple(kwargs.get("judge_data").values())
        else:
            logger.warning(f"""<judge_data> unlawful.""")
            logger.warning(f"""<judge_data> - {kwargs.get("judge_data")}""")
            return False

        logger.debug(f"<delete_sql> - {delete_sql}")
        logger.debug(f"<judge_data> - {judge_data}")
        conn,cur = self.get_conn()
        try:
            cur.execute(delete_sql,judge_data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.warning(f"records delete fail.")
            logger.debug(f"Exception - {e}")
            logger.debug(f"rollback success.")
            return False
        else:
            logger.debug(f"records delete success.")
            return True
        finally:
            cur.close()
            conn.close()

DBClient = db_client()   