#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.views.game.base import write_gm_log
from GameManage.views.base import  UserStateManager
from GameManage.cache import center_cache
from django.http import HttpResponse
from GameManage.http import http_post
import json


def info(request):
    player_id = int(get_value(request, 'player_id', 0, int))
    
    err_msg = ''
    hunshi = 0
    zhanhun_list = []
    
    if 0 == player_id:
        err_msg = '请输入角色ID'
        
    if '' == err_msg:
        result = get_data(player_id, 8)
        
        if None == result:
            err_msg = '请刷新再试'
        else:
            data = result.get('data', [])
            if 0 != data.__len__():
                hunshi = data[0]
                for index in range(1 , data.__len__()):
                    zhanhun_list.append(data[index])
    
    parg = {}
    parg['err_msg'] = err_msg
    parg['hunshi'] = hunshi
    parg['zhanhun_list']  = zhanhun_list
    parg['player_id'] = player_id
    
    return render_to_response('game/battle_heart.html', parg)


def post(request):
    player_id = get_value(request, 'player_id', 0, int)
    
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_type = 141 
    
    data = []
    
    append_hunshi = get_value(request, 'append_hunshi', None, int)
    if None != append_hunshi:
        data.append(append_hunshi)
    else:
        data.append(0)
        
    for index in range(1, 21):
        #1 到  20
        append_value = get_value(request, 'append_zhanhun_%s' % index, None, int)
        if None != append_value: 
            data.append(append_value)
        else:
            data.append(0)
             
  
    try:
        request_param = json.dumps({"data" : data})
        
        req_params = 'req_type=%d&player_id=%s&server_id=%d&modify_battle_heart_info=%s' % (req_type, player_id, server_id, request_param)
        print req_params
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10) 
        result = json.loads(result)
        print result
    except Exception, ex:
        print ex
        return HttpResponse(ex)
    
        
    usm = None
    try:
        usm = UserStateManager(request)
        
        write_gm_log(request, [req_type, server_id, player_id, result['code'], request_param]) #写日志，保存到数据库
        
    except Exception, ex:
        operate_id = -1
        operate_id = usm.get_the_user().id
        
        print '<<views game battle_heart.py>> write_log error, operate admin id :%s , player_id:%s '% (operate_id. player_id)
        print ex
        pass
    
    if result['code'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse('失败')
     
     
def get_data(player_id, req_type):
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_params = 'req_type=%d&player_id=%s&server_id=%d' % (req_type, player_id, server_id)
    result = None
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=20)
        result = json.loads(result)
        if result['code'] == 0:
            result = result['content'][0]
    except:
        pass
    
    return result

def get_value(request, name, default = '', value_type = str):
    result = request.GET.get(name, request.POST.get(name, default))
    
    if None == default and None == result:
        return None
    try:
        result = value_type(result)
    except:
        return default
    return result
