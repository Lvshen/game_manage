#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.cache import center_cache
from GameManage.http import http_post
import json



def train_info(request, player_id=0,is_read=0):
    req_type = 4
    def_params = {"gi":u"武将ID", "ft":u"训练结束时间", "tt":u"训练类型", "lu":u"最后更新时间"}
    #"pn":"训练位置","tl":"训练列表","hft":"突飞CD完成时间","hil":"突飞CD完成时间",
    if player_id == 0:
        player_id = int(request.GET.get('player_id', 0))
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
            train_info = result['content'][0]['tl']
            
            for item in train_info:
                item_info = []
                for param in def_params:
                    if item.get(param, None) != None:
                        item_info.append(item.get(param))
                list_infos.append(item_info)
                
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
        
    template_str = 'game/train_info.html'
    if is_read == 1:
        template_str = 'game/train_info_read_only.html'
    
    parg = {}
    parg["player_id"] = player_id
    parg["result"] = result
    parg["def_params"] = def_params
    parg["list_infos"] = list_infos
    parg["err_msg"] = err_msg
    
    return render_to_response(template_str, parg)
