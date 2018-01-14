# coding=utf-8
from aip import AipOcr


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def image_to_str(name, client):
    image = get_file_content(name)
    text_result = client.basicGeneral(image)
    print(text_result)
    result = get_question_and_options(text_result)
    return result


def init_baidu_ocr(baidu_ocr_config):
    app_id, api_ley, secret_key = baidu_ocr_config
    client = AipOcr(app_id, api_ley, secret_key)
    return client


# {'words_result': [{'words': '11.代表作之一是《蒙娜丽莎的眼'},
#                   {'words': '泪》的歌手是?'}, {'words': '林志颖'},
#                   {'words': '林志炫'}, {'words': '林志玲'}],
#  'log_id': 916087026228727188, 'words_result_num': 5}

def get_question_and_options(text):
    if 'error_code' in text:
        print('请确保百度OCR配置正确')
        exit(-1)
    if text['words_result_num'] == 0:
        return None
    result_arr = text['words_result']
    ques = result_arr[:2]
    ques_str = ''
    option_arr = []
    for word in ques:
        ques_str += word['words']
    options = result_arr[2:]
    for opt in options:
        option_arr.append(opt['words'])
    ques_str = ques_str[2:]  # 去掉题号
    print(ques_str)
    print(option_arr)
    return ques_str, option_arr
