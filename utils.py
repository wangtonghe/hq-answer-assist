# coding=utf-8
import subprocess
import os
import json
from PIL import Image
import baiduocr

shot_way = 3


# 具体截图方法，按优先级排序
def shot_screen():
    global shot_way
    if 1 <= shot_way <= 3:
        process = subprocess.Popen(
            'adb shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_img = process.stdout.read()
        if shot_way == 2:
            binary_img = binary_img.replace(b'\r\n', b'\n')
        elif shot_way == 1:
            binary_img = binary_img.replace(b'\r\r\n', b'\n')
        f = open('image/backup.png', 'wb')
        f.write(binary_img)
        f.close()
    elif shot_way == 0:
        os.system('adb shell screencap -p /sdcard/answer_backup.png')
        os.system('adb pull /sdcard/answer_backup.png image/backup.png')


# 屏幕截图，参考 跳一跳截图方法 https://github.com/wangshub/wechat_jump_game/blob/master/common/screenshot.py
def pull_from_screen():
    global shot_way
    if shot_way < 0:
        print('暂不支持当前设备')
        exit(-1)
    shot_screen()
    try:
        Image.open('image/backup.png').load()
    except Exception:  # 递归调用，直到找到截图方式
        shot_way -= 1
        pull_from_screen()


# 检查adb是否安装,获取屏幕大小
def check_os():
    size_str = os.popen('adb shell wm size').read()
    if not size_str:
        print('请安装ADB,并打开调试模式')
        exit(-1)
    else:
        size_x_y = size_str.split(':')[1].strip()
        x, y = size_x_y.split('x')
        size = x, y
        return size


# 获取分辨率配置文件
def get_pixel_config(size):
    width, height = size
    config_path = 'config/{}x{}.json'.format(width, height)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:  # 加载
        print('请配置对应分辨率')
        exit(-1)


# 截取图片
def crop_image(image, crop_area, image_name):
    start_x, start_y, end_x, end_y = crop_area
    crop_img = image.crop((start_x, start_y, end_x, end_y))
    crop_img.save(image_name)
    crop_img_obj = crop_img, image_name
    return crop_img_obj


def init_baidu_ocr(ocr_config):
    ocr_config_param = ocr_config['app_id'], ocr_config['api_ley'], ocr_config[
        'secret_key']
    return baiduocr.init_baidu_ocr(ocr_config_param)
