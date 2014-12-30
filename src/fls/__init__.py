import os
import sys
import json
import pickle
import cPickle
import logging



JSON = 0
PICKLE = 1
CPICKLE = 2

import data


def struct(**kwargs):
    def new_struct(**update_args):
        kwargs.update(update_args)
        return data.Structure(**kwargs)
    return new_struct


def rangef(start, stop=None, step=1.0):
    if stop is None:
        r_start = 0.0
        r_stop = float(start)
    else:
        r_start = float(start)
        r_stop = float(stop)
    x = r_start
    if r_start > r_stop:
        while x > r_stop:
            yield x
            x += float(step)
    else:
        while x < r_stop:
            yield x
            x += float(step)


def dumps(data_obj, sformat=JSON):
    if sformat is JSON:
        return json.dumps(data_obj)
    if sformat is PICKLE:
        return pickle.dumps(data_obj)
    if sformat is CPICKLE:
        return cPickle.dumps(data_obj)


def dump(data_obj, file_object, sformat=JSON):
    if sformat is JSON:
        json.dump(data_obj, file_object)
    if sformat is PICKLE:
        pickle.dump(data_obj, file_object)
    if sformat is CPICKLE:
        cPickle.dump(data_obj, file_object)


def loads(data_obj, sformat=JSON):
    if sformat is JSON:
        return json.loads(data_obj)
    if sformat is PICKLE:
        return pickle.loads(data_obj)
    if sformat is CPICKLE:
        return cPickle.loads(data_obj)


def load(file_object, sformat=JSON):
    if sformat is JSON:
        return json.load(file_object)
    if sformat is PICKLE:
        return pickle.load(file_object)
    if sformat is CPICKLE:
        return cPickle.load(file_object)


def get_path(file_path):
    return os.path.realpath(os.path.abspath(file_path))


class DataDirectory(object):
    """Object for easy retrieval of file paths."""

    def __init__(self, directory):
        self.DataDir = directory

    def get_file(self, file_name, permissions):
        """Returns a file handle.

        Filename - Relative path
        Permissions - Normal file permissions"""
        return open(get_path(os.path.join(self.DataDir, file_name)), permissions)

    def get_file_path(self, file_name):
        """Returns a file path.

        FileName - Relative file path."""
        return get_path(os.path.join(self.DataDir, file_name))

    def file_exists(self, file_name):
        """Returns true if relative file path exists."""
        return os.path.exists(self.get_file_path(file_name))


user_data = None
cwd = DataDirectory(get_path(os.getcwd()))
app_dir = DataDirectory(get_path(os.path.dirname(get_path(sys.argv[0]))))

USE_USER_DATA = True
NO_USER_DATA = False


def application(app_name, user_data_flag=False, no_log=False):
    root_logger = logging.getLogger()
    log_file_handler = None
    if user_data_flag:
        global user_data
        user_dir = os.path.realpath(os.path.join(
            os.environ["APPDATA"] if os.name == 'nt' else os.environ["HOME"],
            '.' + app_name))
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        user_data = DataDirectory(user_dir)

        log_file_handler = logging.FileHandler(user_data.get_file_path("{name}.log".format(name=app_name)))
    else:
        log_file_handler = logging.FileHandler(cwd.get_file_path("{name}.log".format(name=app_name)))

    log_file_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s: %(message)s')
    log_file_handler.setFormatter(log_formatter)
    if not no_log:
        root_logger.addHandler(log_file_handler)
        root_logger.handlers.pop(0)

