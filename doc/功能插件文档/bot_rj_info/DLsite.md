## RJ号查询功能——dlsite

### 1、指定RJ号查询

#### 脚本请求

```python
import requests,json
url = "https://www.dlsite.com/maniax/product/info/ajax"

# 同时查询多个RJ号为: RJ320374,RJ320864
# 返回结果为{},{},{}...
RJ = "RJ250814"
params = {
    "product_id": RJ
}
headers = {
    "referer": "https://www.dlsite.com",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}
resp = requests.get(url,params=params,headers=headers)
result = json.loads(resp.text)
# 暂时不添加cdn_cache_min=1
# 使用不存在的RJ号则会返回[]
```

#### response

```json
{
    "RJ250814":{
        "site_id":"maniax",
        "site_id_touch":"maniaxtouch",
        "maker_id":"RG18195",
        "affiliate_deny":0,
        "dl_count":"1652",
        "wishlist_count":"2849",
        "dl_format":0,
        "rank":[
            {
                "term":"day",
                "category":"all",
                "rank":18,
                "rank_date":"2019-04-26"
            },
            {
                "term":"week",
                "category":"all",
                "rank":49,
                "rank_date":"2019-04-29"
            },
            {
                "term":"month",
                "category":"all",
                "rank":84,
                "rank_date":"2019-05-23"
            },
            {
                "term":"day",
                "category":"voice",
                "rank":7,
                "rank_date":"2019-04-26"
            },
            {
                "term":"week",
                "category":"voice",
                "rank":15,
                "rank_date":"2019-04-29"
            },
            {
                "term":"month",
                "category":"voice",
                "rank":30,
                "rank_date":"2019-05-11"
            }
        ],
        "rate_average":5,
        "rate_average_2dp":4.73,
        "rate_average_star":50,
        "rate_count":927,
        "rate_count_detail":[
            {
                "review_point":1,
                "count":1,
                "ratio":0
            },
            {
                "review_point":2,
                "count":10,
                "ratio":1
            },
            {
                "review_point":3,
                "count":43,
                "ratio":4
            },
            {
                "review_point":4,
                "count":130,
                "ratio":14
            },
            {
                "review_point":5,
                "count":743,
                "ratio":80
            }
        ],
        "review_count":"14",
        "price":1100,
        "price_without_tax":1000,
        "price_str":"1,100",
        "default_point_rate":10,
        "default_point":100,
        "product_point_rate":null,
        "dlsiteplay_work":true,
        "is_sale":true,
        "on_sale":1,
        "is_discount":false,
        "is_pointup":false,
        "gift":[

        ],
        "is_rental":false,
        "work_rentals":[

        ],
        "upgrade_min_price":110,
        "down_url":"https:\/\/www.dlsite.com\/maniax\/download\/=\/product_id\/RJ250814.html",
        "is_tartget":null,
        "title_id":null,
        "title_name":null,
        "is_title_completed":false,
        "bulkbuy_key":null,
        "bonuses":[

        ],
        "is_limit_work":false,
        "is_sold_out":false,
        "limit_stock":0,
        "is_reserve_work":false,
        "is_reservable":false,
        "is_timesale":false,
        "timesale_stock":0,
        "is_free":false,
        "is_oly":false,
        "is_led":false,
        "work_name":"\u30aa\u30ca\u7981\u59a8\u5bb3\u30dc\u30a4\u30b9 1\u9031\u9593\u30c1\u30e3\u30ec\u30f3\u30b8",
        "work_image":"\/\/img.dlsite.jp\/modpub\/images2\/work\/doujin\/RJ251000\/RJ250814_img_main.jpg",
        "locale_price":{
            "USD":10.09,
            "EUR":8.26,
            "GBP":7.14,
            "TWD":282.05,
            "CNY":64.71,
            "KRW":11340
        },
        "locale_price_str":{
            "USD":"$10.09<i> USD<\/i>",
            "EUR":"8.26",
            "GBP":"7.14",
            "TWD":"<i>NT$<\/i>282.05",
            "CNY":"64.71<i> RMB<\/i>",
            "KRW":"11,340<i> \uc6d0<\/i>"
        },
        "default_point_str":"100"
    }
}
```



#### 信息提取

|        字段         | path                                                      |
| :-----------------: | --------------------------------------------------------- |
|    缩略图 / pic     | "http:" + result[RJ] ["work_image"]                       |
| 名称 / product_name | result[RJ] ["work_name"]                                  |
|     dlsite_url      | https://www.dlsite.com/maniax/work/=/product_id/{RJ}.html |
|      RJ号 / RJ      | list(result.keys()) / result.items()                      |

脚本

```python
# func:parse_product_info
# 单个提取
product_info = {}
# RJ号信息为空
if result == []:
    return product_info

for k,v in result.items():
    product_info["pic"] = "http:" + v["work_image"]
    product_info["product_name"] = v["work_name"]
    product_info["RJ"] = k
    product_info["dlsite_url"] = "https://www.dlsite.com/maniax/work/=/product_id/{}.html".format(k)
```



### 2、关键字查询

个人指定：对象作品不指定，保持默认

API-GJ号查询指定：同人作品、成人漫画、全年龄向、R指定/成人指定、成人向，没有指定美少女游戏

#### 脚本请求

```python
# https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/keyword/搜索关键字在这/order[0]/trend/options[0]/JPN/options[1]/NM/per_page/30/lang_options[0]/%E6%97%A5%E6%9C%AC%E8%AA%9E/lang_options[1]/%E8%A8%80%E8%AA%9E%E4%B8%8D%E5%95%8F
```

```python
import requests
from lxml import etree

keyword = "双子"
search_dl_url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/keyword/搜索关键字在这/order[0]/trend/options[0]/JPN/options[1]/NM/per_page/30/lang_options[0]/%E6%97%A5%E6%9C%AC%E8%AA%9E/lang_options[1]/%E8%A8%80%E8%AA%9E%E4%B8%8D%E5%95%8F".format(keyword)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    "Referer": "https://www.dlsite.com"
}

resp = requests.get(search_dl_url,headers=headers)
obj = etree.HTML(resp.text)
# 一页90个结果
result = obj.xpath("""//ul[@id='search_result_img_box']//li""")
# 根据result进行网页信息提取
```

#### response

```markdown
# 网页html内容不贴
```





