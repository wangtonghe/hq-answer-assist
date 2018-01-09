import os
from PIL import Image
import pytesseract
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup

DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 1280


def main():
    # 720*1280分辨率坐标
    left_top_x = 30
    left_top_y = 200
    right_bottom_x = 680
    right_bottom_y = 380

    # 1. 截图
    # os.system('adb shell screencap -p /sdcard/answer.png')
    # os.system('adb pull /sdcard/answer.png answer.png')

    # 2. 截取题目并文字识别
    image = Image.open('answer.png')
    crop_img = image.crop((left_top_x, left_top_y, right_bottom_x, right_bottom_y))
    crop_img.save('crop.png')
    text = pytesseract.image_to_string(crop_img, lang='chi_sim')
    print(text)

    # 3. 去百度知道搜索
    text = text[2:]  # 把题号去掉
    # text = '一亩地大约是多少平米'
    wd = urllib.request.quote(text)
    url = 'https://zhidao.baidu.com/search?ct=17&pn=0&tn=ikaslist&rn=10&fr=wwwt&word={}'.format(
        wd)
    print(url)
    result = urlopen(url)
    body = BeautifulSoup(result.read(), 'html5lib')
    good_result_div = body.find(class_='list-header').find('dd')
    second_result_div = body.find(class_='list-inner').find(class_='list')
    if good_result_div is not None:
        good_result = good_result_div.get_text()
        print(good_result.strip())

    if second_result_div is not None:
        second_result = second_result_div.find('dl').find('dd').get_text()
        print(second_result.strip())


if __name__ == '__main__':
    main()
