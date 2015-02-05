#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.views.game.base import write_gm_log
from GameManage.cache import center_cache
from GameManage.http import http_post
import json


def seience_info(request, player_id=0,is_read=0):
    #req_type = 3
    def_params = get_seience_param()
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0')) 
    #req_params = 'req_type=%d&player_id=%s&server_id=%d' % (req_type, player_id, server_id)
    list_infos = []
    err_msg = ''
    try:
         
        seience_info = get_seience_info(player_id) 
        for item in def_params:  
            if len(seience_info) > int(item[0]):
                #raise Exception, item[1]
                list_infos.append({'name':item[1], 'key':item[0], 'value':seience_info[int(item[0])], 'is_modify':item[2]})
                
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    
    template_str = 'game/seience_info.html'
    if is_read == 1:
        template_str = 'game/seience_info_read_only.html'
    
    parg = {}
    parg["player_id"] = player_id
    parg["list_infos"] = list_infos
    parg["err_msg"] = err_msg
    
    return render_to_response(template_str, parg)

def get_seience_info(player_id):
    req_type = 3  
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_params = 'req_type=%d&player_id=%s&server_id=%d' % (req_type, player_id, server_id) 
    result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
    result = json.loads(result)
    seience_info = {}
    if result['code'] == 0:
        seience_info = result['content'][0]['scl']
        
    return seience_info

def get_seience_param():
    def_params = [
    ["0", u"兵刃锻造", 1],
    ["1", u"玄麟阵", 0],
    ["2", u"扩军令牌", 1],
    ["3", u"长蛇阵", 0],
    ["4", u"战马冲锋", 1],
    ["5", u"龙牙阵", 0],
    ["6", u"甲胄锻造", 1],
    ["7", u"战队操练", 1],
    ["8", u"虎翼阵", 0],
    ["9", u"机械策略", 1],
    ["10", u"八卦阵", 0],
    ["11", u"敌情应变", 1],
    ["12", u"奇煌阵", 0],
    ["13", u"统兵军旗", 1],
    ["14", u"背水阵", 0],
    ["15", u"玄甲阵", 0],
    ["16", u"战争檄文", 1],
    ["17", u"随军郎中", 1],
    ["18", u"全军整训", 1],
    ["19", u"富国强兵", 1],
    ["20", u"城墙修葺", 1],
    ["21", u"抛石研究", 1],
    ["22", u"搏击术", 1],
    ["23", u"坚韧术", 1],
    ["24", u"突进术", 1],
    ["25", u"列阵术", 1],
    ["26", u"奇谋术", 1],
    ["27", u"冥想术", 1],
    ["28", u"甲坚兵利", 1],
    ["29", u"鲜衣怒马", 1],
    ["30", u"地灵人杰", 1],
    ]
    return def_params

def get_seience_param_dictionary():
    dic = {}
    for item in get_seience_param():
        dic[item[0]] = item[1]
    return dic


def seience_modify(request, player_id=0):
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
    
    req_type = 131
    result_msgs = {-1:'未知错误', 0:'成功', 1:'更新信息中存在不允许更新的布阵科技ID'}
    result_code = -1
    
    #modify_science_info = json.dumps(request.POST)
#    modify_science_info = json.dumps(modify_science_info)
    
    log_param = {}
    request_param = do_filter_seience_param(request.POST, get_seience_info(player_id), log_param)
    request_param = json.dumps(request_param, ensure_ascii=False)
    log_param = json.dumps(log_param, ensure_ascii=False)
    
    err_msg = ''
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_params = 'req_type=%d&player_id=%s&server_id=%d&modify_science_info=%s' % (req_type, player_id, server_id, request_param)
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
        print(game_server_url.GM_PLAYER_URL, req_params, result)
        if result['code'] == 0:
            result_code = result['content'][0]
        
        write_gm_log(request, [req_type, server_id, player_id, result_code, log_param])
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    result_msg = result_msgs.get(result_code, '')
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
    
    return render_to_response('game/feedback.html', parg)  


#处理过滤只修改的值放入集合， 并纪录到 log_param 集合， 返回 只修改的 参数集合
def do_filter_seience_param(seience_info, source_seience_info, log_param):
    request_param = {}  
    dic = get_seience_param_dictionary() 
    for key in seience_info:
        
        tmp = seience_info.get(key, 'empty_data')
        if tmp == 'empty_data':
            continue
        finalVal = int(seience_info[key])
        sourceVal = source_seience_info[int(key)]
        if finalVal != sourceVal:
            cname = dic.get(key, key)#获取参数对应的中文意思
            log_param[cname] = [finalVal, sourceVal] #纪录原来的值和被修改的值到日志集合
            request_param[int(key)] = finalVal
            
    return request_param

