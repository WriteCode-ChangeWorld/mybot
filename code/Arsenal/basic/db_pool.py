# -*- encoding: utf-8 -*-
'''
@File    :   db_pool.py
@Time    :   2021/06/23 16:44:57
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
from sys import exec_prefix
import pymysql
import datetime
from DBUtils.PooledDB import PooledDB
# DictCursor,返回结果由tuple转为dict
from pymysql.cursors import DictCursor


from bot_tool import tool
from log_record import logger
from msg_temp import DB_TEMP,DB_SQL_TEMP,DB_INSERT_DEFAULT_TEMP


class db_client:
    def __init__(self):
        self.config_yaml = tool.config
        self.db_type = "mysql"
        self.db_config = self.config_yaml["Bot"].get(self.db_type,"")
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

    # TODO:与select_records合并后移除
    def isExists_records(self,
                cqp_data,
                table="users",
                **kwargs,
        ):
        """
        检测table表中是否有符合kwargs条件的记录
        DBClient.isExists_records(cqp_data,user_id=123,group_id=456)
        :parans cqp_data: CQ端数据包
        :parans table: 指定数据表
        :params kwargs: 查询sql额外的参数组,如:
            {"user_id": 123, "group_id": 456}
        :return: True Or False
        cqp_data={"user_id": 1508015265,"group_id": 835006}
        DBClient.isExists_records(cqp_data,**{"uid": 1508015265,"gid": 835006})
        """
        # 拼接额外参数
        cond = " AND ".join([f"{k} = {v}" for k,v in kwargs.items()])
        # cond = ""
        # for k,v in kwargs.items():
        #     cond += f"AND {k} = {v} "
        if not cond:
            cond = "1 = 1"
            # func_sql += cond

        func_sql = DB_SQL_TEMP["isExists_sql"]
        func_sql = func_sql.format(table,cond)
        logger.debug(f"kwargs - {kwargs}")
        logger.debug(f"cond - {cond}")
        logger.debug(f"func_sql - {func_sql}")

        # conn,cur = self.get_conn()
        # try:
        #     cur.execute(func_sql)
        # except Exception as e:
        #     logger.info(f"Exception - {e}")
        #     logger.info(f"kwargs - {func_sql}")
        #     logger.info(f"func_sql - {func_sql}")
        #     return False
        # else:
        #     res = cur.fetchall()
        #     logger.info(f"res length is {len(res)}")
        #     logger.debug(f"res - {res}")
        # finally:
        #     cur.close()
        #     conn.close()

        # 若记录存在
        # if res[0]["COUNT(1)"] >= 1:
        #     return True
        # else:
        #     return False

    def select_records(self,
                cqp_data=None,
                table="users",
                limit=10,
                **kwargs):
        """
        精确查询,查询符合kwargs字典组条件的记录并返回
        
        :params cqp_data: CQ端数据包
        :params table:    指定数据表
        :params limit:    自定义返回记录数量, limit=-1 ALL return
        :params kwargs:   查询条件,只提供=
            查询条件有字符串需要用引号包括
            {"user_id": 123, "group_id": 456}
        :return: {} or {result}

        DBClient.select_records(table="messages",limit=1,**{"group_name":"测试群组"})
        DBClient.select_records(**{"uid": 1508015265,"gid": 835006})
        """
        # 拼接额外参数
        cond = " AND ".join([f"{k} = {repr(v)}" if isinstance(v,str) else f"{k} = {v}" for k,v in kwargs.items()])
        # cond = ""
        # for k,v in kwargs.items():
        #     cond += f"AND {k} = {v} "
        if not cond:
            cond = "1 = 1"

        func_sql = DB_SQL_TEMP["select_sql"]
        func_sql += f"LIMIT {limit}"
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
            return {}
        else:
            res = cur.fetchall()
            logger.info(f"found {len(res)} recods")
            logger.debug(f"res - {res}")
        finally:
            cur.close()
            conn.close()
        
        # 返回所有查询结果
        if len(res) != 0:
            if limit == -1:
                return res
            else:
                return res[:limit]
        else:
            return []

    def insert_records(self,
            cqp_data,
            table="users",
            **kwargs
        ):
        """
        插入数据
        :parans cqp_data: CQ端数据包
        :parans table: 指定数据表
        :params kwargs: 额外参数
            insert_data 指定插入数据
        :return: True Or False
        DBClient.insert_records(cqp_data={"user_id": 1508015265,"group_id": 835006})
        """
        # 无指定插入数据,使用默认模板插入
        if not kwargs.get("insert_data",""):
            uid = cqp_data["user_id"]
            gid = cqp_data["group_id"]
            user_data = {"uid": uid,"gid": gid}
            user_data.update(DB_INSERT_DEFAULT_TEMP["New_User"])

            now_time = datetime.datetime.now()
            offset = datetime.timedelta(seconds=DB_INSERT_DEFAULT_TEMP["New_User"]["user_limit_cycle"])
            create_date = now_time.strftime('%Y-%m-%d %H:%M:%S')
            last_call_date = create_date
            cycle_expiration_time = (now_time + offset).strftime('%Y-%m-%d %H:%M:%S')

            timestamp_data = {
                "create_date": create_date,
                "last_call_date": last_call_date,
                "cycle_expiration_time": cycle_expiration_time
            }
            user_data.update(timestamp_data)
        else:
            user_data = kwargs["insert_data"]
            
        if isinstance(user_data,dict):
            user_data = tuple(user_data.values())
        else:
            logger.warning(f"<user_data> unlawful. -{user_data}")
            return False

        conn,cur = self.get_conn()
        perch = ",".join(["%s" for i in range(len(DB_SQL_TEMP["insert_sql_keys_str"].split(",")))])
        insert_sql = DB_SQL_TEMP["insert_sql"].format(table,DB_SQL_TEMP["insert_sql_keys_str"],perch)
        logger.debug(f"insert_sql - {insert_sql}")
        logger.debug(f"<user_data> - {user_data}")
        try:
            cur.execute(insert_sql,user_data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.warning(f"records insert fail.")
            logger.debug(f"Exception - {e}")
            logger.info(f"rollback success.")
            return False
        else:
            logger.success(f"records insert success.")
            return True
        finally:
            cur.close()
            conn.close()

    def update_records(self,
            cqp_data=None,
            table="users",
            **kwargs
            ):
        """
        更新数据
        :parans cqp_data: CQ端数据包
        :parans table:    指定数据表
        :parans kwargs:   额外参数
            update_data   更新数据
            judge_data    判断条件,只提供=
            **{"update_data":{...}, "judge_data":{...}}
        :return: True Or False

        DBClient.update_records(**{"update_data":{"user_level":20}, "judge_data":{"uid":1508015265, "gid":835006}})
        """
        # 检测update_data是否存在
        if not kwargs.get("update_data"):
            logger.warning(f"Null Value <update_data>")
            return False

        # 检测judge_data是否存在
        if not kwargs.get("judge_data"):
            logger.warning(f"Null Value <judge_data>")
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
            logger.warning(f"""<user_data> or <judge_data> unlawful.""")
            logger.warning(f"""<user_data> - {kwargs.get("user_data")}""")
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
            logger.info(f"rollback success.")
            return False
        else:
            logger.success(f"records update success.")
            return True
        finally:
            cur.close()
            conn.close()

    def delete_records(self,
            cqp_data=None,
            table="users",
            **kwargs
            ):
        """
        删除数据
        :parans cqp_data: CQ端数据包
        :parans table: 指定数据表
        :parans kwargs: 额外参数
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
            logger.info(f"rollback success.")
            return False
        else:
            logger.success(f"records delete success.")
            return True
        finally:
            cur.close()
            conn.close()

DBClient = db_client()