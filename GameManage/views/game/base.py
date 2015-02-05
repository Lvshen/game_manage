#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.models.log import Log
import datetime

#处理过滤只修改的值放入集合， 并纪录到 log_param 集合， 返回 只修改的 参数集合 
#@target 目标参数集合,即被修改过的参数集合
#@source 原来的参数集合
#@log_param 要被保存到 日志纪录的集合 
#@dic 参数字典  （用于把参数的英文 名字 转回中文纪录到日志）
#@is_append 是否追加值（一个是覆盖信息，要不就是追加值）//追加值:意思是值在原来值上面加上某个值
def do_filter_modify_param(target, source, log_param, dic, is_append = False):
    request_param = {}  
    append_flag = 'append_'
    for key in target:# 循环提交回来的 player_info JSON
        if is_append and -1 == key.find(append_flag):#如果是追加值情况，key不带 append_ 则忽略
            continue
        
        if target[key] == 'True':
            targetVal = True
        elif target[key] == 'False':
            targetVal = False
        else: 
            tmp_val = target[key]
            if tmp_val == '' or tmp_val == None:
                tmp_val = 0
            try:
                targetVal = float(tmp_val)
            except:
                targetVal = 0
        if is_append:
            key = key.replace(append_flag, '')
        tmp = source.get(key, 'empty_data')
        if tmp == 'empty_data':
            continue
        if is_append and targetVal==0:#追加值情况，追加值为0则不作处理
            continue
        if  targetVal != tmp:
            request_param[key] = targetVal
            cname = dic.get(key, key)#获取参数对应的中文意思
            log_param[cname] = [targetVal, source[key]] #纪录原来的值和被修改的值到日志集合
    return request_param


def write_gm_log(request, data=[]):
    
    #写登录日志
    Log._meta.db_table = 'log_gm'
    log = Log()
    log.log_type = 27
    log.log_server = data[1]
    log.log_channel = data[0]
    
    userid = int(request.session.get('userid', '0'))
    log_user = userid
    
    #如果管理员id 为0则是channel 所操作
    if userid == 0:
        log_user = int(request.session.get('channel_id', '0'))
    
    msg = data[4]
    tmp = msg
    try:
        tmp = tmp.decode('utf-8')
        msg = tmp
    except:
        pass 
     
    msg2 = u''
    msg3 = u''
    msg4 = u''
    msg5 = u''
    msg6 = u'' 
    msg_len = msg.__len__()
    
    msg1 = msg
    if msg_len >= 99:
        msg1 = msg[:99]
        msg2 = msg[99:99+99]
    if msg_len >= 99*2:
        msg3 = msg[99*2:99*3]
    if msg_len >= 99*3:
        msg4 = msg[99*3:99*4]
    if msg_len >= 99*4:
        msg5 = msg[99*4:99*5]
    if msg_len >= 99*5:
        msg6 = msg[99*5:99*6]
    
    log.log_user = log_user
    log.log_data = data[2]
    log.log_result = data[3]
    log.f1 = msg1
    log.f2 = msg2
    log.f3 = msg3
    log.f4 = msg4
    log.f5 = msg5
    log.f6 = msg6
    log.log_time = datetime.datetime.now()
    log.save(using='write')
    
    
