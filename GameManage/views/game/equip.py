#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.views.game.base import write_gm_log
from GameManage.http import http_post
from GameManage.cache import center_cache
import json



def equip_info(request, player_id=0,is_read=0):
    req_type = 5
    def_params = {"id":u"装备ID", "rawId":u"装备原型ID", "generalName":u"装配武将", "level":u"装备等级", "attribute":u"属性", "mountlvl": u"战魂等级","pieceNum":u"临时装备删除时间"}
    if player_id ==0:
        player_id = int(request.GET.get('player_id', '0'))
    server_id = int(player_id) >> 20
    
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    
    req_params = 'req_type=%d&player_id=%s&server_id=%d' % (req_type, player_id, server_id)
    list_infos = []
    err_msg = ''
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
        print(game_server_url.GM_PLAYER_URL, req_params, result)
        
        if result['code'] == 0:
            player_info = result['content'][0]['equipList']
            
            for item in player_info:
                item_info = []
                for param in def_params:
                    if item.get(param, None) != None:
                        item_info.append(item.get(param))
                    else:
                        item_info.append('')
                list_infos.append(item_info)
            print(list_infos)    
    except Exception, e:
        err_msg = '发生错误:%s!' % e
    template_str = 'game/equip_info.html'
    
    if is_read == 1:
        template_str = 'game/equip_info_read_only.html'
    
    parg = {}
    parg["player_id"] = player_id
    parg["def_params"] = def_params
    parg["list_infos"] = list_infos
    parg["err_msg"] = err_msg
    
    return render_to_response(template_str, parg)


#装备相关
def equip_add(request, player_id=0):
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
    
    req_type = 111
    result_msgs = {-1:'未知错误', 0:'成功', 1:'增加列表存在不存在的装备ID'}
    result_code = -1
    err_msg = ''
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    
    equip_id = int(request.POST.get('equip_id', '1'))
    equip_level = int(request.POST.get('equip_level', '0'))
    equip_num = int(request.POST.get('equip_num', '1'))
    req_params = 'req_type=%d&player_id=%s&server_id=%d&equip_list=[[%d,%d,%d]]' % (req_type, player_id, server_id, equip_id, equip_level, equip_num)
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
    
        if result['code'] == 0:
            result_code = result['content'][0]
            
        write_gm_log(request, [req_type, server_id, player_id, result_code, '[%d,%d,%d]' % (equip_id, equip_level, equip_num)])
    except Exception, e:
        err_msg = '发生错误:%s!' % e   
    result_msg = result_msgs.get(result_code, '')
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
        
    return render_to_response('game/feedback.html', parg)


def equip_del(request, player_id=0):
    req_type = 112
    result_msgs = {-1:'未知错误', 0:'成功'}
    result_code = -1
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
        
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    equip_id = int(request.GET.get('equip_id', '0'))
    err_msg = ''
    req_params = 'req_type=%d&player_id=%s&server_id=%d&equip_id=%s' % (req_type, player_id, server_id, equip_id)
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
    
        if result['code'] == 0:
            result_code = result['content'][0]
        
        write_gm_log(request, [req_type, server_id, player_id, result_code, equip_id])
    except Exception, e:
        err_msg = '发生错误:%s!' % e
    result_msg = result_msgs.get(result_code, '')
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
    
    return render_to_response('game/feedback.html', parg)

