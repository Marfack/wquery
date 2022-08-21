# -*- coding:utf-8 -*-

'''
通过pyinstaller将python项目编译成可执行文件
'''
import os
from query.task_list import *
from common.session_store import store

def main():
    # 执行所有查询任务
    for task in task_list:
        task.start()
    # 主进程等待所有查询任务结束
    for task in task_list:
        task.join()
    # 输出结果
    data.get()
    # 保存会话状态
    store()
    os.system('pause')

if __name__ == '__main__':
    main()
