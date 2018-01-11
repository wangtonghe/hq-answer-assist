import os
from PIL import Image
import pytesseract

# 720*1280分辨率坐标
left_top_x = 30
left_top_y = 200
right_bottom_x = 680
right_bottom_y = 930

negate_word = ['没有', '不是', '不会', '不']

auxiliary_word = ['下列', '以下']


def image_to_str():
    # 1. 截图
    os.system('adb shell screencap -p /sdcard/answer.png')
    os.system('adb pull /sdcard/answer.png answer.png')

    # 2. 截取题目并文字识别
    image = Image.open('answer.png')
    crop_img = image.crop(
        (left_top_x, left_top_y, right_bottom_x, right_bottom_y))
    crop_img.save('crop.png')
    text = pytesseract.image_to_string(crop_img, lang='chi_sim')
    return text


def get_question(text):
    options = ''
    option_arr = []
    question = ''
    text_arr = text.split('?')
    if len(text_arr) > 0:
        question = text_arr[0]
        question = question.strip()
        if len(text_arr) > 1:
            options = text_arr[1]
    if options is not None:
        option_arr_o = options.split('\n')
        print('原始选项：{}'.format(option_arr_o))
        for op in option_arr_o:
            if op != '' and not op.isspace():
                option_arr.append(op)
                print(op)
    print(question)
    print(option_arr)

    extra_word = negate_word + auxiliary_word
    is_negate = False
    for ele in extra_word:
        if ele in negate_word and ele in question:
            is_negate = True
        if ele in question:
            question = question.replace(ele, '')
    return question, option_arr, is_negate


def get_result(result_list, option_arr, question, is_negate):
    answer_num = len(result_list)
    op_num = len(option_arr)
    source_arr = []  # 记录各选项得分
    for i in range(0, op_num):
        source_arr.append(0)
    for i in range(0, answer_num):
        result = result_list[i]
        for j in range(0, op_num):
            op = option_arr[j]
            if op in result:  # 选项在答案中出现一次，加10分
                source_arr[j] += 10

    if len(source_arr) == 0 or max(source_arr) == 0:
        return None
    if is_negate:
        best_index = min(source_arr)
    else:
        best_index = max(source_arr)
    best_result = option_arr[source_arr.index(best_index)]
    for num in source_arr:
        print(num)
    return best_result
