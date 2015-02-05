#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.views.game.base import write_gm_log 
from GameManage.cache import center_cache
from GameManage.http import http_post
import json



def army_info(request, player_id=0, is_read=0):
    req_type = 2
    def_params = {"rid":u"武将RAWID", "ia":u"是否在野", "glv":u"武将等级 ", "rnl":u"转生需求等级", "exp":u"武将当前经验 ", "slv":u"士兵星级 ", "scn":u"当前士兵数", "smn":u"默认最大士兵数", "aa":u"武将培养增加值", "ee":u"武将身上的装备", "ha":u"武将体力加成"}
    
    if player_id == 0:
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
            player_info = result['content'][0]['rgl']
            
            for item in player_info:
                item_info = []
                for param in def_params:
                    if item.get(param, None) != None:
                        item_info.append(item.get(param))
                list_infos.append(item_info)
            print(list_infos)  
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    
    template_str = 'game/army_info.html'
    
    if is_read == 1:
        template_str = 'game/army_info_read_only.html'
        
    parg = {}
    parg["player_id"] = player_id
    parg["is_read"] = is_read
    parg["def_params"] = def_params
    parg["result"] = result
    parg["list_infos"] = list_infos
    parg["err_msg"] = err_msg
    
    return render_to_response(template_str, parg)


def hero_add(request, player_id=0):
    req_type = 121
    result_msgs = {-1:'未知错误', 0:'成功', 2:'玩家不存在', 3:'该英雄已可招募', 4:'不存在该ID的英雄'}
    result_code = -1
    err_msg = ''
    hero_id = int(request.POST.get('hero_id', '0'))
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
        
    if player_id == 0:
        player_id = int(request.POST.get('player_id', '0'))
    
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_params = 'req_type=%d&player_id=%s&server_id=%d&hero_id=%s' % (req_type, player_id, server_id, hero_id)
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
    
        if result['code'] == 0:
            result_code = result['content'][0]
        write_gm_log(request, [req_type, server_id, player_id, result_code, hero_id])
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    result_msg = result_msgs.get(result_code, '')
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
        
    return render_to_response('game/feedback.html', parg)  
