import os
from PIL import Image
import pytesseract

# 720*1280分辨率坐标下题目及选项区域
body_width_720_start = 30
body_height_1280_start = 200
body_width_720_end = 680
body_height_1280_end = 800

# 720*1280分辨率下此区域是一片白色，以此判断是否是答题页面
judge_width_720_start = 100
judge_width_720_end = 600
judge_height_1280_start = 200
judge_height_1280_end = 250

default_width = 720
default_height = 1280

negate_word = ['没有', '不是', '不会', '不包括', '不属于']

auxiliary_word = ['下列', '以下']

opt_aux_word = ['《', '》']


# 分辨答题页面,若是返回图片对象
def tell_and_get_image():
    os.system('adb shell screencap -p /sdcard/backup.png')
    os.system('adb pull /sdcard/backup.png image/backup.png')
    backup_img = Image.open('image/backup.png')
    start_720_point = judge_width_720_start, judge_height_1280_start
    height_1280_point = judge_width_720_end, judge_height_1280_end
    start_x, start_y = get_pixel_by_size(start_720_point, backup_img.size)
    end_x, end_y = get_pixel_by_size(height_1280_point, backup_img.size)

    is_answer_page = False
    is_end = False
    for w in range(start_x, end_x, 100):  # 根据颜色判断是否是题目页面
        for h in range(start_y, end_y, 10):
            pixel = backup_img.getpixel((w, h))  # 获取像素点
            r, y, b, a = pixel
            is_answer_page = r == 0xff and y == 0xff and b == 0xff
            if not is_answer_page:
                is_end = True
                break
        if is_end:
            break

    if is_answer_page:
        backup_img.save('image/backup.png')
        return backup_img
    else:
        backup_img.close()
        return None


def image_to_str(image):
    # 2. 截取题目并文字识别
    start_720_point = body_width_720_start, body_height_1280_start
    height_1280_point = body_width_720_end, body_height_1280_end
    start_x, start_y = get_pixel_by_size(start_720_point, image.size)
    end_x, end_y = get_pixel_by_size(height_1280_point, image.size)
    crop_img = image.crop((start_x, start_y, end_x, end_y))
    crop_img.save('image/crop.png')
    text = pytesseract.image_to_string(crop_img, lang='chi_sim')
    return text


def get_question(text):
    options = ''
    option_arr = []
    question = ''
    text_arr = text.split('\n\n')
    if len(text_arr) > 0:
        question = text_arr[0]
        question = question.strip()
        if len(text_arr) > 1:
            for opt in text_arr[1:]:
                options += '\n' + opt
    if options is not None:
        option_arr_o = options.split('\n')
        print('原始选项：{}'.format(option_arr_o))
        for op in option_arr_o:
            if op != '' and not op.isspace():
                if op.startswith('《'):
                    op = op[1:]
                if op.endswith('》'):
                    op = op[:-1]
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


# 获取各手机实际像素点
def get_pixel_by_size(area, size):
    x, y = area
    width, height = size
    new_x = x * width / default_width
    new_y = y * height / default_height
    return int(new_x), int(new_y)
