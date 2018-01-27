# coding=utf-8
import os

import pytesseract
from PIL import Image

import baiduocr
import utils

negate_word = ['没有', '不是', '不会', '不包括', '不属于', '无关', '不可能', '错误']

auxiliary_word = ['下列', '以下', '哪个', '?']


# 分辨是否为答题页面,若是则返回图片对象
def tell_and_get_image(is_auto, black_point, is_ios):
    if is_ios:
        utils.pull_from_screen_ios()
    else:
        utils.pull_from_screen()  # 截图
    backup_img = None
    if os.path.exists('image/backup.png'):
        backup_img = Image.open('image/backup.png')
    else:
        print('image/backup.png位置图片不存在')
        exit(-1)
    if not is_auto:
        return backup_img
    start_x, start_y, end_x, end_y = black_point

    is_answer_page = False
    is_end = False
    for w in range(start_x, end_x, 100):  # 根据颜色判断是否是题目页面
        for h in range(start_y, end_y, 10):
            pixel = backup_img.getpixel((w, h))  # 获取像素点
            r, y, b = pixel[0], pixel[1], pixel[2]
            is_answer_page = 0xfa <= r <= 0xff and 0xfa <= y <= 0xff and 0xfa <= b <= 0xff
            if not is_answer_page:
                is_end = True
                break
        if is_end:
            break
    if is_answer_page:
        return backup_img
    else:
        backup_img.close()
        return None


# 截取题目并文字识别
def image_to_str(image_obj, is_baidu_ocr, client):
    image, name = image_obj
    if is_baidu_ocr and client is not None:
        question, option_arr = baidu_ocr(name, client)
    else:
        question, option_arr = tesseract_orc(image)
    question, is_negative = analyze_question(question)
    return question, option_arr, is_negative


# 使用 tesseract_orc识别
def tesseract_orc(image):
    text = pytesseract.image_to_string(image, lang='chi_sim')
    print('识别的文字是： {}'.format(text))
    return get_question(text)


# 使用百度ocr识别
def baidu_ocr(name, client):
    try:
        text = baiduocr.image_to_str(name, client)
        print('识别的文字是： {}'.format(text))
        return text
    except RuntimeError:
        print('请确保百度OCR配置正确')
        exit(-1)


def get_question(text):
    options = ''
    option_arr = []
    question = ''
    text_arr = text.split('\n\n')
    if len(text_arr) > 0:
        question = text_arr[0]
        question = question.strip()[2:]
        if len(text_arr) > 1:
            for opt in text_arr[1:]:
                options += '\n' + opt
    if options is not None:
        option_arr_o = options.split('\n')
        for op in option_arr_o:
            if op != '' and not op.isspace():
                if op.startswith('《'):
                    op = op[1:]
                if op.endswith('》'):
                    op = op[:-1]
                option_arr.append(op)
                print(op)
    return question, option_arr


# 分析题目，去掉否定词及无关词，得到题目所求答案正反
def analyze_question(question):
    extra_word = negate_word + auxiliary_word
    is_negate = False
    for ele in extra_word:
        if ele in negate_word and ele in question:
            is_negate = True
        if ele in question:
            question = question.replace(ele, '')
    return question, is_negate

#
# def get_result(result_list, option_arr, question, is_negate):
#     answer_num = len(result_list)
#     op_num = len(option_arr)
#     source_arr = []  # 记录各选项得分
#     for i in range(0, op_num):
#         source_arr.append(0)
#     for i in range(0, answer_num):
#         result = result_list[i]
#         for j in range(0, op_num):
#             op = option_arr[j]
#             if op in result:  # 选项在答案中出现一次，加10分
#                 source_arr[j] += 10
#
#     if len(source_arr) == 0 or max(source_arr) == 0:
#         return None
#     if is_negate:
#         best_index = min(source_arr)
#     else:
#         best_index = max(source_arr)
#     best_result = option_arr[source_arr.index(best_index)]
#     for num in source_arr:
#         print(num)
#     return best_result
