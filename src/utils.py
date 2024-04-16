import time
import os
from utils_proto import *


def get_format_date_by_timestamp(ts: int):
    time_array = time.localtime(ts)
    format_date = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
    return format_date


def singleton(cls):
    instances = {}

    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return get_instance


def check_or_mkdir(dir: str):
    if os.path.exists(dir):
        return
    try:
        os.mkdir(dir)
    except OSError as e:
        print(f'mkdir error: {e}')
