## dynamic_plugin动态加载模块插件说明文档

[TOC]

---

## 模块函数解析

### 1、func:import_modules

**作用**
动态加载插件的核心所在；导入指定路径下，符合指定条件的插件类（实例化对象）

**关于主动式插件与被动式插件**
两者的区分见第二点`func:plugin_selector`

Q：因为主动式插件完成请求后会返回`PLUGIN_BLOCK`，若被动式插件轮次在前者后边，此时已跳出循环，被动式插件会被忽略；**应确保被动式插件优先级高于主动式插件**
A：插件`__init__`函数中增加`插件加载优先级 import_level`属性；

+ 被动式51~100，主动式1~50，import_level越大越优先导入

+ 可设置相同的import_level，未设置import_level则默认为50，即默认为主动式

  ```python
  try:
      self.import_level
  except AttributeError as e:
      self.import_level = 50
  ```


```python
for x,y in module_dicts.items():
    eval("{}.import_level".format(y))
```







**需要注意的地方**

+ 插件类必须是用户自定义的
+ 插件类变量必须是以Bot开头
+ 插件类包含bot_name属性 -- `type(self).__name__`
+ 插件类包含parse函数

其中parse函数

```python
def parse(self,eval_cqp_data:dict) -> dict:
    """
    每个功能插件主类必须存在一个parse函数
    用于解析cq message是否满足触发条件
    也是这个功能插件类的主流程所在
    
    :param eval_cqp_data:酷Q数据包
    :return: 用于发给机器人的数据包
    类似{"group_id":"123","message":"hi"}
    """
    message = eval_cqp_data["message"]
    # parse函数触发条件
    if "hello" in message:
        bot_result = {
            "group_id":eval_cqp_data["group_id"],
            "message":"[CQ:at,qq={}]\n".format(eval_cqp_data["user_id"]) + 
                        "hi"
        }
        Config.send_group_msg(bot_result)
        # 插件功能逻辑执行完成后
        # 主动式插件回复PLUGIN_BLOCK,跳出动态加载
        # 被动式插件回复PLUGIN_IGNORE,继续下一迭代
        return Config.PLUGIN_BLOCK

    # 以防万一默认返回PLUGIN_IGNORE(继续执行下一插件)
    return Config.PLUGIN_IGNORE
```



---

### 2、func:plugin_selector

**作用**
动态加载插件的转轮，也是消息选择器。

插件与消息选择器之间的关系

1. 插件端为了避免出错未捕获到，默认返回`PLUGIN_IGNORE`；同时dynamic判断None等同于`PLUGIN_IGNORE`
2. **主动式插件（用户主动调用，有触发词）——发送请求后返回`PLUGIN_BLOCK`，无发送请求则返回`PLUGIN_IGNORE`**
3. **被动式插件（无触发词，根据逻辑条件或用户数据触发）——只返回`PLUGIN_IGNORE`；相当于每次有消息进来，都需要过一遍被动式插件（触发概率参考：每日插件0.2+0.5/复读插件0.125，每日插件整体概率仍需调低）**
4. 插件只负责返回`PLUGIN_BLOCK`/`PLUGIN_IGNORE`/`None`，上传go-cq的消息请求插件内部完成；
   消息选择器只负责根据插件返回的status，判断是否要转动到下一个插件（是否要继续循环还是跳出循环）。



### 3、func:main

---

触发：`.reimport`
作用：将所有符合条件的插件类重新导入（插件类导入的模块不会重新导入）

若要重新启动机器人可使用`./reload`命令，命令具体归属哪个模块还在确认。

