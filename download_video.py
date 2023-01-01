# -*- coding: utf-8 -*-
# @Time : 2022/12/7 9:37 上午
# @Author : chenxiangan
# @File : download_video.py.py
# @Software: PyCharm
import json
import os
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import requests

from redis_helper import redis_cli
from set_duplicate import SetDuplicate, get_md5
from loguru import logger
set_filter = SetDuplicate()


def read_file(file_name):
    with open(file_name, "r") as fs:
        data = json.loads(fs.read())
    return data


def save_video(each_item,file_name):
    title = each_item.get("desc")
    title = re.sub('[\/:*?"<>|]', '-', title)  # 去掉非法字符
    video_url = each_item.get("video").get("play_addr").get("url_list")[0]
    full_path = os.path.join(file_name, f"{title}.mp4")
    path = f"{file_name}/{title}.mp4"
    md5_title = get_md5(title)
    try:
        if not os.path.exists(full_path) and not set_filter.contains(full_path):
            res = requests.get(video_url)
            code = res.status_code
            logger.info(f"Code:{code},当前下载:{title}")

            content = res.content
            buff_len = len(content)
            redis_cli.hset("douyin_video_hash",md5_title,str(buff_len))
            logger.info(f"size:{int(buff_len/1024/1024)}M")
            if os.path.exists(path):
                return
            with open(path, "wb") as fs:
                fs.write(content)
            set_filter.insert(full_path)
        else:
            file_len = os.path.getsize(path)
            video_buff_len = redis_cli.hget("douyin_video_hash", md5_title)
            if file_len==int(video_buff_len):
                logger.info(f"标题已存在:{title},size:{int(file_len/1024/1024)}M")
            else:
                os.remove(path)
                redis_cli.srem("local_zset_duplicate",get_md5(path))


    except Exception:
        pass


def parse(file_name, data):
    aweme_list = data.get("aweme_list")
    # for each_item in aweme_list:
    logger.info(f"共{len(aweme_list)}条视频")
    with ThreadPoolExecutor(max_workers=3) as excutor:
        excutor.map(partial(save_video, file_name=file_name), aweme_list)


if __name__ == '__main__':
    for i in range(0,2):
        index = "22"
        file_name = f"/Users/chennan/Movies/douyin_video/yuanjun"
        json_path = f"/Users/chennan/pythonproject/douyin_video/json_file/yuanjun/page{index}.json"
        if not os.path.exists(file_name):
            os.makedirs(file_name)

        data = read_file(json_path)
        parse(file_name, data)
        time.sleep(1)
        logger.info("开始检验:===============")

