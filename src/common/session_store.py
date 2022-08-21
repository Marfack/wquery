# -*- coding:utf-8 -*-

import pickle
import requests
import common.http_sender as http_sender
from common.log import *

# 将sender持久化到本地，在Cookie有效期内可以避免重复获取Cookie
def store()->None:
    try:
        with open('session.dump', 'wb') as f:
            pickle.dump(http_sender.sender, f)
        info('会话状态已保存')
    except Exception:
        warn('会话状态保存失败')

# 尝试加载上次的session
def load()->requests.Session:
    _session:requests.Session = None
    debug('正在加载上一次请求的状态...')
    try:
        with open('session.dump', 'rb') as f:
            _session = pickle.load(f)
    except Exception:
        warn('未找到已存在的状态记录')
    return _session