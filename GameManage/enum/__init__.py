#! /usr/bin/python
# -*- coding: utf-8 -*-
class ENUM_SERVER_STATUS(object):
    #已删除
    DELETED = -1
    #停机
    STOP = 0
    #维护
    MAINTENANCE = 1
    #良好
    NORMAL = 2
    #繁忙
    BUSY = 3
    #爆满
    FULL = 4 
    
class ROLE_TYPE(object):
    #普通账号
    NORMAL = 0 
    #系统管理员
    ROOT = 1
    #专区账号
    ZHUANQU = 2
    #客服账号
    KEFU = 3
    