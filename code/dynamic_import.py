# -*- encoding: utf-8 -*-
'''
@File    :   dynamic_import.py
@Time    :   2021/06/21 16:25:18
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
import os
import glob
import importlib

from Arsenal.basic.bot_tool import tool
from Arsenal.basic.log_record import logger
from Arsenal.basic.datetime_tool import datetime_now
from Arsenal.basic.msg_temp import PLUGIN_BLOCK, PLUGIN_IGNORE

class Dynamic_Load:
    """消息 - 插件解析器"""
    
    def __init__(self):
        # 插件路径表达式
        # self.pathname = "Arsenal/bot**.py"
        self.pathname = "Arsenal/bot**/bot**.py"
        # self.module_dicts = self.import_modules(self.pathname)

        self.error_code_list = {
            "NPF": "Not Plugin Found",
            "NHM": "Not Hit Module"
        }

    def import_modules(self,
                pathname:str,
                recursive:bool=False,
                class_start_with:str="Bot",
                reimport:bool=False
        )->list: 
        """导入路径表达式下的模块
            1. 导入指定路径(pathname)下的模块,返回满足指定条件的类信息
            2. 被导入的插件类必须满足以下几个条件:
                类是用户自定义的
                类名以Bot开头
                类必须包含有plugin_name属性(type(self).__name__)
                类必须有一个解析函数parse

            :param pathname: 
                要导入的模块目录的相对路径,只要符合glob路径表达式写法即可
            :param recursive: 
                True则迭代匹配pathname下子目录
            :param start_str: 
                条件2:返回符合以start_str开头的类
            :param reimport: 
                True为重新导入插件目录下满足条件的类,False则忽略
            :return: 
                模块信息字典

            :exp: 重新导入
            import_modules(pathname,reimport=True)
        """
        module_paths = glob.glob(pathname,recursive=recursive)
        logger.debug("<Module> - Start")
        logger.debug(f"<Module Count> - 识别到{len(module_paths)}个符合规则的模块.")
        [logger.debug(f"<Module> - {path}") for path in module_paths]
        logger.debug("<Module> - End")

        module_dicts = {}
        for path in module_paths:
            # Arsenal.bot_dynamic_demo1
            module_name = path.replace(os.sep, '.')[:-3]
            # <module 'Arsenal.bot_dynamic_demo1' from 'D:\\xxx\\bot_dynamic_demo1.py'>
            module = importlib.import_module(module_name)
            logger.debug(f"<Module> - Try To Import {module}")

            # 重载
            if reimport:
                logger.warning(f"<Module> - <{module}> Reimporting!!!")
                module = importlib.reload(module)

            info = {}
            # element -> str
            for element in dir(module):
                if not element.startswith('__') and \
                    element.startswith(class_start_with) and \
                    hasattr(eval("module.{}".format(element)),"plugin_name") and \
                    hasattr(eval("module.{}".format(element)),"parse"):

                    info[element] = eval('module.{}'.format(element))
                    try:
                        info["plugin_level"] = int(eval("module.{}.plugin_level".format(element)))
                    except Exception as e:
                        logger.warning(f"<Plugin> <{eval('element')}> Not Found <plugin_level>. Use Default PluginLevel")
                        # 默认插件权限
                        info["plugin_level"] = 10

                    # 添加插件类型
                    if info["plugin_level"] >= 10:
                        # 主动式插件
                        info["plugin_type"]  = 1
                    elif 1 <= info["plugin_level"] <= 9:
                        # 被动式插件
                        info["plugin_type"] = 0
                    else:
                        info["plugin_type"] = 1

                    info["plugin_name"] = element
                    try:
                        info["plugin_nickname"] = eval("module.{}.plugin_nickname".format(element))
                    except Exception as e:
                        info["plugin_nickname"] = ""

                    logger.success(f"<Plugin> Import Plugin Success - {element}")
                    module_dicts[element] = info
            # else:
            #     logger.debug(f"Module: <{eval('module')}> Cancel Import")

        logger.info(f"<Plugin> Import Plugin Count: {len(module_dicts)}")
        module_dicts = dict(sorted(module_dicts.items(), key=lambda module_dicts:module_dicts[1]["plugin_type"]))
        return module_dicts
 
    def plugin_selector(self,mybot_data):
        """
        消息解析器
        :params mybot_data: mybot消息体
        :return : 
        """
        if not self.module_dicts:
            return self.error_code_list["NPF"]

        # logger.info(self.module_dicts)

        count = 1
        for module_name,module_addr in self.module_dicts.items():
            logger.debug(f"[{count}/{len(self.module_dicts)}][{module_name}] =======")
            result = None
            if hasattr(module_addr[module_name],"parse"):
                try:
                    # 判断群组权限是否大于等于插件权限
                    # 判断用户权限是否大于等于插件权限
                    pass
                    
                    result = module_addr[module_name].parse(mybot_data)
                except Exception as e:
                    logger.debug(f"<Exception> - {e}")
                    # 异常则默认跳过
                    result = PLUGIN_IGNORE
            else:
                logger.warning("module:{} not func:parse.Skip".format(module_name))

            # 未命中解析规则或空值
            if result == PLUGIN_IGNORE:
                logger.debug(f"Miss Hit Module: {module_name} | <result> - PLUGIN_IGNORE")
                count += 1
                continue
            # 解析成功后跳出
            elif result == PLUGIN_BLOCK:
                # TODO 调用机器人成功,更新last_call_date/user_call_count
                # 调用成功才更新last_call_date
                mybot_data["user_info"]["last_call_date"] = datetime_now().strftime('%Y-%m-%d %H:%M:%S')
                # TODO 搜图第一句之类的提示语会消耗次数,待后续调整
                mybot_data["user_info"]["user_call_count"] += 1
                tool.db.update_records(**{
                    "update_data": mybot_data["user_info"], 
                    "judge_data": {"uid": mybot_data["sender"]["user_id"], "gid": mybot_data["sender"]["group_id"]}
                })
                logger.success(f"Hit Module: {module_name} | <result> - PLUGIN_BLOCK")
                count += 1
                break
            # 意料之外的值
            else:
                logger.debug(f"Warning Module: {module_name} | <result> - {result}")
                count += 1
                continue
        else:
            logger.warning(f"Not Hit Any Modules | <mybot_data> - {mybot_data}")
            return self.error_code_list["NHM"]
       
    # TEST for dynamic import
    def main(self):
        self.module_dicts = self.import_modules(self.pathname)
        while True:
            command = input("\nInput the Command or q to Quit: ")
            if command == "q":
                exit()
            elif command == ".reimport":
                self.module_dicts = self.import_modules(self.pathname,reimport=True)
                logger.success(self.module_dicts)
            elif command == "modules":
                logger.success(self.module_dicts)
            else:
                result = self.plugin_selector(command)
                logger.success(result)

modules_dynamicLoad = Dynamic_Load()

# if __name__ == "__main__":
#    modules_dynamicLoad.main()