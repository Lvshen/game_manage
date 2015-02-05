#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.db.models import Q
from GameManage.views.game.game_server_url import game_server_url
from GameManage.views.game.base import do_filter_modify_param, write_gm_log
from GameManage.views.base import UserStateManager, OperateLogManager
from GameManage.models.center import Server, Group
from GameManage.models.task import TaskDefine
from GameManage.cache import center_cache
from django.http import HttpResponse
from GameManage.http import http_post
import json, datetime


def server_info(request, server_id=0):
    def_params = get_server_param()
    server_id = int(server_id)
    if server_id == 0:
        server_id = int(request.GET.get('server_id', ''))
    net_id = request.GET.get('net_id', '-10')
    config_type = request.GET.get('config_type', '0')
    list_infos = []
    err_msg = ''
    
    try:  
        server_info = get_server_info(server_id, net_id, config_type) 
        for item in def_params:
            if server_info.get(item[0], None) != None:
                remark = ''
                if 4 <= item.__len__():
                    remark = item[3]
                list_infos.append({'name':item[1], 'key':item[0], 'value':server_info.get(item[0]), 'is_modify':item[2], 'remark':remark})
    except Exception, e:
        err_msg = '发生错误:%s!' % e
    
    
    group_list = center_cache.get_group_list()
    group_server_list =  center_cache.get_cache_server_list_group_by()
    
    parg = {}
    parg['list_infos'] = list_infos
    parg["config_type"] = config_type
    parg["net_id"] = net_id
    parg["server_id"] = server_id
    parg["group_list"] = group_list 
    parg["group_server_list"] = group_server_list
    parg["err_msg"] = err_msg
    
    return render_to_response('game/server_info.html', parg)

def get_server_info(server_id, net_id= -1, config_type=0):
    req_type = 502
    req_params = 'req_type=%d&server_id=%d&net_id=%s&config_type=%s' % (int(req_type), int(server_id), net_id, config_type)
    result = http_post(game_server_url.GM_SERVER_URL, req_params, timeout_param=10)
    result = json.loads(result) 
    server_info = {}
    if result['code'] == 0:
        server_info = result['content'][0]
    return server_info

def get_server_param():
    def_params = [
        ["is_novice_progress_use",                  "新手引导奖励功能开关",                     1, ""],
        ["is_story_ranking_use",                  "攻略功能使用开关",                         1, ""],
        ["is_vip_use",                              "VIP功能使用开关",                         1, ""],
        ["is_vip_client_use",                          "该服务器是否支持VIP特权客户端",            1, ""],
        ["simpleinfo",                              "读取玩家标准信息功能开关",                 1, ""],
        ["city_be_attacked_maintain",             "城市战后繁荣度概率",                     1, "默认值0.0(战败后不掉繁荣度),服务器中直接将该值作为随机概率"],
        ["horse_delegate_effect_param",             "战马委派获得概率加成值",                 1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["colak_delegate_effect_param",             "披风委派获得概率加成值",                 1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["NPC_elite_drop_effect_param",             "精英NPC物品掉落概率加成",                 1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["NPC_legion_drop_effect_param",         "NPC军团物品掉落概率加成",                 1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["pvp_prestige_effect_param",             "PVP战威望加成值",                         1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["train_exp_effect_param",                  "训练经验加成值",                         1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["hard_train_exp_effect_param",             "突飞经验加成值",                         1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["legion_jungong_special_time",             "NPC军团战精英时间军功加成值",             1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["collect_effect_param",                  "征收获得银币加成值",                     1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["active_reward_param",                      "活跃度获得加成值",                         1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["online_reward_param",                      "在线奖励加成值",                         1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["mine_fight_mine_silver",                 "银矿战银币产量加成值",                     1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["equipment_delegate_cost_effect",        "召唤商人价格加成值",                     1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["equipment_shopbuy_bingfu_cost_effect","兵符价格加成值",                         1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["vip_buy_junling_cost_effect",            "VIP购买军令价格加成值",                 1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["forceImpose_cost_effect",                "强征价格加成值",                         1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["refine_equipment_silver_param",        "洗炼银币价格加成值",                     1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["refine_equipment_gold_param",            "洗炼金币价格加成值",                     1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["force_product_effect_prarm",            "强制生产价格加成值",                    1, "0.0:没有加成,公式:基础概率 * ( 1 + 加成值)"],
        ["seize_reward_param",             "攻城战征税参数", 1,""],
        ["is_new_gift_card_sys_use",        "是否使用新的礼品卡模式", 1, ""]
    ]
    return def_params

def get_server_param_dictionary(): 
    dic = {}
    for item in get_server_param():
        dic[item[0]] = item[1]
    return dic

def server_modify(request, server_id=0):
    server_id = int(server_id)
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))
    err_msg = ''
    #*****定时任务设置参数 ****************
    
    task_setting = int(request.GET.get('task_setting', 0))
    trigger_time = request.GET.get('trigger_time', '')
    recover_time = request.GET.get('recover_time', '')
    
    if 1 == task_setting:
        try:
            trigger_time = datetime.datetime.strptime(trigger_time, '%Y-%m-%d %H:%M:%S')
            recover_time = datetime.datetime.strptime(recover_time, '%Y-%m-%d %H:%M:%S')
        except:
            err_msg = '请输入正确的时间格式'
    
    #*****定时任务设置参数 END ***********
    
    is_ajax = request.GET.get('ajax', False)
    req_type = 606
    result_msgs = {-1:u'未知错误', 0:u'成功'}
    result_code = -1
    config_json = request.POST
#    modify_science_info = json.dumps(modify_science_info)
    net_id = request.GET.get('net_id', '-1')
    config_type = request.GET.get('config_type', '0')
    
    source_server_info = get_server_info(server_id, net_id, config_type)
    
    log_param = {}
    request_param = do_filter_server_param(config_json, source_server_info, log_param) 
    
    #需要设置定时任务
    if task_setting == 1:
        server = Server.objects.get(id=server_id)
        recover_data = {}
        for modify_param_key in request_param:
            recover_data[modify_param_key] = source_server_info.get(modify_param_key)
        setting_task(server, net_id, trigger_time, recover_time, recover_data, request_param)
        if is_ajax:
            return HttpResponse('{code:0,msg:"设置成功"}')
        
        return render_to_response('game/feedback.html', {"result_msg":u"设置成功"})
    
    
    request_param = json.dumps(request_param, ensure_ascii=False)#转化字符串
    log_param = json.dumps(log_param, ensure_ascii=False)
    
    req_params = 'req_type=%d&server_id=%d&net_id=%s&config_type=%s&config_json=%s' % (req_type, server_id, net_id, config_type, request_param)
    
    try:
        result = http_post(game_server_url.GM_SERVER_URL, req_params, timeout_param=10)
        result = json.loads(result)
        #print(game_server_url.GM_SERVER_URL, req_params, result)
        if result['code'] == 0:
            result_code = result['content'][0]
        
        write_gm_log(request, [req_type, server_id, net_id, result_code, log_param])
    except Exception, e:
        err_msg = u'发生错误%s' % e
    result_msg = result_msgs.get(result_code, '')
    
    if is_ajax:
        
        if err_msg.__len__() > 0:
            return HttpResponse('{code:1,msg:"%s"}' % err_msg)
         
        return HttpResponse('{code:%s,msg:"%s"}' % (result_code, result_msg))
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
    
    return render_to_response('game/feedback.html', parg)

def setting_task(server, net_id, trigger_time, recover_time, recover_data, setting_data):
    server_id = server.id
    title = u"服务器ID%s活动设置" % server.name
    #过滤是否已经设置过
    q = Q(title=title) & Q(trigger_date=trigger_time) & Q(end_date=recover_time)
    task = TaskDefine()
    list_data = TaskDefine.objects.filter(q)
    if 0 < list_data.__len__():
        task = list_data[0]
    
    setting_param = {"req_type":606, "server_id":server_id, "net_id":net_id, "config_type":0, "json_param":{"config_json":setting_data}}
    recover_param = {"req_type":606, "server_id":server_id, "net_id":net_id, "config_type":0, "json_param":{"config_json":recover_data}}
    
    task.title = title
    task.type = u"服务器参数设置"
    task.state = 0
    task.request_url = game_server_url.GM_SERVER_URL
    task.source_cfg = json.dumps(recover_param)
    task.target_cfg = json.dumps(setting_param)
    task.trigger_date = trigger_time
    task.end_date = recover_time
    task.interval = 0
    task.result_msg = '{"content": [0], "code": 0}'
    task.remark = ''
    task.counter = 0
    task.save()
    
    

def save_server_modify_log(request, log_param, server_id):
    msg_str = u'没有操作'
    msg = [] 
    for key in log_param:
        msg.append(key)
    if msg.__len__() != 0:
        msg_str  = ','.join(msg)
    the_user_id = UserStateManager.get_the_user_id(request)
    ip = OperateLogManager.get_request_ipAddress(request)
    request_path = '/game/server/info/%s' % server_id
    OperateLogManager.save_operate_log(the_user_id, msg_str, request_path, ip)


#处理过滤只修改的值放入集合， 并纪录到 log_param 集合， 返回 只修改的 参数集合
def do_filter_server_param(server_info, source_server_info, log_param): 
    server_param_dic = get_server_param_dictionary() 
    return do_filter_modify_param(server_info, source_server_info, log_param, server_param_dic)



#--HTTP获取最新服务器列表
def post_getServer_list(request): 
    req_params = 'req_type=601'
    result = http_post(game_server_url.GM_SERVER_URL, req_params, timeout_param=10)
    result = json.loads(result)
    msg = '失败'
    
    if result != '' and result != None:
        if result['code'] == '0' or result['code'] == 0:
            msg = '成功'
    
    return HttpResponse(msg)
