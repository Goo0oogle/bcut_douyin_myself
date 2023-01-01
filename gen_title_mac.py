# -*- coding: utf-8 -*-
# @Time : 2022/12/7 10:18 上午
# @Author : chenxiangan
# @File : gen_title_mac.py
# @Software: PyCharm
import glob
import json
import os
import shutil
import time

name_id_dict = {}


def gen_info_dict():
    with open("/Users/chennan/Movies/Bcut Drafts/draftInfo.json", "r") as fs:
        data = json.loads(fs.read())
    draftInfos = data.get("draftInfos")
    max_time = 0
    for each in draftInfos:
        name = each.get("name")
        id = each.get("id")
        modified = each.get("modifyTime")
        if modified>max_time:
            max_time= modified
            name_id_dict[name] = f"{id}"


def read_srt_json(id_str):
    path = f"/Users/chennan/Movies/Bcut Drafts/{id_str}"
    json_list = glob.glob(f"{path}/*.json")
    json_list = sorted(json_list, key=lambda file: os.path.getmtime(os.path.join(path, file)),reverse=True)

    content_list = []
    srcPath = ""
    for each_item in json_list:
        with open(each_item, "r") as fs:
            track_list = json.loads(fs.read()).get("tracks", [])
            for each_track in track_list:
                trackIndex = each_track.get("trackIndex")
                clips = each_track.get("clips")
                if trackIndex == 1:

                    for clip in clips:
                        content = clip.get("AssetInfo").get("content")
                        content_list.append(content)
                elif trackIndex == 2:
                    clip = clips[0]
                    AssetInfo = clip.get("AssetInfo")
                    srcPath = AssetInfo.get("srcPath").replace(".mp4", ".txt")

        if len(content_list) > 0:
            break


    full_srt = ("\n".join(content_list))
    if full_srt:
        shutil.rmtree(path)
    return srcPath, full_srt


def save_src_file(path, text):
    with open(path, "w") as fs:
        fs.write(text)


if __name__ == '__main__':
    file_name = "3"
    gen_info_dict()
    _id = name_id_dict[file_name]
    print("file_id",_id)
    sr_path, result = read_srt_json(_id)
    print("result",result)

    print("sr_path",sr_path)
    save_src_file(sr_path, result)
