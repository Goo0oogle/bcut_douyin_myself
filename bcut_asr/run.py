# -*- coding: utf-8 -*-
# @Time : 2022/12/18 7:42 下午
# @Author : chenxiangan
# @File : run.py.py
# @Software: PyCharm
import glob
from loguru import logger
import os.path
from concurrent.futures import ThreadPoolExecutor

import ffmpeg

from bcut_asr import BcutASR
from bcut_asr.orm import ResultStateEnum


def save_src_file(path, text):
    with open(path, "w") as fs:
        fs.write(text)


def ffmpeg_render(media_file: str) -> bytes:
    '提取视频伴音并转码为aac格式'
    out, err = (ffmpeg
                .input(media_file, v='warning')
                .output('pipe:', ac=1, format='adts')
                .run(capture_stdout=True)
                )
    return out


def run():
    path = "/Users/chennan/Movies/douyin_video/yuanjun/new"
    mp4_list = glob.glob(f"{path}/*.mp4")

    try:
        with ThreadPoolExecutor(max_workers=10) as excutor:
            excutor.map(work, mp4_list)
    except Exception:
        pass
    # for each_item in mp4_list:
    #     try:
    #         work(each_item)
    #     except Exception:
    #         pass


def work(mp4_path):
    logger.info(f"mp4_path:{mp4_path}")
    asr = BcutASR(mp4_path)
    infile_data = ffmpeg_render(mp4_path)
    infile_fmt = "aac"
    asr.set_data(None, raw_data=infile_data, data_fmt=infile_fmt)
    if os.path.exists(mp4_path.replace(".mp4", ".txt")):
        return

    asr.upload()  # 上传文件
    asr.create_task()  # 创建任务

    # 轮询检查结果
    while True:
        result = asr.result()
        # 判断识别成功
        if result.state == ResultStateEnum.COMPLETE:
            break

    # 解析字幕内容
    subtitle = result.parse()
    # 判断是否存在字幕
    if subtitle.has_data():
        # 输出srt格式
        result = subtitle.to_txt()
        save_src_file(mp4_path.replace(".mp4", ".txt"), result)


run()
