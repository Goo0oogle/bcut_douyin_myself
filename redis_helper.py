# -*- coding: utf-8 -*-
# @Time : 2022/12/7 2:41 下午
# @Author : chenxiangan
# @File : redis_helper.py
# @Software: PyCharm
from redis import Redis
REDIS_URL = "redis://@localhost:6379"

redis_cli = Redis.from_url(REDIS_URL)


