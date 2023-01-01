# -*- coding: utf-8 -*-
# @Time : 2023/1/1 6:46 下午
# @Author : chenxiangan
# @File : read_txt_to_excel.py
# @Software: PyCharm
import glob
import re
from pathlib import Path

import pandas  as pd

info_map={}
def read_file(file_name):
    with open(file_name, "r") as fs:
        data = fs.read()
    return data


def run():
    path = "/Users/chennan/Movies/douyin_video/yuanjun"
    text_list = glob.glob(f"{path}/*.txt")
    for file_path in text_list:
        content=read_file(file_path)
        title=Path(file_path).stem
        title = re.sub('[\/:*?"<>|]', '-', title)  # 去掉非法字符
        info_map[title]=content
    df = pd.DataFrame(info_map,index=[0]).T
    df.to_excel('file.xlsx')


if __name__ == '__main__':
    run()

