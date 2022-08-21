# -*- coding:utf-8 -*-

import os
import sys
from common.http_sender import sender
from common.log import *
from common.parser import parser
from query.query import Query

class QueryElectricityBillWorker(Query):
    '''
    This class is responsible for obtaining dormitory electricity bill information.
    Each instance of this class should be an independent thread to get the infomation.
    '''
    # 查询电力通用请求参数
    FACTORY_CODE = 'E035'
    # 获取楼层的所有寝室
    __QUERY_ROOM_LIST_URL = 'http://cwsf.whut.edu.cn/getRoomInfo'
    # 获取寝室的电表标识符
    __QUERY_ROOM_ELEC_ID_URL = 'http://cwsf.whut.edu.cn/queryRoomElec'
    # 获取电表的数据
    __QUERY_ELEC_BILL_URL = 'http://cwsf.whut.edu.cn/queryReserve'
    __BUILD_ID_VAR_NAME = 'buildid'
    # 接收配置文件中的building，请求所需要的参数
    __build_id = ''
    __FLOOR_ID_VAR_NAME = 'floorid'
    # 接受配置文件中的floor，请求所需要的参数
    __floor_id = ''
    __ROOM_ID_VAR_NAME = 'roomid'
    # 接收配置文件中的room，请求所需要的参数
    __room_id = ''
    __METER_ID_NAME = 'meterId'

    def query(self):
        QueryElectricityBillWorker.__load_info()
        if self.__build_id == '' or self.__floor_id == '' or self.__room_id == '':
            warn(msg='电费查询取消', detail='无法读取寝室信息，请检查user-info.ini，并填写[room]相关配置项')
            return
        debug(msg='thread: [{}-{}] start.'.format(self.name, self.ident))

        # 请求楼层信息
        body = {
            QueryElectricityBillWorker.__BUILD_ID_VAR_NAME: QueryElectricityBillWorker.__build_id,
            QueryElectricityBillWorker.__FLOOR_ID_VAR_NAME: QueryElectricityBillWorker.__floor_id,
            QueryElectricityBillWorker.FACTORY_CODE_VAR_NAME: QueryElectricityBillWorker.FACTORY_CODE
        }
        debug(msg='正在获取楼层信息...', detail='\nPOST {}\nRequest Headers:\n    {}\nRequest Body:\n    {}'
            .format(QueryElectricityBillWorker.__QUERY_ROOM_LIST_URL,
            '\n    '.join([f'{k}: {v}' for k, v in sender.headers.items()]),
            '\n    '.join([f'{k}: {v}' for k, v in body.items()])))
        response = sender.post(url=QueryElectricityBillWorker.__QUERY_ROOM_LIST_URL, data=body)
        if 'roomList' not in response.json():
            warn(msg='电费查询取消', detail=f'请求数据失败：{response.json()["msg"]}。请检查[room]配置信息是否正确')
            return
        # 返回字符串格式为：roomid@楼栋名-房间号，此处将房间号分割出来
        room_list = [_.split('-') for _ in response.json()['roomList']]
        room_no = QueryElectricityBillWorker.__room_id
        for item in room_list:
            if item[1] == QueryElectricityBillWorker.__room_id:
                # 用真正的roomid替换房间号
                room = item[0].split('@')
                QueryElectricityBillWorker.__room_id = room[0]
                room_no = f'{room[1]}-' + room_no
                break

        # 请求寝室信息
        body = {
            QueryElectricityBillWorker.__ROOM_ID_VAR_NAME: QueryElectricityBillWorker.__room_id,
            QueryElectricityBillWorker.FACTORY_CODE_VAR_NAME: QueryElectricityBillWorker.FACTORY_CODE
        }
        debug(msg='正在获取寝室信息...', detail='\nPOST {}\nRequest Headers:\n    {}\nRequest Body:\n    {}'
            .format(QueryElectricityBillWorker.__QUERY_ROOM_ELEC_ID_URL,
            '\n    '.join([f'{k}: {v}' for k, v in sender.headers.items()]),
            '\n    '.join([f'{k}: {v}' for k, v in body.items()])))
        response = sender.post(url=QueryElectricityBillWorker.__QUERY_ROOM_ELEC_ID_URL, data=body)
        if 'meterId' not in response.json():
            warn(msg='电费查询取消', detail=f'请求数据失败：{response.json()["msg"]}。请检查[room]配置信息是否正确')
            return
        meter_id = response.json()['meterId']

        # 请求电表信息
        body = {
            QueryElectricityBillWorker.__METER_ID_NAME: meter_id,
            QueryElectricityBillWorker.FACTORY_CODE_VAR_NAME: QueryElectricityBillWorker.FACTORY_CODE
        }
        debug(msg='正在获取电表信息...', detail='\nPOST {}\nRequest Headers:\n    {}\nRequest Body:\n    {}'
            .format(QueryElectricityBillWorker.__QUERY_ROOM_ELEC_ID_URL,
            '\n    '.join([f'{k}: {v}' for k, v in sender.headers.items()]),
            '\n    '.join([f'{k}: {v}' for k, v in body.items()])))
        response = sender.post(url=QueryElectricityBillWorker.__QUERY_ELEC_BILL_URL, data=body)
        if 'ZVlaue' not in response.json():
            warn(msg='电费查询取消', detail=f'请求数据失败：{response.json()["msg"]}。请检查[room]配置信息是否正确')
            return
        result: dict = response.json()
        self.dto.set_electricity_bill = '寝\u3000\u3000室：{: >9}\n表码示数：{: >11}\n剩余用量：{: >11}\n剩余金额：{: >11}'.format(
            room_no, f'{result["ZVlaue"]} 度', f'{result["remainPower"]} 度', f'{result["meterOverdue"]} 元')
        info(f'电费查询已完成.')
    
    def __load_info():
        try:
            debug('正在加载寝室配置信息...')
            QueryElectricityBillWorker.__build_id = parser.get('room', 'building')
            QueryElectricityBillWorker.__floor_id = parser.get('room', 'floor')
            QueryElectricityBillWorker.__room_id = parser.get('room', 'room')
        except Exception:
            error(msg='配置信息加载失败', detail='识别user-info.ini中section [room]失败，请检查配置文件。')
            os.system('pause')
            sys.exit('配置信息加载失败，请检查user-info.ini')
