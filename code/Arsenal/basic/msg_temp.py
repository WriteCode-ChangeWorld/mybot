# -*- encoding: utf-8 -*-
'''
@File    :   msg_temp.py
@Time    :   2020/09/19 19:54:04
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   模板消息
'''


# ===== basic start =====
# 消息收发
USER_MSG_TEMP = {
    "qqBlocker_user_msg": "[私]收到来自屏蔽用户{}的信息: {}. 已丢弃",
    "qqBlocker_group_msg": "[群]收到群:{} 屏蔽用户{} 的信息: {}. 已丢弃",
    "general_user_msg": "[私]收到用户{} 的消息: {}",
    "general_group_msg": "[群]收到群:{} 用户:{} 的消息: {}",
    "general_unknown_msg": "[unknown]收到群:{} 用户:{} 的消息: {}",
    "limit_user_msg": "[私][level=1]收到用户:{} 的消息: {}",
    "limit_group_msg": "[群][level=1]收到群:{} 用户:{} 的消息: {}"
}


# basic:CQ码
CONFIG_CQ_CODE = {
    "reply_img": "[CQ:image,file={}]",
    "reply_local_img": "[CQ:image,file=file:///{}]",
    "reply_at": "[CQ:at,qq='{}']",
    "reply_audio": "[CQ:record,file={}]",
    "reply_local_audio": "[CQ:record,file=file:///{}]"
}

# basic:bot_tool

# 主动式插件消息未命中解析规则
# 被动式插件跳过解析
PLUGIN_IGNORE = 1

# 主动式插件消息命中解析规则
PLUGIN_BLOCK = 0

TOOL_TEMP = {
    "load_config_success": "MybotConfigLoadSuccess - 配置加载成功",
    "load_config_error": "MybotConfigLoadError - 配置加载异常",
    "debug_status": "DEBUG STATUS: {}",
    "config_path_info": "MybotConfigFilePath - {}",
    "config_info": "MybotConfig - {}",

    # 消息发送 - 群
    "cq_http_send_group_url": "{}/send_group_msg",
    # 消息发送 - 私
    "cq_http_send_private_url": "{}/send_private_msg",
    # 消息发送(合并) - 群
    "cq_seng_group_forward_msg": "{}/send_group_forward_msg",
    # 获取消息
    "cq_get_msg": "{}/get_msg",
    # 撤回消息 - 撤回其他人的群消息需管理员权限
    "cq_delete_msg": "{}/delete_msg",
    # 获取群列表
    "cq_get_group_list": "{}/get_group_list",
    # 获取群信息
    "cq_get_group_info": "{}/get_group_info",
    # 处理加群请求
    "cq_set_group_add_request": "{}/set_group_add_request"
}

# basic:db_pool
DB_TEMP = {
    "db_config_error": "请检查配置文件中Bot.{}的配置是否正确",
    "db_disable": "无法连接数据库,请启动数据库",
    "is_qqBlocked": 0
}

# basic:db_pool
DB_SQL_TEMP = {
    "isExists_sql": "SELECT COUNT(1) FROM {} WHERE {} ",
    "select_sql": "SELECT * FROM {} WHERE {} ",
    "insert_sql": "INSERT INTO {} ({}) VALUES({})",
    "insert_sql_keys_str": """\
        uid, gid, user_level, user_limit_cycle, user_limit_count, 
        user_call_count, magic_thing, is_qqBlocked, create_date, 
        last_call_date, cycle_expiration_time"""
        .replace(" ","").replace("\n",""),
    "update_sql": "UPDATE {} SET {} WHERE {}",
    "delete_sql": "DELETE FROM {} WHERE {}"
}

# basic:db_pool users表默认模板
DB_INSERT_DEFAULT_TEMP = {
    "New_User": {
        "user_id": "",
        "group_id": "",
        "user_level": 10,
        "user_limit_cycle": 10,
        "user_limit_count": 3,
        "user_call_count": 0,
        "magic_thing": 0,
        "is_qqBlocked": 1,
        "create_date": "",
        "last_call_date": "",
        "cycle_expiration_time": ""
    }
}

# basic:task_processor 错误信息模板
TASK_PROCESSOR_TEMP = {
    "TASK_START": "task start",
    "TASK_BREAK_TERMINAL": "task break by <pool.terminal>",
    "TASK_NO_RECORD": "check:TABLE no tasks",
    "TASK_END": "task end. Sleep {}",
    "NULL_VALUE": "<{}> is null value",
    "NOT_DATETIME_DATA": "<{}> is not DATETIME data"
}

# basic:file_handler
# FILEIO_ERROR_INFO = {
#     "loadYamlErrorInfo": "",
#     "YamlPath": ""
# }


# ===== basic end =====


# ===== module start =====
# module:bot_saucenao_img
SEARCH_IMG_MSG = {
    "search_image_enable": "开启搜图",
    "search_image_quit": "关闭搜图",
    "reply_image": "[CQ:at,qq={}]\n搜图模式开启成功!\n请连续发送图片进行搜图吧~\n发送非图片信息自动退出搜图模式!",
    # 观察者对此项进行监控,重复开启则进入限制模式
    "reply_tip": "[CQ:at,qq={}]\n已开启搜图模式,请勿重复开启!",
    "reply_image_quit": "[CQ:at,qq={}]\n搜图模式关闭成功!",
    # 观察者对此项进行监控,重复开启则进入限制模式
    "reply_enable_search": "[CQ:at,qq={}]\n未启用搜图模式!请勿重复关闭!\n(加入黑名单)",
    "reply_bot_quit": "[CQ:at,qq={}]\n检测到发送非图片信息\n搜图模式自动关闭",
}

# module:bot_wahtanime
WHATANIME_MSG = {
    "enbale": "开启搜番"
}
# ===== module end =====


# ===== main start =====
# main:error_code 错误码
MYBOT_ERR_CODE = {
    "Arsenal_Not_Found": "Arsenal目录不存在,请重新检查并创建",
    "Generic_Exception_Info": "Exception : {}"
}

# main:church.identify_data模板
CHURCH_IDENTIFY_MSG = [
    {"code": -100, "description": "识别到心跳包或其他未知原因"},
    {"code": -1, "description": "识别到用户处于黑名单列表,将忽略信息"},
    {"code": 0, "description": "距离下次调用还有{}秒,当前非法调用:{}次"},
    {"code": 1, "description": "识别到用户再次过快调用,请等待20秒再调用"},
    {"code": 10, "description": "识别到用户状态正常"},
    {"code": 200, "description": "识别通过,用户状态正常"}
]

# main:priority 优先级
EXECUTOR_FUNCTION_LIST = [
    {"priority": 500, "function": "SauceNao", "module": ""},
    {"priority": 500, "function": "Ascii2d", "module": ""}
]

# main:executor 
EXECUTOR_TASK_STATUS_INFO = {
    "info": "task_status:<{}> nums:<{}>"
}

# main:level_manager
USER_LIMIT_TEMP = {
    "temp1": "请等待{}秒后再尝试...",
    "temp2": "请不要过快调用,至少等待{}秒后再使用"
}
# ===== main end =====
