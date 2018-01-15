# coding=utf-8
import json
import os
import datetime
import time
import sys
import analyze
import search
import utils

'''
主要思路：
1. 答题时使用adb截图并将图片pull到本机
2. 通过ocr图片识别题目
3. 百度题目
4. 百度后结果与选项做匹配，匹配度最高的即为推荐答案

注： 部分题目由于识别或题目本身无法问题，可能搜索不到答案或推荐有误差，需自己根据题目情况进行抉择


'''


# 获取配置文件
def get_config():
    config_file = 'config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        print('请检查根目录下是否存在配置文件 config.json')
        exit(-1)


def main():
    size = utils.check_os()
    config = get_config()
    is_auto = config['auto']
    is_baidu_ocr = config['baidu_ocr']
    is_debug = config['debug']
    baidu_ocr_clint = None
    if is_baidu_ocr:
        baidu_cor_config = config['baidu_ocr_config']
        baidu_ocr_clint = utils.init_baidu_ocr(baidu_cor_config)
    pixel_json = utils.get_pixel_config(size)
    blank_area = pixel_json['blank_area']
    question_area = pixel_json['question_area']

    blank_area_point = blank_area['x1'], blank_area['y1'], blank_area['x2'], blank_area['y2']
    question_area_point = question_area['x1'], question_area['y1'], question_area['x2'], question_area['y2']

    question_num = 0
    crop_img_name = 'image/crop.png'

    while True:
        while True:
            img = analyze.tell_and_get_image(is_auto, blank_area_point)
            if img is not None:
                question_num += 1
                break
            else:  # 若不是答题页
                if not is_auto:
                    print('没有发现题目页面')
                    exit(-1)
                print('没有发现答题页面，继续')
                time.sleep(0.8)  # 不是题目页面，休眠0.8秒后继续判断

        # 获取题目及选项
        start = datetime.datetime.now()  # 记录开始时间
        crop_obj = utils.crop_image(img, question_area_point, crop_img_name)
        question, option_arr, is_negative = analyze.image_to_str(crop_obj, is_baidu_ocr, baidu_ocr_clint)  # 图片转文字
        if question is None or question == '':
            print('\n没有识别题目')
            exit(-1)
        result_list = search.search(question)  # 搜索结果

        best_result = search.get_result(result_list, option_arr, question, is_negative)  # 分析结果
        if best_result is None:
            print('\n没有答案')
        else:
            print('最佳答案是： \033[1;31m{}\033[0m'.format(best_result))
        run_time = (datetime.datetime.now() - start).seconds
        print('本次运行时间为：{}秒'.format(run_time))
        crop_img = crop_obj[0]
        if is_debug:
            crop_img.save('image/question_{}.png'.format(question_num))
        crop_img.close()
        img.close()
        if is_auto:
            time.sleep(10)  # 每一道题结束，休息10秒
        else:
            break


if __name__ == '__main__':
    main()
