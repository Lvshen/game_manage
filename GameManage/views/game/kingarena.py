#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.models.center import Server 
from GameManage.views.base import get_server_list
from GameManage.http import http_post
import json


def get_kingarena_player_param():
    result= {
        "lv": u"等级",
        "na": u"姓名",
        "bkt": u"当选时间",
        "player_id": u"玩家ID",
        "dwn": u"决赛胜利次数",
        }
    return result

def get_kingarena_position_param():
    result = {"king":u"国王", "left":u"左储君", "right":u"右储君"}
    return result
   
def get_seige_city_list():
    result = ["酒泉城","西平","张掖","汉嘉","朱提","永昌"]
    return result

#国王争霸信息    返回顺序'魏', '蜀', '吴'
def kingarena_info(request):
    list_infos = []
    list_server = get_server_list()
    is_search = request.GET.get('is_search', False)
    server_id = int(request.GET.get('server_id', '0'))
    err_msg = None
    if is_search:
        req_params = 'req_type=505&server_id=%d' % server_id 
        result = ''
        try:
            result = http_post(game_server_url.GM_SERVER_URL, req_params, timeout_param=10) 
            result = json.loads(result)
        except:
            err_msg = '获取失败!'
        if result != '' and result != None and err_msg == None:
            if result['code'] == '0' or result['code'] == 0:
                country_json = result.get("content")[0]
                
                position_param = get_kingarena_position_param();
                player_dic = get_kingarena_player_param();
                 
                for country in country_json:
                    position_array = []
                    for p_key in  position_param:
                        cname = position_param.get(p_key)
                        value = u"没有数据"
                        player_json = country.get(p_key) 
                        if player_json != None and player_json != '': 
                            player_attribute =  get_king_player_attribute(player_json, player_dic)
                            value = ','.join(player_attribute)
                            
                        tmp = "%s: %s" % (cname, value)
                        position_array.append(tmp)
                    list_infos.append(position_array)
    
    parg = {}
    parg["list_infos"] = list_infos
    parg["list_server"] = list_server
    parg["server_id"] = server_id
    parg["err_msg"] = err_msg
    
    return render_to_response('game/kingarena_info.html', parg)

def get_king_player_attribute(player_json, cname_dic):
    player_attribute = []
    for u_key in cname_dic:
        cname = cname_dic.get(u_key)
        value = player_json.get(u_key)
        tmp = ("%s: %s" % (cname, value)) 
        player_attribute.append(tmp)
    return player_attribute
