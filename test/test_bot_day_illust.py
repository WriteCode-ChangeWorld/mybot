# day_illust_process
# 方便复制
from bot_day_illust import Bot_Day_Illust

eval_cqp_data = {"group_id": 1072957655,"user_id":4,"message_type":"group"}
# eval_cqp_data = {"group_id": 1072957655,"user_id":1695210915,"message_type":"group"}
Bot_Day_Illust.day_illust_process(eval_cqp_data)

# day_illust_process
# ========== get_rare_value ==========
from bot_day_illust import Bot_Day_Illust
Bot_Day_Illust.get_rare_value(0.8,limit_prob=0.7)
# ""
Bot_Day_Illust.get_rare_value(0.115,limit_prob=0.7)
# SR
Bot_Day_Illust.get_rare_value(1.115,limit_prob=0.7)
# UR
Bot_Day_Illust.get_rare_value(1.7)
# UR
Bot_Day_Illust.get_rare_value(0.7)
# R
Bot_Day_Illust.get_rare_value(0.2,rare_set={"lost":0.05,"get":0.1,"normal":0.85})
Bot_Day_Illust.get_rare_value(1.2,rare_set={"lost":0.05,"get":0.1,"normal":0.85})

"""
limit prob = 0
pool_rare_set_sum = 1
random = 0.1/1.2

limit prob = 0.7
pool_rare_set_sum = 0.3
random = 0.1/0.8/1.2
"""
# ========== get_rare_value ==========

# ========== get_additional_prob ==========
from bot_day_illust import Bot_Day_Illust
Bot_Day_Illust.get_additional_prob(int("10"))
Bot_Day_Illust.get_additional_prob(int(10))
# ========== get_additional_prob ==========

# ========== safe2pid_error ==========
from bot_day_illust import Bot_Day_Illust
Bot_Day_Illust.safe2pid_error(illust_level="R")
Bot_Day_Illust.safe2pid_error(illust_level="SR")
Bot_Day_Illust.safe2pid_error(illust_level="SSR")
Bot_Day_Illust.safe2pid_error(illust_level="UR")
# ========== safe2pid_error ==========




