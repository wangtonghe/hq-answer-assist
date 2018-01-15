import utils
import os
from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime


# 测试代码
def test_shot():
    size = utils.check_os()
    pixel_json = utils.get_pixel_config(size)
    blank_area = pixel_json['blank_area']
    question_area = pixel_json['question_area']
    blank_area_point = blank_area['x1'], blank_area['y1'], blank_area['x2'], blank_area['y2']
    question_area_point = question_area['x1'], question_area['y1'], question_area['x2'], question_area['y2']
    backup_img = None
    if os.path.exists('image/backup.png'):
        backup_img = Image.open('image/backup.png')
    else:
        print('image/backup.png位置图片不存在')
        exit(-1)
    utils.crop_image(backup_img, question_area_point, 'image/crop_test.png')
    utils.crop_image(backup_img, blank_area_point, 'image/blank_test.png')


def test_search():
    start = datetime.datetime.now()
    urls = ['http://www.baidu.com', 'http://www.sina.com', 'http://www.qq.com']
    pool = ThreadPool()
    results = pool.map(urlopen, urls)
    pool.close()
    pool.join()
    end = datetime.datetime.now()
    time = (end - start).microseconds / 1000
    print('耗时{}毫秒'.format(time))
    for result in results:
        body = BeautifulSoup(result.read(), 'html5lib')
        print(body)


if __name__ == '__main__':
    test_search()
