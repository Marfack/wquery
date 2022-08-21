import os
import sys
from configparser import ConfigParser
from common.log import *

parser = ConfigParser()

try:
    debug('开始解析配置文件...')
    parser.read( 'user-info.ini', encoding='utf8')
    info('解析完成')
except FileNotFoundError:
    error(msg='配置加载失败：', detail='当前目录无法找到文件user-info.ini')
    os.system('pause')
    sys.exit('缺失user-info.ini')
except Exception:
    error(msg='配置加载失败：', detail='请检查配置文件，并保证程序拥有足够权限')
    os.system('pause')
    sys.exit('无法读取user-info.ini')