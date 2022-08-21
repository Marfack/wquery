# -*- coding:utf-8 -*-

import requests
from common.log import *
from common.parser import parser

switch = False
userid = ''
groupid = ''
base_url = ''

try:
    debug('正在加载qq, cqhttp配置信息...')
    switch = parser.get('qq', 'switch') == 'true'
    userid = parser.get('qq', 'userid')
    groupid = parser.get('qq', 'groupid')
    base_url = parser.get('cqhttp', 'base_url')
except:
    error(msg='配置信息读取失败：', detail='读取配置文件user-info.ini出现异常，无法正确获取 sections [qq] [cqhttp] 的部分字段')

def send_msg(msg: str):
    global switch, userid, groupid, base_url
    if not switch:
        return
    debug(msg='启用qq通知', detail='cqhttp使用{}'.format('默认地址' if base_url == '' else base_url))
    if base_url == '':
        error('请填写cqhttp配置', '读取到cqhttp base_url为空，请输入可用的cqhttp地址或者关闭QQ通知功能')
        return
    try:
        if len(userid) > 0:
            debug(f'将消息发送到个人QQ[{userid}]')
            response = requests.get(base_url + '/send_msg', params={
                'user_id': userid,
                'message': msg
            })
            if (response.json()['status'] == 'ok'):
                info(msg=f'个人[{userid}]消息已送达', detail=f'收到响应信息：{response.text}')
            else:
                warn(msg=f'个人[{userid}]消息丢失', detail=f'收到响应信息：{response.text}')
        if len(groupid) > 0:
            debug(f'将消息发送到QQ群[{userid}]')
            response = requests.get(base_url + '/send_msg', params={
                'group_id': groupid,
                'message': msg
            })
            if (response.json()['status'] == 'ok'):
                info(msg=f'群[{groupid}]消息已送达', detail=f'收到响应信息：{response.text}')
            else:
                warn(msg=f'群[{groupid}]消息丢失', detail=f'收到响应信息：{response.text}')
    except Exception:
        error('QQ通知发送失败', f'向cqhttp server: [{base_url}]请求失败，请检查服务器地址是否正确')