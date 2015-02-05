#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.cache import center_cache
from GameManage.http import http_post
import json

def build_info(request, player_id=0, is_read=0):
    req_type = 6
    def_params = {0:u"主城", 1:u"银库", 2:u"民居一", 3:u"民居二", 4:u"民居三", 5:u"民居四", 6:u"商店", 7:u"校场", 8:u"军机处", 9:u"粮仓", 10:u"市场", 11:u"兵营", 12:u"民居五", 13:u"民居六", 14:u"民居七", 15:u"账房", 16:u"民居八", 17:u"铸币厂", 18:u"民居九", 19:u"驿站", 20:u"钱庄", 21:u"民居十", 22:u"第二校场", 23:u"纺织局", 24:u"铁匠铺"}
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
            build_list = result['content'][0]['buildingList']
            
            for item in build_list:
                if def_params.get(item['rawId'], None) != None:
                    list_infos.append({'name':def_params.get(item['rawId'], '未知'), 'key':item['rawId'], 'value':item['level'], 'is_modify':0})
    except Exception, e:
        err_msg = '发生错误:%s!' % e
    template_str = 'game/build_info.html'
    if is_read == 1:
        template_str = 'game/build_info_read_only.html'
    
    parg = {}
    parg["player_id"] = player_id
    parg["list_infos"] = list_infos
    parg["err_msg"] = err_msg
    
    return render_to_response(template_str, parg)
    
