from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import analyze

DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 1280


def main():
    text = analyze.image_to_str()  # 图片转文字
    question, option_arr, is_negative = analyze.get_question(text)  # 得到题目、选项及题目正反
    # is_negative = False
    # option_arr = ['法国', '美国', '英国']
    # question = '“戛纳国际电影节”在哪一个国家举办的？'
    result_list = []

    wd = urllib.request.quote(question)
    url = 'https://zhidao.baidu.com/search?ct=17&pn=0&tn=ikaslist&rn=10&fr=wwwt&word={}'.format(
        wd)
    print(url)
    result = urlopen(url)
    body = BeautifulSoup(result.read(), 'html5lib')
    good_result_div = body.find(class_='list-header').find('dd')
    second_result_div = body.find(class_='list-inner').find(class_='list')
    if good_result_div is not None:
        good_result = good_result_div.get_text()
        result_list.append(good_result)
        print(good_result.strip())

    if second_result_div is not None:
        second_result_10 = second_result_div.findAll('dl')  # .find(class_='answer').get_text()
        if second_result_10 is not None and len(second_result_10) > 0:
            for index, each_result in enumerate(second_result_10):
                result_dd = each_result.dd.get_text()
                result_list.append(result_dd)
                if index < 3:
                    print(result_dd)

    best_result = analyze.get_result(result_list, option_arr, question, is_negative)
    if best_result is None:
        print('\n没有答案')
    else:
        print('最佳答案是： \033[1;31m{}\033[0m'.format(best_result))


if __name__ == '__main__':
    main()
