# coding: utf-8
from os import makedirs
from os.path import dirname, realpath, join, exists
from shutil import copyfile

cur_dir = dirname(realpath(__file__))


def get_file_realpath(file):
    return join(cur_dir, file)


# 检查并创建文件
def check_and_create_file(absolute_file_path):
    if not  exists(absolute_file_path) :
        tmp_dir = dirname(absolute_file_path)
        if not exists(tmp_dir):
            makedirs(tmp_dir)
        with open(absolute_file_path, "w+"):
            pass


# 检查并创建目录
def check_and_create_dir(absolute_dir_path):
    if not  exists(absolute_dir_path) :
        makedirs(absolute_dir_path)


# 复制sqlite配置文件到用户个人目录
def check_and_create_sqlite_file(config_path):
    if not exists(config_path) :
        check_and_create_dir(dirname(config_path))
        copyfile(get_file_realpath("../data/data.db"), config_path)
