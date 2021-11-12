## Mybot 功能插件编写规范

### **目录存放**

+ 功能插件存放在`./code/Arsenal`目录下

+ 功能插件产生的中间或临时文件存放在workspace工作目录下，workspace工作目录支持自定义或向`plus_res_directory`询问

+ 而静态文件或资源存放在`./code/res`目录下

---

### **功能插件命名**

```
bot_report_time.py
```

以bot_xxxx开头，后面写明插件功能（便于动态导入识别）

比如bot_ascii2d_img.py；以bot为前半部分，后半部分为ascii2d_img代表ascii2d搜图模块

---

### **类编写**

```python
# -*- encoding: utf-8 -*-
'''
@File    :   bot_ascii2d_img.py
@Time    :   2021/10/12 15:05:30
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   None
'''

# here put the import lib
# 导入内置库及第三方库
import module

# 导入自定义模块
from your_module import your_func
from config import Config


# 主类命名以模块文件(bot_ascii2d_img.py)后半部分为名,并且首字母大写
class Ascii2d_Img:
    """此处简要写明该类功能
    
    较长的类功能描述
    """
    def __init__(self):
        """初始化工作"""
        # 必须
        self.bot_name = type(self).__name__
        
        # 可选
        # 未定义level,则插件调用权限默认为10,与普通用户权限持平
        self.level = 50
        if not self.level:
            self.level = 10
        
        # 获取该功能插件的res资源目录
        self.module_res_path = pdr.get_plus_res(self.bot_name)
        
    def parse(self,eval_cqp_data:dict) -> dict:
        """
        每个功能插件主类必须存在一个parse函数
        用于解析message和执行插件功能
        
        :param eval_cqp_data:酷Q数据包
        :return: 用于发给机器人的数据包
        类似{"group_id":"123","message":"hi"}
        """
        message = eval_cqp_data["message"]
        # parse函数触发条件
        if "hello" in message:
            bot_result = {
                "group_id":eval_cqp_data["group_id"],·
                "message":"[CQ:at,qq={}]\n".format(eval_cqp_data["user_id"]) + 
                		  "hi"
            }
            Config.send_group_msg(bot_result)
            # 插件功能逻辑执行完成后
            # 主动式插件回复PLUG_SKIP,跳出动态加载
            # 被动式插件回复PLUG_IGNORE,继续下一迭代
            return Config.PLUG_SKIP

        # 以防万一默认返回PLUG_IGNORE(继续执行下一插件)
        return Config.PLUG_IGNORE
    
    def word2dict(self,word:str) -> dict:
        """
        简要注明函数功能
        
        :param word:输入的单词
        :return: 返回生成的单词字典
        """
        if word:
            return {"word":word}
        return {"word":None}
    
# 实例化对象以'Bot_' + 类名来命名
# 动态加载插件通过该特征载入该功能插件类
Bot_Ascii2d_Img = Ascii2d_Img()
```

