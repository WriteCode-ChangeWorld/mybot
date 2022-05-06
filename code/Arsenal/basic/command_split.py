# -*- encoding: utf-8 -*-
'''
@File    :   command_split.py
@Time    :   2022/05/06 15:19:01
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   将群组消息拆解为kw关键词/mode模式/params参数
'''

# here put the import lib


def translate(command:str)->dict:
    """
    :params command: 输入需要解析的命令
    :return: {exp} or {}
    
    :exp:
    {
        "kw": keyword,
        "mode": [mode1, mode2...],
        "params": {
            key1: value1,
            key2: value2,
            key3: value3
        }
    }
    """
    result = {}
    result["kw"] = command.split(" ", 1)[0]
    result["mode_list"] = []
    result["params"] = {}

    command_list = command.split(" ")[1:]
    for _ in command_list:
        if "=" not in _ and "-" in _:
            result["mode_list"].append(_.replace("-", ""))
        
        if "=" in _ and "-" in _:
            k = _.split("-")[-1].split("=")[0]
            v = _.split("=")[-1]
            result["params"][k] = v

    return result
