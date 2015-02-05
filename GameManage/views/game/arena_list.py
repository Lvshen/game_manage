#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from GameManage.cache import center_cache
from GameManage.http import http_post
from GameManage.views.game.game_server_url import game_server_url
import json, datetime, time

def get_Top300list(request):
    
    s = int(request.GET.get('s', 0))
    
    server_id = int(request.GET.get('server_id', 0)) 
    
    if 0 == server_id:
        server_id = int(request.POST.get('server_id', 0))
    
    server_list = center_cache.get_server_list()
    
    data_list = []
    if 1 == s:
        req_type = 507
        req_params = 'req_type=%d&server_id=%d' % (int(req_type), int(server_id))
        result = http_post(game_server_url.GM_SERVER_URL, req_params, timeout_param=10)
        print result
        result = json.loads(result)  
        if result['code'] == 0:
            content_list = result['content']
            for item in content_list:
                for key in item:
                    data_item = {}
                    date = datetime.datetime.fromtimestamp(float(key))
                    data_item['date'] = date.strftime('%Y-%m-%d')
                    data_item['player_list'] = item.get(key, []) 
                    
                    data_list.append(data_item)
    
    parg = {}
    parg['server_list'] = server_list
    parg['data_list'] = data_list
    
    
    return render_to_response('game/arena_list.html', parg)
    
    
