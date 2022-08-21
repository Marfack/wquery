from threading import Lock
from time import strftime

# 避免并发输出混乱
lock = Lock()

def info(msg, detail=''):
    with lock:
        print(f'\033[1;34m{strftime("%Y-%m-%d %H:%M:%S")} [INFO ] {msg}\033[0m {detail}')

def debug(msg, detail=''):
    with lock:
        print(f'\033[1;32m{strftime("%Y-%m-%d %H:%M:%S")} [DEBUG] {msg}\033[0m {detail}')

def warn(msg, detail=''):
    with lock:
        print(f'\033[1;33m{strftime("%Y-%m-%d %H:%M:%S")} [WARN ] {msg} {detail}\033[0m')

def error(msg, detail=''):
    with lock:
        print(f'\033[1;31m{strftime("%Y-%m-%d %H:%M:%S")} [ERROR] {msg} {detail}\033[0m')