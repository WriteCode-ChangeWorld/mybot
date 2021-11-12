import re
import json
import requests
from lxml import etree

# filePath = "C:\\path\\whateverThisIs.png"
# searchUrl = 'https://yandex.com/images/'
# multipart = {'encoded_image': (filePath, open(
#     filePath, 'rb')), 'image_content': ''}
# # allow_redirects 禁止重定向
# response = requests.post(searchUrl, files=multipart, allow_redirects=False)


"""
cbir_id=1574873%2F2RTpPjqOPRMiJu83pPYMWQ1357&uinfo=sw-1920-sh-1080-ww-1920-wh-937-pd-1-wp-16x9_1920x1080&rpt=imageview&lr=109371&family=yes


https://yandex.com/images/search?family=yes&rpt=imageview&url=https://im0-tub-com.yandex.net/i?id=39ac23213f869e30e5974ad896e7b6a8&n=24&cbir_id=1574873%2F2RTpPjqOPRMiJu83pPYMWQ1357


测试：https://im0-tub-com.yandex.net/i?id=39ac23213f869e30e5974ad896e7b6a8&n=24


https://yandex.ru/images/search?cbir_id=1750078%2FQ7Je-yG6ApwH7NkCB73Caw9438&uinfo=sw-1920-sh-1080-ww-1920-wh-937-pd-1-wp-16x9_1920x1080&rpt=imageview&lr=109371&family=yes
"""

# 参考 https://www.it1352.com/2330402.html
filePath = r"D:\Code\mybot\code\Arsenal\coding\yandex_demo.jpg"
searchUrl = 'https://yandex.com/images/search'
files = {
    'upfile': ('blob', open(filePath, 'rb'), 'image/jpeg')
}
params = {
    'rpt': 'imageview', 
    'format': 'json',
    'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'
}
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "referer":"https://yandex.com/images/",
    "content-type":"multipart/form-data; boundary=----WebKitFormBoundaryAhBIdySP3K1BCxLB"
}


resp = requests.post(searchUrl, headers=headers, params=params, files=files)
# print(json.loads(resp.text))

query_string = json.loads(resp.content)['blocks'][0]['params']['url']
result_url = f"{searchUrl}?{query_string}"
print(result_url)

resp = requests.get(result_url, headers=headers)
obj = etree.HTML(resp.text)

# ======== 包含该图片的文章 ========




# ======== 相似图片 ========
# 取第一个
xpath_selector = """.//div[@class='CbirSimilar-Thumbs CbirSimilar-Thumbs_justified']/div[1]/div[1]/a/div/@style"""
# 取第一个和第二个
# [position()=1 or position()=2]
xpath_selector = """.//div[@class='CbirSimilar-Thumbs CbirSimilar-Thumbs_justified']/div[1]/div[position()=1 or position()=2]/a/div/@style"""
# 取前两个
# [position()<3]
xpath_selector = """.//div[@class='CbirSimilar-Thumbs CbirSimilar-Thumbs_justified']/div[1]/div[position()<3]/a/div/@style"""
# https://blog.csdn.net/qq_39454048/article/details/90598344
text = obj.xpath(xpath_selector)[0]
compile_expression = """.*?:url\("(.*?)"\);.*?"""
img_url = f"http:{re.findall(compile_expression,text)[0]}"