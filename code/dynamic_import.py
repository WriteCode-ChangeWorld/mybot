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
import sys
import glob
import importlib
sys.path.append("Arsenal")

from Arsenal.basic.bot_tool import tool

class Dynamic_Load:
    def __init__(self):
        self.bot_name = type(self).__name__
        # 需要动态导入的插件 路径表达式
        self.pathname = "Arsenal/bot**.py"
        self.module_dicts = self.import_modules(self.pathname)

    # 从dynamic_load_module中集成过来
    def import_modules(self,
                pathname:str,
                recursive:bool=False,
                start_str:str="Bot",
                reimport:bool=False
        ) -> dict: 
        """
        1. 导入指定路径(pathname)下的模块,返回满足指定条件的类信息
        2. 被导入的插件类必须满足以下几个条件:
            类是用户自定义的
            类名以Bot开头
            类必须包含有bot_name属性(type(self).__name__)
            类必须有一个解析函数parse

        :param pathname: 
            要导入的模块目录的相对路径,只要符合glob路径表达式写法即可
        :param recursive: 
            True则匹配pathname下任何文件和子目录下的文件  
        :param start_str: 
            条件2:返回符合以start_str开头的类
        :param reimport: 
            True为重新导入插件目录下满足条件的类,False则忽略
        :return: 
            模块信息字典
        """
        module_dicts = {}
        module_paths = glob.glob(pathname,recursive=recursive)
        for path in module_paths:
            info = {}
            # Arsenal.bot_dynamic_demo1
            module_name = path.replace(os.sep, '.')[:-3]

            # <module 'Arsenal.bot_dynamic_demo1' from 'D:\\Arsenal\\bot_dynamic_demo1.py'>
            module = importlib.import_module(module_name)
            # 重载
            if reimport:
                module = importlib.reload(module)

            # element此时为str类型
            for element in dir(module):
                # 获取用户自定义类/函数/变量
                # 获取Bot开头的类/函数/变量
                # 获取包含bot_name属性的类
                if not element.startswith('__') and \
                    element.startswith(start_str) and \
                    hasattr(eval("module.{}".format(element)),"bot_name") and \
                    hasattr(eval("module.{}".format(element)),"parse"):
                    # if reimport:
                    #     print("reimport moudle {}".format(element))
                    #     importlib.reload(module)
                    
                    # module_dicts[element] = eval('module.{}'.format(element))
                    # print("import_level: ",eval("module.{}.import_level".format(element)))
                    
                    info[element] = eval('module.{}'.format(element))
                    info["import_level"] = eval("module.{}.import_level".format(element))
                    module_dicts[element] = info


        return module_dicts
 
    def plugin_selector(self,msg):
        if not self.module_dicts:
            return "Not Plug"

        print(self.module_dicts)
        result = ""
        for module_name,module_addr in self.module_dicts.items():
            if hasattr(module_addr[module_name],"parse"):
            # if hasattr(self.module_dicts[module_name],"parse"):
            #     result = module_addr.parse(msg)
                result = module_addr[module_name].parse(msg)
            else:
                print("Warning!The {} is not parse func".format(module_name))
            # try:
            #     result = module_addr.parse(msg)
            # except Exception as e:
            #     print(e)

            # result = eval("{}.parse('{}')".format(module_dicts[module_name],msg))
            if result:
                print("Hit Module: {}".format(module_name))
                return result
        else:
            return "Not Hit Module"
       
    def main(self):
        while True:
            command = input("\nInput the Command or q to Quit: ")
            if command == "q":
                exit()
            elif command == ".reimport":
                self.module_dicts = self.import_modules(self.pathname,reimport=True)
                print(self.module_dicts)
            elif command == "modules":
                print(self.module_dicts)
            else:
                result = self.plugin_selector(command)
                print(result)

if __name__ == "__main__":
    DL = Dynamic_Load()
    DL.main()

    # print(DL.module_dicts)
    # module_dicts = DL.import_modules(DL.pathname,reimport=True)
    # print(module_dicts)