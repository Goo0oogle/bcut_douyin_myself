# -*- coding: utf-8 -*-
# @Time : 2023/1/1 7:13 下午
# @Author : chenxiangan
# @File : mp4tomp3.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time : 2022/12/27 4:37 下午
# @Author : chenxiangan
# @File : mp4tomp3.py
# @Software: PyCharm
import click
import ffmpeg


@click.command()
@click.option('-v', '--video_name', required=True, type=str, help='please input video full path')
@click.option('-f', '--format', default='aac', type=str, help='audio format ,support aac or mp3,default is acc')
def main(video_name, format):
    buff = ffmpeg_render(video_name, format)
    if not format.startswith('.'):
        format = f".{format}"
    with open(video_name.replace(".mp4", format), "wb") as fs:
        fs.write(buff)


def ffmpeg_render(media_file: str, audio_format) -> bytes:
    '提取视频伴音并转码为aac格式'
    if audio_format == "aac":
        audio_format = 'adts'
    out, err = (ffmpeg
                .input(media_file, v='warning')
                .output('pipe:', ac=1, format=audio_format)
                .run(capture_stdout=True)
                )
    return out


if __name__ == '__main__':
    main()