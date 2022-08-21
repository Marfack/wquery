# -*- coding:utf-8 -*-

from common.parser import parser
from common.log import *
from common.common_data_dto import CommonDataDTO
from query.query import Query
from query.query_electricity_bill import QueryElectricityBillWorker
from query.query_net_bill import QueryNetBill

# 将所有查询任务集中统计在此处，方便批量处理
task_list: list[Query] = []
# 接收查询任务结果的对象
data = CommonDataDTO()

debug('正在加载服务配置信息...')
try:
    if (parser.get('service-switch', 'electricity-bill') == 'true'):
        task_list.append(QueryElectricityBillWorker(data))
        debug('service [electricity-bill] enabled.')
        
    if (parser.get('service-switch', 'net-bill')) == 'true':
        task_list.append(QueryNetBill(data))
        debug('service [net-bill] enabled.')
except:
    warn(msg='配置文件读取失败', detail='在加载配置文件user-info.ini sections [service-switch] 时出错。将默认打开所有服务继续执行。')
    task_list.append(QueryElectricityBillWorker(data))
    task_list.append(QueryNetBill(data))
