import os
import time
from PIL import Image, ImageDraw, ImageFont

def add_test_img(eval_cqp_data):
	person_time = time.localtime()
	hour = str(person_time.tm_hour)
	minutes = str(person_time.tm_min)

	if len(hour) == 1:
		hour = "0" + hour

	if len(minutes) == 1:
		minutes = "0" + minutes

	text_list = [
		{"point": (400,15),"char": hour},
		{"point": (400,50),"char": "点"},
		{"point": (400,85),"char": minutes},
		{"point": (400,120),"char": "分"},
		{"point": (400,155),"char": "了"},
		{"point": (400,190),"char": "!!"},
	]

	# 加载模板图像
	img = Image.open("../res/test.png")
	# 创建绘制对象
	draw = ImageDraw.Draw(img)
	# 载入字体
	ttf_path = "../res/dy.ttf"
	font = ImageFont.truetype(ttf_path,30)
	# 写入文字
	for text in text_list:
		draw.text(text["point"],text["char"],"black",font)
		
	res_path = os.path.join(os.getcwd(),"res")
	report_img_filename = "result-{}{}.png".format(hour,minutes)
	report_img_path = os.path.join(res_path,report_img_filename)
	img.save(report_img_path)
	# img.save("./res/add_text.png")

	reply_group = {
		"group_id": eval_cqp_data['group_id'],
		"message":"[CQ:image,file=file:///{}]".format(report_img_path)
	}
	return reply_group
