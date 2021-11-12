## saucenao数据示例

basic类型账号支持最大文件为20MB



成功，status = 0

失败

+ 服务器错误，status > 0
+ 客户端错误，status < 0（错误图像、搜索失败）



short_limit为30秒内可进行的搜索的次数，basic账户为6

long_limit为24小时内可进行的搜索的次数，basic账户为200

short_remaining为30秒内剩余搜索的次数

long_remaining为24小时内剩余搜索的次数



### 正常示例

```json
{"header":{"user_id":"35027","account_type":"1","short_limit":"6","long_limit":"200","long_remaining":175,"short_remaining":5,"status":0,"results_requested":16,"index":{"0":{"status":0,"parent_id":0,"id":0,"results":1},"2":{"status":0,"parent_id":2,"id":2,"results":1},"5":{"status":0,"parent_id":5,"id":5,"results":1},"51":{"status":0,"parent_id":5,"id":51,"results":1},"52":{"status":0,"parent_id":5,"id":52,"results":1},"53":{"status":0,"parent_id":5,"id":53,"results":1},"6":{"status":0,"parent_id":6,"id":6,"results":1},"8":{"status":0,"parent_id":8,"id":8,"results":1},"9":{"status":0,"parent_id":9,"id":9,"results":8},"10":{"status":0,"parent_id":10,"id":10,"results":1},"11":{"status":0,"parent_id":11,"id":11,"results":1},"12":{"status":0,"parent_id":9,"id":12,"results":8},"16":{"status":0,"parent_id":16,"id":16,"results":1},"18":{"status":0,"parent_id":18,"id":18,"results":1},"19":{"status":0,"parent_id":19,"id":19,"results":1},"20":{"status":0,"parent_id":20,"id":20,"results":1},"21":{"status":0,"parent_id":21,"id":21,"results":1},"211":{"status":0,"parent_id":21,"id":211,"results":1},"22":{"status":0,"parent_id":22,"id":22,"results":1},"23":{"status":0,"parent_id":23,"id":23,"results":1},"24":{"status":0,"parent_id":24,"id":24,"results":1},"25":{"status":0,"parent_id":9,"id":25,"results":8},"26":{"status":0,"parent_id":9,"id":26,"results":8},"27":{"status":0,"parent_id":9,"id":27,"results":8},"28":{"status":0,"parent_id":9,"id":28,"results":8},"29":{"status":0,"parent_id":9,"id":29,"results":8},"30":{"status":0,"parent_id":9,"id":30,"results":8},"31":{"status":0,"parent_id":31,"id":31,"results":1},"32":{"status":0,"parent_id":32,"id":32,"results":1},"33":{"status":0,"parent_id":33,"id":33,"results":1},"34":{"status":0,"parent_id":34,"id":34,"results":1},"341":{"status":0,"parent_id":341,"id":341,"results":1},"35":{"status":0,"parent_id":35,"id":35,"results":1},"36":{"status":0,"parent_id":36,"id":36,"results":1},"37":{"status":0,"parent_id":37,"id":37,"results":1},"38":{"status":0,"parent_id":38,"id":38,"results":1},"39":{"status":0,"parent_id":39,"id":39,"results":1},"40":{"status":0,"parent_id":40,"id":40,"results":1},"41":{"status":0,"parent_id":41,"id":41,"results":1},"42":{"status":0,"parent_id":42,"id":42,"results":1}},"search_depth":"128","minimum_similarity":51.47,"query_image_display":"userdata\/nK1jUEA4q.jpg.png","query_image":"nK1jUEA4q.jpg","results_returned":16},"results":[{"header":{"similarity":"97.37","thumbnail":"https:\/\/img1.saucenao.com\/res\/pixiv\/8839\/88390726_p0_master1200.jpg?auth=RRjN5MzF9KsI-or0uHv3vQ\u0026exp=1620154800","index_id":5,"index_name":"Index #5: Pixiv Images - 88390726_p0_master1200.jpg","dupes":0},"data":{"ext_urls":["https:\/\/www.pixiv.net\/member_illust.php?mode=medium\u0026illust_id=88390726"],"title":"\u5c01\u5370\u7b26\u6e7f\u5566\uff0c\u8981\u5931\u6548\u4e86\u5462","pixiv_id":88390726,"member_name":"JANLoAd1ng","member_id":26160193}},{"header":{"similarity":"97.85","thumbnail":"https:\/\/img3.saucenao.com\/booru\/7\/2\/7249307f3b53247c5959b1d5f6e39615_1.jpg?auth=nCi6YeV2dfFDvhwAKu423g\u0026exp=1620154800","index_id":12,"index_name":"Index #12: Yande.re - 7249307f3b53247c5959b1d5f6e39615_1.jpg","dupes":0},"data":{"ext_urls":["https:\/\/yande.re\/post\/show\/754981"],"yandere_id":754981,"creator":"janload1ng","material":"genshin impact","characters":"hu tao","source":"https:\/\/i.pximg.net\/img-original\/img\/2021\/03\/12\/15\/28\/12\/88390726"}},{"header":{"similarity":"95.88","thumbnail":"https:\/\/img3.saucenao.com\/booru\/f\/1\/f1ef56a645a3837c684b2518fad87a65_1.jpg?auth=D6ZhpHp14mdQsIZtJqqK1A\u0026exp=1620154800","index_id":12,"index_name":"Index #12: Yande.re - f1ef56a645a3837c684b2518fad87a65_1.jpg","dupes":0},"data":{"ext_urls":["https:\/\/yande.re\/post\/show\/754980"],"yandere_id":754980,"creator":"janload1ng","material":"genshin impact","characters":"hu tao","source":"https:\/\/i.pximg.net\/img-original\/img\/2021\/03\/12\/15\/28\/12\/88390726"}},{"header":{"similarity":"96.7","thumbnail":"https:\/\/img3.saucenao.com\/ehentai\/32\/c5\/32c5f4dd2215e271b160b304c2003d03033790bd.jpg?auth=xwHvwhbXbEUg-RNw5x7zVw\u0026exp=1620154800","index_id":38,"index_name":"Index #38: H-Misc (E-Hentai) - 32c5f4dd2215e271b160b304c2003d03033790bd.jpg","dupes":0},"data":{"source":"Hu Tao","creator":["Unknown"],"eng_name":"Genshin Impact [Character] Hu Tao","jp_name":"\u539f\u795e\u30a4\u30f3\u30d1\u30af\u30c8\u3010\u30ad\u30e3\u30e9\u30af\u30bf\u30fc\u3011\u80e1\u30bf\u30aa"}},{"header":{"similarity":"50.47","thumbnail":"https:\/\/img1.saucenao.com\/res\/pixiv\/2649\/26491025_s.jpg?auth=j2EcmnNge2d1zulHBywTtw\u0026exp=1620154800","index_id":5,"index_name":"Index #5: Pixiv Images - 26491025_s.jpg","dupes":0},"data":{"ext_urls":["https:\/\/www.pixiv.net\/member_illust.php?mode=medium\u0026illust_id=26491025"],"title":"\u3055\u3041","pixiv_id":26491025,"member_name":"\u3053\u592a\u90ce@\u30de\u30a4\u30d4\u30af\u52df\u96c6","member_id":2332700}},{"header":{"similarity":"49.83","thumbnail":"https:\/\/img3.saucenao.com\/dA\/57044\/570443943.jpg?auth=jGY66kYAJp2W4fIiwV6CaQ\u0026exp=1620154800","index_id":34,"index_name":"Index #34: deviantArt - 570443943.jpg","dupes":0},"data":{"ext_urls":["https:\/\/deviantart.com\/view\/570443943"],"title":"060","da_id":"570443943","author_name":"floofyowl","author_url":"http:\/\/floofyowl.deviantart.com"}},{"header":{"similarity":"49.81","thumbnail":"https:\/\/img3.saucenao.com\/furaffinity\/1817\/18175534.jpg?auth=lMe2L-ULeVjrdANqRuFWGg\u0026exp=1620154800","index_id":40,"index_name":"Index #40: FurAffinity - 18175534.jpg","dupes":0},"data":{"ext_urls":["https:\/\/www.furaffinity.net\/view\/18175534"],"title":"109","fa_id":18175534,"author_name":"NovaRaptor","author_url":"https:\/\/www.furaffinity.net\/user\/novaraptor"}},{"header":{"similarity":"49.60","thumbnail":"https:\/\/img1.saucenao.com\/res\/pixiv\/7451\/manga\/74512493_p1.jpg?auth=eXQiujzV08UUEJYeVrx9Fw\u0026exp=1620154800","index_id":5,"index_name":"Index #5: Pixiv Images - 74512493_p1.jpg","dupes":0},"data":{"ext_urls":["https:\/\/www.pixiv.net\/member_illust.php?mode=medium\u0026illust_id=74512493"],"title":"Aether Sage kog!!","pixiv_id":74512493,"member_name":"\u6ce5\u9154","member_id":6445809}},{"header":{"similarity":"49.43","thumbnail":"https:\/\/img3.saucenao.com\/booru\/d\/3\/d3342b25e1663cc3917467b67b29e2f1_4.jpg?auth=NuvZsRYFkRhQXI35KMZpjA\u0026exp=1620154800","index_id":9,"index_name":"Index #9: Danbooru - d3342b25e1663cc3917467b67b29e2f1_0.jpg","dupes":2},"data":{"ext_urls":["https:\/\/danbooru.donmai.us\/post\/show\/1029192","https:\/\/gelbooru.com\/index.php?page=post\u0026s=view\u0026id=1330721","https:\/\/chan.sankakucomplex.com\/post\/show\/1154873"],"danbooru_id":1029192,"gelbooru_id":1330721,"sankaku_id":1154873,"creator":"maguro","material":"fate\/zero, fate\/stay night, fate (series)","characters":"rider (fate\/zero), waver velvet","source":"http:\/\/img03.pixiv.net\/img\/maguro\/22828851_big"}},{"header":{"similarity":"48.7","thumbnail":"https:\/\/img1.saucenao.com\/res\/nhentai\/278358%20%281436336%29%20--%20%5BAZKSB%20%28Tahara%20Anco%29%5D%20Kuroneko%20to%20Shoujo%20%28Puella%20Magi%20Madoka%20Magica%29%20%5BDigital%5D\/44.jpg?auth=b-NaqGXu0lFyZXRf8CuviQ\u0026exp=1620154800","index_id":18,"index_name":"Index #18: H-Misc (nhentai) - 44.jpg","dupes":0},"data":{"source":"Kuroneko to Shoujo","creator":["tahara anco","azksb"],"eng_name":"[AZKSB (Tahara Anco)] Kuroneko to Shoujo (Puella Magi Madoka Magica)","jp_name":"[\u3042\u305a\u304d\u305d\u30fc\u3070\u3002 (\u7530\u539f\u3042\u3093\u3053)] \u9ed2\u732b\u30c8\u5c11\u5973 (\u9b54\u6cd5\u5c11\u5973\u307e\u3069\u304b\u2606\u30de\u30ae\u30ab)"}},{"header":{"similarity":"48.62","thumbnail":"https:\/\/img1.saucenao.com\/res\/drawr\/34\/347433.jpg?auth=U7rqjqLNxsprlGcIWLe7aw\u0026exp=1620154800","index_id":10,"index_name":"Index #10: Drawr Images - 347433.jpg","dupes":0},"data":{"ext_urls":["https:\/\/drawr.net\/show.php?id=347433"],"title":"2009-02-14 12:29:43","drawr_id":347433,"member_name":"\u3064\u3064\u307f","member_id":9365}},{"header":{"similarity":"48.5","thumbnail":"https:\/\/img3.saucenao.com\/booru\/1\/1\/11805e393096f028c3da1d1e1bff0a57_4.jpg?auth=b6voN8K2W8rX3aLTcvlM1g\u0026exp=1620154800","index_id":27,"index_name":"Index #27: Sankaku Channel - 11805e393096f028c3da1d1e1bff0a57_4.jpg","dupes":0},"data":{"ext_urls":["https:\/\/chan.sankakucomplex.com\/post\/show\/783588"],"sankaku_id":783588,"creator":"miyata souji","material":"original","characters":"","source":"http:\/\/homepage3.nifty.com\/~ms\/image\/hyousi.jpg"}},{"header":{"similarity":"48.49","thumbnail":"https:\/\/img1.saucenao.com\/res\/bcy\/illust\/5\/manga\/53202_p3.jpg?auth=1Eiio17HaEPQPXZOkOLxGA\u0026exp=1620154800","index_id":31,"index_name":"Index #31: bcy.net Illust - 53202_p3.jpg","dupes":0},"data":{"ext_urls":["https:\/\/bcy.net\/illust\/detail\/213"],"title":"\u4e1c\u65b9project","bcy_id":53202,"member_name":"\u6c81\u9752","member_id":5283,"member_link_id":213,"bcy_type":"illust"}},{"header":{"similarity":"48.15","thumbnail":"https:\/\/img1.saucenao.com\/res\/mangadex\/152\/152052\/x20.jpg?auth=ZWiWjTdr2AlSehjUT83qeQ\u0026exp=1620154800","index_id":37,"index_name":"Index #37: MangaDex - x20.jpg","dupes":0},"data":{"ext_urls":["https:\/\/mangadex.org\/chapter\/152052\/","https:\/\/www.mangaupdates.com\/series.html?id=34090","https:\/\/myanimelist.net\/manga\/17257\/"],"md_id":152052,"mu_id":34090,"mal_id":17257,"source":"Shounen Maid","part":" - Chapter 16","artist":"Ototachibana","author":"Ototachibana"}},{"header":{"similarity":"47.9","thumbnail":"https:\/\/img1.saucenao.com\/res\/0_magazines\/COMIC%20Penguin%20Club%20Sanzokuban\/140%20%5B2000-09%5D\/172.jpg?auth=EcTefa1dNmNmpP92famD0g\u0026exp=1620154800","index_id":0,"index_name":"Index #0: H-Magazines - 172.jpg","dupes":0},"data":{"title":"COMIC Penguin Club Sanzokuban","part":"vol. 140","date":"2000-09"}},{"header":{"similarity":"47.69","thumbnail":"https:\/\/img1.saucenao.com\/res\/pawoo\/19\/1972436_0.jpg?auth=-CslJrIMcoAdh_wwTOqvYg\u0026exp=1620154800","index_id":35,"index_name":"Index #35: Pawoo.net - 1972436_0.jpg","dupes":0},"data":{"ext_urls":["https:\/\/pawoo.net\/@Onomichi"],"created_at":"2017-04-19T19:04:07.000Z","pawoo_id":1972436,"pawoo_user_acct":"Onomichi","pawoo_user_username":"Onomichi","pawoo_user_display_name":"Onomichi \ud83d\udeb3"}}]}
```





short_remaining——周期搜图次数为0

"status":-2

```json
{"header":{"status":-2,"message":"\u003Cstrong\u003ESearch Rate Too High.\u003C\/strong\u003E\u003Cbr \/\u003E\u003Cbr \/\u003Ecoder_sakura, basic accounts share an IP based usage pool. Your IP (45.87.95.238) has exceeded the basic account type\u0027s rate limit of 6 searches every 30 seconds.\u003Cbr \/\u003EAccount upgrades provide a per-user usage pool, and can be used to increase this limit.\u003Cbr \/\u003E\u003Cbr \/\u003EPlease check the \u003Ca href=\u0027user.php?page=account-upgrades\u0027\u003Eupgrades page\u003C\/a\u003E to find available upgrades."}}
```



不存在的图片 400

"status":-3

```json
{"header":{"user_id":"35027","account_type":"1","short_limit":"6","long_limit":"200","long_remaining":166,"short_remaining":3,"status":-3,"results_requested":16,"message":"Problem with remote server... (400 - http:\/\/gchat.qpic.cn\/gchatpic_new\/2076465138\/1072957655-3116092947-06F0A21181FA6B227FD60?term=3)"}}
```

404

"status":-3

```json
{"header":{"user_id":"35027","account_type":"1","short_limit":"6","long_limit":"200","long_remaining":165,"short_remaining":5,"status":-3,"results_requested":16,"message":"Specified file no longer exists on the remote server!"}}
```

乱七八糟的url "status":-3

```json
{"header":{"user_id":"35027","account_type":"1","short_limit":"6","long_limit":"200","long_remaining":151,"short_remaining":5,"status":-3,"results_requested":16,"message":"Supplied URL is not usable..."}}
```









图片过大，超出当前用户文件最大限制（basic为20MB）

"status":-5

20.7MB：https://danbooru.donmai.us/data/original/e0/eb/__9a_91_girls_frontline_drawn_by_pottsness__e0eb64dd6a250e7cf86a5bf4d195e88e.png

```json
{"header":{"user_id":"35027","account_type":"1","short_limit":"6","long_limit":"200","long_remaining":160,"short_remaining":5,"status":-5,"results_requested":16,"message":"\u003Cstrong\u003E20MB\u003C\/strong\u003E is the maximum file size for your account type. \u003Cbr \/\u003EPlease thumbnail your image."}}
```







---

ascii2d

404图片

不可访问图片

大于5MB的图片

使用香港ip无法使用ascii2d









































