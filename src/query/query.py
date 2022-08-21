# -*- coding:utf-8 -*-

from threading import Thread
from common.log import *
from common.common_data_dto import CommonDataDTO

class Query(Thread):
    '''
    [*] Note: This class is deprecated. It is useless at this version.
        But this class may become the super class of other query class
        like QueryElectronicBillWorker.
    Common query operation in a concurrent condition.
    url: request destination url
    method: GET/POST
    body: the request body in a POST request
    '''
    FACTORY_CODE_VAR_NAME = 'factorycode'

    def __init__(self, dto: CommonDataDTO):
        super(Query, self).__init__()
        self.dto = dto

    def run(self):
        debug(msg='thread: [{}-{}] start.'.format(self.name, self.ident))
        self.query()
        info(msg='thread : [{}-{}] terminated.'.format(self.name, self.ident))
    
    # subclass extends this method to query something
    def query(self):
        pass