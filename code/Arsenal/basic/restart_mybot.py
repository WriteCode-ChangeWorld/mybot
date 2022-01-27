# -*- encoding: utf-8 -*-
'''
@File    :   restart_mybot.py
@Time    :   2022/01/26 23:18:48
@Author  :   Coder-Sakura
@Version :   1.0
@Desc    :   重启mybot
'''

# here put the import lib
import os
import sys

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)