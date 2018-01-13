import json
import os
import datetime
import time
import sys
import analyze
import search

"""
主要思路：
1. 答题时使用adb截图并将图片pull到本机
2. 通过ocr图片识别题目
3. 百度题目
4. 百度后结果与选项做匹配，匹配度最高的即为推荐答案

注： 部分题目由于识别或题目本身无法问题，可能搜索不到答案或推荐有误差，需自己根据题目情况进行抉择


"""


# 检查adb是否安装
def check_os():
    size_str = os.popen('adb shell wm size').read()
    if not size_str:
        print('请安装ADB调试工具')
        sys.exit()


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
    pro_start = datetime.datetime.now()
    check_os()
    config = get_config()
    is_auto = config['auto']

    while True:
        while True:
            img = analyze.tell_and_get_image(is_auto)
            if img is not None:
                break
            if is_auto:
                print('没有发现题目页面')
                exit(-1)
            time.sleep(1)  # 不是题目页面，休眠1秒后继续判断
        # 获取题目及选项
        start = datetime.datetime.now()  # 开始时间
        text = analyze.image_to_str(img)  # 图片转文字
        question, option_arr, is_negative = analyze.get_question(text)  # 得到题目、选项及题目正反
        result_list = search.search(question)  # 搜索结果

        best_result = analyze.get_result(result_list, option_arr, question, is_negative)  # 分析结果
        if best_result is None:
            print('\n没有答案')
        else:
            print('最佳答案是： \033[1;31m{}\033[0m'.format(best_result))
        run_time = (datetime.datetime.now() - start).seconds
        print('本次运行时间为：{}秒'.format(run_time))
        if is_auto:
            time.sleep(10)  # 每一道题结束，休息10秒
        else:
            break
    total_time = (datetime.datetime.now() - pro_start).seconds
    print('脚本运行共运行{}秒'.format(total_time))


if __name__ == '__main__':
    main()
