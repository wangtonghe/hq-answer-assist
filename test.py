import utils
import os
from PIL import Image
from multiprocessing import Process, Queue, Pool
import wda


# 测试代码
def test_shot(is_ios):
    size = utils.check_os(is_ios)
    pixel_json = utils.get_pixel_config(size)
    blank_area = pixel_json['blank_area']
    question_area = pixel_json['question_area']
    blank_area_point = blank_area['x1'], blank_area['y1'], blank_area['x2'], blank_area['y2']
    question_area_point = question_area['x1'], question_area['y1'], question_area['x2'], question_area['y2']
    backup_img = None
    if os.path.exists('image/backup.png'):
        backup_img = Image.open('image/backup.png')
    else:
        utils.pull_from_screen_ios()
        backup_img = Image.open('image/backup.png')
    utils.crop_image(backup_img, question_area_point, 'image/crop_test.png')
    utils.crop_image(backup_img, blank_area_point, 'image/blank_test.png')


def run_proc(name):
    print('这是子进程{}'.format(name))


def test_process():
    print('process {} start'.format(os.getpid()))
    pool = Pool(2)
    for i in range(2):
        pool.apply_async(run_proc(i))
    pool.close()
    pool.join()
    print('all done')


def test_split():
    text = '蝴蝶的翅膀'
    arr = text.split('的')
    a1, a2 = arr
    print(a1)
    if a1 in '蝴蝶哈哈哈哈':
        print(a1)
    print(arr)


def test_ios_crop():
    c = wda.Client()
    c.screenshot('image/screen.png')
    if os.path.exists('image/screen.png'):
        ios_img = Image.open('image/screen.png')
        width, height = ios_img.size
        print('width:{},height:{}'.format(width, height))


def test_get_pixel():
    size = 1440, 2560
    config = utils.get_pixel_config(size)
    print(config)


if __name__ == '__main__':
    test_get_pixel()
