# -*- coding:utf-8 -*-

from lxml import etree
from common.http_sender import sender
from common.log import *
from query.query import Query

class QueryNetBill(Query):

    __GET_HTML_URL = 'http://cwsf.whut.edu.cn/netdetails515N023'
    __QUERY_NET_BILL_URL = 'http://cwsf.whut.edu.cn/queryNetAccBalance'
    FACTORY_CODE = 'N023'
    __NET_NO_VAR_NAME = 'netNo'
    __net_no = ''

    def query(self):
        # 请求HTML取得DOM，在DOM上获取net_no
        debug(msg='正在获取DOM...', detail='\nGET {}\nRequest Headers:\n    {}'
            .format(QueryNetBill.__GET_HTML_URL,
            '\n    '.join([f'{k}: {v}' for k, v in sender.headers.items()])))
        response = sender.get(QueryNetBill.__GET_HTML_URL)
        dom = etree.HTML(response.text)
        QueryNetBill.__net_no = dom.xpath(r'//*[@name="netNo"]/@value')[0]
        # 查询网费
        body = {
            QueryNetBill.__NET_NO_VAR_NAME: QueryNetBill.__net_no,
            QueryNetBill.FACTORY_CODE_VAR_NAME: QueryNetBill.FACTORY_CODE
        }
        debug(msg='正在获取网费信息...', detail='\nPOST {}\nRequest Headers:\n    {}\nRequest Body:\n    {}'
            .format(QueryNetBill.__QUERY_NET_BILL_URL,
            '\n    '.join([f'{k}: {v}' for k, v in sender.headers.items()]),
            '\n    '.join([f'{k}: {v}' for k, v in body.items()])))
        response = sender.post(QueryNetBill.__QUERY_NET_BILL_URL, data=body)
        result = response.json()
        self.dto.set_net_bill = '账\u3000\u3000号：{: >10}\n用\u3000\u3000户：{: >7}\n余\u3000\u3000额：{: >9}'.format(
            QueryNetBill.__net_no, result['user_real_name'], f"{result['netaccbal']} 元")
        info(f'网费查询已完成.')
        