# -*- coding:utf-8 -*-

import os
import sys
import hashlib
import requests
import execjs
from lxml import etree
from common.log import *
from common.session_store import *
from common.parser import parser

class HttpSender:
    '''
    Don't use the constructor of this class. Use the singleton sender defined at the bottom instead.
    '''
    def __init__(self):
        self.__body = { 'rsa': '', 'ul': 0, 'pl': 0, 'lt': '', 'execution': '', '_eventId': '' } # 初始化请求体
        self.__login_url = '' # 登录url会重定向到登陆界面，每次重定向form的action会不同
        self.session = requests.Session() # 获取通用session
        self.__username = ''
        self.__password = ''
        self.__init()

    def __init(self):
        '''
        通过简单抓包可以拿到以下登录请求表单的数据项：

        |字段       |解释                                                           |
        |:-         |:-                                                            |
        |rsa|通过des.js中strEnc()加密得到的序列：strEnc(用户名+密码+lt, '1', '2', '3')|
        |ul         |用户名长度                                                     |
        |pl         |密码长度                                                       |
        |lt         |服务端生成的序列                                                |
        |execution  |服务端生成的序列，一般都是e1s1                                   |
        |_eventId   |服务端生成的序列，一般都是submit                                 |

        基本思路为：
        - 通过请求登录页拿到服务端生成的序列
        - 本地数据处理，构建登录所需请求体
        - 通过登录请求拿到Cookie
        '''
        try:
            debug('正在加载账号和密码...')
            # 获取配置文件中的账号密码信息
            self.__username = parser.get('zhlgd', 'username')
            self.__password = parser.get('zhlgd', 'password')
            user_info_hash = parser.get('system', 'user-info-hash')
        except Exception:
            error(msg='获取配置信息失败', detail='识别user-info.ini中section [zhlgd]失败，请检查配置文件。')
            os.system('pause')
            sys.exit('加载智慧理工大配置失败，程序终止')
        if self.__username == '':
            error(msg="请填写配置信息", detail="读取到智慧理工大账号为空，请在配置文件user-info.ini中填写[zhlgd]相关配置")
            os.system('pause')
            sys.exit('缺失账号密码信息，查询终止，请在user-info.ini中配置相关参数')
        new_hash = hashlib.sha256((self.__username + self.__password).encode('utf8')).hexdigest()
        if user_info_hash == new_hash:
            _session = load()
            if _session:
                # 该url在Cookie有效时会返回订单列表，在缺失或Cookie过期时会重定向
                # 通过该请求状态码判断Cookie是否过期
                if _session.get('http://cwsf.whut.edu.cn/queryOrderList', allow_redirects=False).status_code == 200:
                    self.session = _session
                    info('请求状态加载成功')
                    return
                warn('状态已过期，开始重新获取Cookie...')
        else:
            parser.set('system', 'user-info-hash', new_hash)
        self.__get_args()
        self.__build_body()
        self.__login()

    # 请求一次登录，拿到登录表单加密所需的相关字段
    def __get_args(self):
        debug('正在获取服务端序列...')
        url = 'http://cwsf.whut.edu.cn/casLogin'
        response = self.session.request(method='POST', url=url)
        dom = etree.HTML(response.text)
        self.__body['lt'] = dom.xpath(r'//*[@id="lt"]/@value')[0] # 加密辅助字段lt
        self.__body['execution'] = dom.xpath(r'//*[@name="execution"]/@value')[0] # excution
        self.__body['_eventId'] = dom.xpath(r'//*[@name="_eventId"]/@value')[0] # _eventId
        self.__login_url = 'http://zhlgd.whut.edu.cn/' + dom.xpath(r'//*[@id="loginForm"]/@action')[0]

    # 构建请求体
    def __build_body(self):
        # 读取des.js加密库，生成rsa
        js_code = ''
        with open(file='lib/des.js', mode='r', encoding='utf8') as f:
            for line in f:
                js_code += line.strip()
        self.__body['rsa'] = execjs.compile(js_code).call('strEnc', self.__username + self.__password + self.__body['lt'], '1', '2', '3') # 利用与客户端相同的方法加密生成rsa
        self.__body['ul'] = len(self.__username)
        self.__body['pl'] = len(self.__password)

    # 登录，获取Cookie并保存在__session中
    def __login(self):
        debug(msg='正在获取Cookie...', detail=f'请求地址：{self.__login_url}  请求体：{self.__body}')
        # 禁止重定向
        response = self.session.post(url=self.__login_url, data=self.__body, allow_redirects=False)
        # 此处如果登录成功会被重定向，而登录失败则会直接返回200登录失败页面
        if response.status_code == 302: # 登录成功
            # 重定向获取认证信息
            dom = etree.HTML(response.text)
            url = dom.xpath(r'//p/a/@href')[0]
            self.session.get(url)
            JSESSIONID = self.session.cookies.get_dict()['JSESSIONID']
            info(msg='Cookie获取成功.', detail=f'得到Cookie：JSESSIONID={JSESSIONID}')

            # 将hash写入配置文件，由于configParser库写入操作会去掉所有注释，所以自定义写入
            text: list[str] = None
            with open('user-info.ini', 'r', encoding='utf8') as f:
                text = [_ for _ in f if _.strip() != '']
                text[-1] = f'user-info-hash = {parser.get("system", "user-info-hash")}'
            with open('user-info.ini', 'w', encoding='utf8') as f:
                for line in text:
                    f.write(line)
        elif response.status_code == 200: # 登录失败
            error('登录信息有误，请检查账号密码是否正确')
            os.system('pause')
            sys.exit('登录失败，无法继续查询。请检查智慧理工大账号密码是否正确')
        else: # 请求异常
            error(f'Cookie获取失败，异常状态码：[{response.status_code}]，终止执行.')
            os.system('pause')
            sys.exit('请求出现未知异常。')

# 所有请求通过sender发送，避免重复获取Cookie
sender = HttpSender().session
# 初始化完成后保存session
store()