# -*- coding:utf-8 -*-

from common.log import *
from qq_notify.notify import send_msg

class CommonDataDTO():
    '''
    该类用来创造接收查询结果的对象，并提供输出结果的方法。
    '''
    def __init__(self):
        # 电费
        self.__electricity_bill: str = None
        # 网费
        self.__net_bill: str = None
        # extension
    
    @property
    def electricity_bill(self):
        return self.__electricity_bill
    
    @electricity_bill.setter
    def set_electricity_bill(self, val: str):
        self.__electricity_bill = val

    @property
    def net_bill(self):
        return self.__net_bill
    
    @net_bill.setter
    def set_net_bill(self, val: str):
        self.__net_bill = val

    def get(self):
        # 所有已开启服务的查询结果列表
        data_list = []
        if self.electricity_bill:
            data_list.append(f'电费信息：\n{self.electricity_bill}')
        if self.net_bill:
            data_list.append(f'网费信息：\n{self.net_bill}')
        # 控制台输出
        info(msg='\n\a'+'='*10 + '查询结果' + '='*10, detail='\n'.join(['\n\033[1;32m[*]\033[0m ' + data for data in data_list]))
        # qq通知
        send_msg('\n'.join([f'[*]{data}' for data in data_list]))