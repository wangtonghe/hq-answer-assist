# coding=utf-8
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Pool
import re
import utils


def search(question, option_arr, is_negative):
    wd = urllib.request.quote(question)
    pool = Pool()
    source_1 = pool.apply_async(search_baidu, args=(wd, option_arr))
    source_2 = pool.apply_async(search_zhidao, args=(wd, option_arr))
    pool.close()
    pool.join()
    s1 = source_1.get()
    s2 = source_2.get()
    print(s1)
    print(s2)
    source_arr = utils.over_add(s1, s2)
    print('分数统计是：{}'.format(source_arr))
    best_answer = get_result(source_arr, option_arr, is_negative)
    return best_answer


# 百度搜索
def search_baidu(question, option_arr):
    result_list = []
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    head = {}
    head['User-Agent'] = user_agent
    url = 'https://www.baidu.com/s?wd={}'.format(question)
    print(url)
    request = urllib.request.Request(url, headers=head)
    result = urlopen(request)
    body = BeautifulSoup(result.read(), 'html5lib')
    content_list = body.find('div', id='content_left')
    content_list = content_list.findAll('div')
    for content in content_list:
        content_text = content.get_text()
        content_text = re.sub('\s', '', content_text)
        result_list.append(content_text)
    answer_num = len(result_list)
    source_arr = []
    op_num = len(option_arr)
    for i in range(0, op_num):
        source_arr.append(0)
    for i in range(0, answer_num):
        result = result_list[i]
        for j in range(0, op_num):
            op = option_arr[j]
            if op in result:  # 选项在答案中出现一次，加10分
                source_arr[j] += 5
    print('百度统计结束')
    return source_arr


# 百度知道搜题
def search_zhidao(question, option_arr):
    result_list = []
    url = 'https://zhidao.baidu.com/search?word={}'.format(
        question)
    print(url)
    result = urlopen(url)
    # 解析页面
    body = BeautifulSoup(result.read(), 'html5lib')
    good_result_div = body.find(class_='list-header').find('dd')
    second_result_div = body.find(class_='list-inner').find(class_='list')
    if good_result_div is not None:
        good_result = good_result_div.get_text()
        result_list.append(good_result)

    if second_result_div is not None:
        second_result_10 = second_result_div.findAll('dl')  # .find(class_='answer').get_text()
        if second_result_10 is not None and len(second_result_10) > 0:
            for each_result in second_result_10:
                result_dd = each_result.get_text()
                result_text = re.sub('\s', '', result_dd)
                result_list.append(result_text)
                print(result_text)
    answer_num = len(result_list)
    source_arr = []
    op_num = len(option_arr)
    for i in range(0, op_num):
        source_arr.append(0)
    for i in range(0, answer_num):
        result = result_list[i]
        for j in range(0, op_num):
            op = option_arr[j]
            if op in result:  # 选项在答案中出现一次，加10分
                source_arr[j] += 10
                if re.search('[答案|结果|而是].{4}' + op, result) is not None:
                    source_arr[j] += 20
    print('百度知道统计结束')
    return source_arr


def get_result(source_arr, option_arr, is_negate):
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
