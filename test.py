import utils
import os
from PIL import Image
from multiprocessing import Process, Queue, Pool


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


if __name__ == '__main__':
    test_process()
