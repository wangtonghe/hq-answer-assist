# coding=utf-8
import subprocess
import os
import json
import baiduocr


# 屏幕截图，参考 跳一跳截图方法 https://github.com/wangshub/wechat_jump_game/blob/master/common/screenshot.py
def pull_from_screen():
    process = subprocess.Popen(
        'adb shell screencap -p',
        shell=True, stdout=subprocess.PIPE)
    binary_screenshot = process.stdout.read()
    f = open('image/backup.png', 'wb')
    f.write(binary_screenshot)
    f.close()


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
