# coding=utf-8
import json
import os
import subprocess
import urllib.request
import webbrowser
import wda

from PIL import Image

import baiduocr

shot_way = 3

wda_client = None

default_screen_pixel_path = 'config/720x1280.json'

default_width = 720
default_height = 1280


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


def pull_from_screen_ios():
    global wda_client
    if wda_client is None:
        wda_client = wda.Client()
    wda_client.screenshot('image/backup.png')


# 检查运行环境,获取屏幕大小
def check_os(is_ios):
    if is_ios:
        global wda_client
        try:
            if wda_client is None:
                wda_client = wda.Client()
            wda_client.screenshot('image/screen.png')
            ios_img = Image.open('image/screen.png')
            width, height = ios_img.size
            print('width:{},height:{}'.format(width, height))
            size = width, height
            return size
        except Exception:
            print('iOS手机请确保安装WDA')
            exit(0)
    else:
        size_str = os.popen('adb shell wm size').read()
        if not size_str:
            print('Android手机请安装ADB,并打开调试模式')
            exit(-1)
        else:
            size_x_y = size_str.split(':')[1].strip()
            x, y = size_x_y.split('x')
            size = x, y
            return size


# 获取分辨率配置
def get_pixel_config(size):
    width, height = size
    config_path = 'config/{}x{}.json'.format(width, height)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:  # 加载
        with open(default_screen_pixel_path, 'r') as f:
            pixel_config = json.load(f)
            blank_area = pixel_config['blank_area']
            question_area = pixel_config['question_area']
            blank_area['x1'], blank_area['y1'] = get_pixel_by_size((blank_area['x1'], blank_area['y1']), size)
            blank_area['x2'], blank_area['y2'] = get_pixel_by_size((blank_area['x2'], blank_area['y2']), size)
            question_area['x1'], question_area['y1'] = get_pixel_by_size((question_area['x1'], question_area['y1']),
                                                                         size)
            question_area['x2'], question_area['y2'] = get_pixel_by_size((question_area['x2'], question_area['y2']),
                                                                         size)
            return pixel_config


# 截取图片
def crop_image(image, crop_area, image_name):
    start_x, start_y, end_x, end_y = crop_area
    crop_img = image.crop((start_x, start_y, end_x, end_y))
    crop_img.save(image_name)
    crop_img_obj = crop_img, image_name
    return crop_img_obj


def over_add(arr1, arr2):
    length = min(len(arr1), len(arr2))
    arr = []
    for i in range(0, length):
        arr.append(0)
    for i in range(length):
        arr[i] = arr1[i] + arr2[i]
    return arr


def init_baidu_ocr(ocr_config):
    ocr_config_param = ocr_config['app_id'], ocr_config['api_key'], ocr_config[
        'secret_key']
    return baiduocr.init_baidu_ocr(ocr_config_param)


def open_browser(url, question):
    wd = urllib.request.quote(question)
    url = '{}/s?wd={}'.format(url, wd)
    webbrowser.open(url)


# 获取各手机实际像素点
def get_pixel_by_size(old_point, size):
    x, y = old_point
    width, height = size
    new_x = x * width / default_width
    new_y = y * height / default_height
    return int(new_x), int(new_y)
