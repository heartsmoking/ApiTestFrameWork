#!/user/bin/env python
#coding=utf-8
'''
@project : bitest
@author  : ZhaoFeng
#@file   : logger.py
#@ide    : PyCharm
#@time   : 2022-01-24 16:00:49
'''
import sys
import logging
from logging import handlers
import os
from typing import Union

from conf.settings import *


#项目绝对路径
curPath = BASE_PATH
level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射
log_level = level_relations.get(LOG_LV, logging.INFO)


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)

class Logger(object):
    def __init__(self,filename=os.path.join(LOG_PATH,"all.log").format(curPath),level=log_level,when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(level)#设置日志级别
        # 设置warning以上的日志输出到stderr
        h1 = logging.StreamHandler(sys.stdout)
        h1.setLevel(logging.DEBUG)
        h1.addFilter(InfoFilter())
        h2 = logging.StreamHandler()
        h2.setLevel(logging.WARNING)
        h1.setFormatter(format_str)
        h2.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')# 往文件里写入
        # 指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        # self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(h1)
        self.logger.addHandler(h2)
        self.logger.addHandler(th)

