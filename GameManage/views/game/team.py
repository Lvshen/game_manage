#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.cache import center_cache
from GameManage.http import http_post
import json


def team_info(request, player_id=0):
    req_type = 7
    def_params = [["createTime", u"创办时间", 0],
    ["creator", u"创办者ID", 0],
    ["creatorName", u"创办者姓名", 0],
    ["declaration", u"留言", 0],
    ["emblemLv", u"军徵等级", 0],
    ["kingdom", u"所属国家", 0],
    ["leader", u"当前领袖ID", 0],
    ["leaderName", u"当前领袖名字", 0],
    ["legionLv", u"军团等级", 0],
    ["name", u"军团名称", 0],
    ["legionId", u"军团ID", 0]]
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id',0))
    
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    legion_name = request.GET.get('legion_name', '')
    
    req_params = 'req_type=%d&player_id=%s&server_id=%d&legion_name=%s' % (req_type, player_id, server_id, legion_name)
    list_infos = []
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
        print(game_server_url.GM_PLAYER_URL, req_params, result)
        
        if result['code'] == 0:
            player_info = result['content'][0]
            
            for item in def_params:
                if player_info.get(item[0], None) != None:
                    list_infos.append({'name':item[1], 'key':item[0], 'value':player_info.get(item[0]), 'is_modify':item[2]})
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    return render_to_response('game/player_info.html', locals())


