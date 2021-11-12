## ACG人设插件

---

[TOC]

---

### 开头的话

这个插件是为了满足异世界重生后的人设而起草开始制作的。也没什么好说的，用的是[鬼东西](https://wtf.hiigara.net/)家的API

主角名称：用户名称 + 时间戳（展示仅使用用户名称）





### 模板消息示例



### 1. 小说大纲

**API**(小說大綱生產器)
https://wtf.hiigara.net/t/Lnstjz



### 2-1 称号

**API**(測試你的中二稱號)

https://wtf.hiigara.net/api/run/LwUmQ6/{name}

> `name`：用户昵称 + 时间戳`str(int(time.time()))`

**response**

```json
{
    "text": "唐三1624261453的稱號是破滅使徒",
    "path": "/t/LwUmQ6",
    "ok": true,
    "msg": ""
}
```

**python script**

```python
import requests
import time
import json
import zhconv

url = "https://wtf.hiigara.net/api/run/LwUmQ6/{}"
word = "唐三" + str(int(time.time()))

text = json.loads(requests.get(url.format(word)).text)["text"]
# 繁转简
try:
	text = zhconv.convert(text,"zh-cn")
except:
	text = text
# 赦令骑士团长
```

---

### **2-2 职业**

**API**（你在二次元的職業OAO!）
https://wtf.hiigara.net/t/LuzX6m

---

### 2-3 称号2(不推荐)

**API**(稱號產生器)
https://wtf.hiigara.net/t/titlegen

---

### 2-4 称号3/中二病角色及台词

**API**(中二病的你)
https://wtf.hiigara.net/t/FRC9A

**response**

```json
{
    "text": "吾名唐三。  \n  \n人稱、**虛幻幻殺**。  \n  \n「天空....在為我哭泣。」",
    "path": "/t/FRC9A",
    "ok": true,
    "msg": ""
}
```

**python_script**

```python
text = "吾名唐三。  \n  \n人稱、**虛幻幻殺**。  \n  \n「天空....在為我哭泣。」"
text = text.split("\n",2)[-1]
# 虛幻幻殺
title = text.split("**")[1].split("**")[0]
# 天空....在為我哭泣。
lines = text[::-1].rsplit("「")[0][-1:1:-1]
```

---

### 2-5 称号4

**API**（製作中二稱號專用）
https://wtf.hiigara.net/t/MGIGI

```
测试今天的中二稱號是狂怒天使
```





---

### 3. 故事剧情

**API**(CM's)
https://wtf.hiigara.net/t/PfzcF

**response**

```json
{
    "text": "文創園區  \n中午  \n被車撞因此開發超能力  \n",
    "path": "/t/PfzcF",
    "ok": true,
    "msg": ""
}
```

**python_script**

```python
text = "文創園區  \n中午  \n被車撞因此開發超能力  \n".replace(" ","").split("\n")[:-1]
```

---

### 4. 技能

**API**(你的中二超能)
https://wtf.hiigara.net/t/23fJfX

```json
桜花树下宇焉酱的超能力是腐化接觸到的物體
```

















