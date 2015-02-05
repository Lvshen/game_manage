#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.game.game_server_url import game_server_url
from GameManage.views.game.base import do_filter_modify_param, write_gm_log
from GameManage.views.base import getConn, UserStateManager, get_server_list
from GameManage.models.center import Server
from GameManage.cache import center_cache
from django.http import HttpResponse
from GameManage.http import http_post
import json, time, MySQLdb

def player_admin(request):
    
    pass
    

def player_info(request, player_id=0,is_read=0):
    def_params = get_player_info_param()
    list_infos = []
    err_msg = ''
    if player_id==0:
        player_id = int(request.GET.get('player_id',0))
    try: 
        player_info = get_player_info(player_id) 
        for item in def_params:
            if player_info.get(item[0], None) != None:
                list_infos.append({'name':item[1], 'key':item[0], 'value':player_info.get(item[0]), 'is_modify':item[2]})
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    template_str = 'game/player_info.html' 
    if is_read == 1:
        template_str = 'game/player_info_read_only.html'
    
    parg = {}
    parg["player_id"] = player_id 
    parg["list_infos"] = list_infos
    parg["err_msg"] = err_msg
    
    return render_to_response(template_str, parg)
    

def get_player_info(player_id):
    req_type = 1
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_params = 'req_type=%d&player_id=%s&server_id=%d' % (req_type, player_id, server_id)
    
    result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
    
    result = json.loads(result)
    player_info = {}
    if result['code'] == 0:
        player_info = result['content'][0]
    
    return player_info

def get_player_info_param():
    def_params = [
    ["nn", u"昵称", 0],
    ["uid", u"帐号ID", 0],
    ["pi", u"玩家ID", 0],
    ["fl", u"旗号", 0],
    ["lv", u"等级", 0],
    ["olv", u"官职", 0],
    ["cid", u"玩家所在当前城市id", 0],
    ["ln", u"军团名称", 0],
    ["gs", u"游戏进度", 0],
    ["rk", u"排名", 0],
    ["lt", u"登陆时间", 0],
    ["kid", u"所属国", 0],
    ["hi", u"头像图片ID", 0],
    ["lp", u"所在地区页", 0],
    ["lg", u"所在地格", 0],
    ["gl", u"金币", 1],
    ["sl", u"银币", 1],
    ["slm", u"银上限", 0],
    ["fd", u"粮", 1],
    ["fdm", u"粮上限", 0],
    ["sn", u"士兵数量", 1],
    ["snm", u"士兵数量上限", 0],
    ["jg", u"军工", 1],
    ["ww", u"威望", 1],
    ["jl", u"军令", 1],
    ["jlcd", u"军令cd", 0],
    ["icdl", u"军令cd是否已红", 0],
    ["mcd", u"迁移CD结束时间", 0],
    ["ids", u"今日俸禄是否已领", 0],
    ["np", u"玩家引导进度", 0],
    ["rg", u"玩家充值金币总数量", 1],
    ["tjbn", u"当天军令购买量", 0],
    ["vbut", u"vip购买更新点的时间", 0],
    ["en", u"敌对度", 0],
    ["legionId", u"军团ID", 0]
    ]
    return def_params

#获取角色 参数 "字典"
def get_player_info_dictionary():
    dic = {}
    for item in get_player_info_param():
        dic[item[0]] = item[1]
    return dic



def player_shutup(request, player_id=0): 
    req_type = 102
    result_msgs = {-1:'未知错误', 0:'成功'}
    result_code = -1
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
    
    if player_id == 0:
        player_id = int(request.POST.get('player_id', '0'))
    
    is_ajax = request.GET.get('ajax', False)
    
    
    server_id = int(player_id) >> 20 
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    time_len = int(request.GET.get('time', '1800'))
    
    
    
    req_params = 'req_type=%d&player_id=%s&server_id=%d&time=%d' % (req_type, player_id, server_id, time_len)
    err_msg = ''
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
        if result['code'] == 0:
            result_code = result['content'][0]
        write_gm_log(request, [req_type, server_id, player_id, result_code, time_len])
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    result_msg = result_msgs.get(result_code, '')
    
    if is_ajax:
        return HttpResponse(result_code);
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
    
    return render_to_response('game/feedback.html', parg)

   

def player_unshutup(request, player_id=0): 
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
    
    req_type = 103
    result_msgs = {-1:'未知错误', 0:'成功'}
    result_code = -1
    
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_params = 'req_type=%d&player_id=%s&server_id=%d' % (req_type, player_id, server_id)
    err_msg = ''
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params)
        result = json.loads(result)
        print(game_server_url.GM_PLAYER_URL, req_params, result)
        if result['code'] == 0:
            result_code = result['content'][0]
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    
    result_msg = result_msgs.get(result_code, '')
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
    
    return render_to_response('game/feedback.html', parg)         

def player_modify(request, player_id=0):
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
    
    result_msgs = {-1:'未知错误', 0:'成功'}
    result_code = -1
    
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    player_info = request.POST
    req_type = get_player_modify_PostType(player_info)#获取请求类别
    
    source_player_info = get_player_info(player_id)#原有player数据
     
    #player_info = {"nn":'hello', "uid":1, "pi":3}
    #source_player_info = {"nn":'hello2', "uid":2, "pi":3}
    err_msg = ''
    result_msg = ''
    append_gl = request.POST.get('append_gl', '')
    if append_gl != '':
        try:
            append_gl = float(append_gl)
            if append_gl >= 50000:
                err_msg = '金币修改最大5W'
        except Exception, ex:
            err_msg = '追加金不能超过50000'
            print 'player_modify error'
            print ex
    
    if err_msg == '':
        log_param = {}  
        #<QueryDict: {u'jl': [u'50000'], u'append_gl': [u''], u'append_fd': [u''], u'append_sn': [u''], u'append_sl': [u''], u'append_ww': [u''], u'rg': [u'0'], u'append_rg': [u''], u'ww': [u'200'], u'append_jl': [u''], u'append_jg': [u''], u'fd': [u'6000'], u'sn': [u'4000'], u'jg': [u'410'], u'sl': [u'125'], u'gl': [u'1905']}>
        request_param = do_filter_player_param(player_info, source_player_info, log_param, req_type)#过滤 没被修改的参数，并纪录到日志集合
        
        log_param = json.dumps(log_param, ensure_ascii=False)
        request_param = json.dumps(request_param, ensure_ascii=False)#转化字符串 
        
        req_params = 'req_type=%d&player_id=%s&server_id=%d&edited_player_info=%s' % (req_type, player_id, server_id, request_param)
        err_msg = ''
        try: 
            result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10) 
            result = json.loads(result)
            print(game_server_url.GM_PLAYER_URL, req_params, result)
            if result['code'] == 0:
                result_code = result['content'][0]
            write_gm_log(request, [req_type, server_id, player_id, result_code, log_param]) #写日志，保存到数据库
        except Exception, e:
            err_msg = '发生错误:%s!' % e    
        
        result_msg = result_msgs.get(result_code, '')
    else:
        result_msg = err_msg
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
    
    return render_to_response('game/feedback.html', parg)     
    
#根据请求提交回来的参数，区别是覆盖玩家信息或者是追加值
def get_player_modify_PostType(request_QueryDict):
    for key in request_QueryDict:
        if -1 != key.find('append_'):
            value = request_QueryDict[key]
            if value != '' and value != 0:
                return 105
    return 104

#处理过滤只修改的值放入集合， 并纪录到 log_param 集合， 返回 只修改的 参数集合
def do_filter_player_param(player_info, source_player_info, log_param, req_type):
    player_param_dic = get_player_info_dictionary()
    is_append = False
    if req_type == 105:
        is_append = True 
    return do_filter_modify_param(player_info, source_player_info, log_param, player_param_dic, is_append)



def shutup_list(request, server_id=0):
    req_type = 503
    
    server_id = int(server_id)
    
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))
    
    net_id = request.GET.get('net_id', '-1')
    req_params = 'req_type=%d&server_id=%d&net_id=%s' % (req_type, server_id, net_id)
    list_record = []
    try:
        result = http_post(game_server_url.GM_SERVER_URL, req_params, timeout_param=10)
        result = json.loads(result)
        print(game_server_url.GM_SERVER_URL, req_params, result)
        list_shutup = []
        if result['code'] == 0:
            list_shutup = result['content'][0]
             
        conn = getConn(server_id)
        cursor = conn.cursor()
        
        sql2 = 'select player_id,player_name,channel_id,user_type,link_key,login_num,mobile_key,last_time,create_time,status from player_%d where player_id in(%s)' % (server_id, ','.join(list_shutup))
        cursor.execute(sql2)
        
        list_tmp = cursor.fetchall()
        cursor.close()
        int_time = int(time.time())
        for item in list_tmp:
#            print(item)
            item = list(item)
            item.append(list_shutup.get(str(item[0]), 0) - int_time)
            list_record.append(item)
    except Exception, e:
        pass
    
    
    parg = {}
    parg["server_id"] = server_id
    parg["list_record"] = list_record
    
    return render_to_response('game/shutup_list.html', parg)  


def send_msg(request, server_id=0):
    server_id = int(server_id)
    player_id = int(request.GET.get('player_id', '0'))
    
    if player_id == 0:
        player_id = int(request.POST.get('player_id', '0'))
    
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))
    
    if server_id == 0:
        server_id = int(request.POST.get('server_id', '0'))
    
    
    usm = UserStateManager(request) 
    
    server_list = []
    if server_id == 0:
        if usm.current_userRole_is_root():
            server_list = get_server_list()
        else:
            server_list = usm.get_the_user().server.all()
    
    err_msg = ''
    if request.method == 'POST':
        result_msgs = {-1:'未知错误', 0:'成功'}
        result_code = -1
        
        if not usm.current_userRole_is_root():
            the_user = usm.get_the_user()
            user_server_list = []
            for server in the_user.server.all():
                user_server_list.append(server.id)
            if not user_server_list.__contains__(server_id):
                return HttpResponse(u'没有权限')
        
        server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
        msg_content = request.POST.get('content', '').encode('utf-8')
        try:
            if player_id > 0:
                if request.POST.get('msg_type', '0') == '0':
                    req_type = 612
                else:
                    req_type = 616
                    
                req_params = 'req_type=%d&server_id=%d&reciver_id=%s&msg_content=%s' % (req_type, server_id, player_id, msg_content)
            else:
                req_type = 611
                net_id = request.GET.get('net_id', '-1')
                req_params = 'req_type=%d&server_id=%d&net_id=%s&msg_content=%s' % (req_type, server_id, net_id, msg_content)
            
            result = http_post(game_server_url.GM_SERVER_URL, req_params, timeout_param=10)
            result = json.loads(result)
            print(game_server_url.GM_SERVER_URL, req_params, result)
            
            if result['code'] == 0:
                result_code = result['content'][0]
            write_gm_log(request, [req_type, server_id, player_id, result_code, msg_content])
        except Exception, e:
            err_msg = '发生错误%s' % e
            #print(u'发生错误:%s' % e)
        result_msg = result_msgs.get(result_code, '')
        
        parg = {}
        parg["err_msg"] = err_msg
        parg["result_msg"] = result_msg
        
        return render_to_response('game/feedback.html', locals())  
    
    parg = {}
    parg["server_id"] = server_id
    parg["player_id"] = player_id
    parg["server_list"] = server_list
    
    return render_to_response('game/send_msg.html', parg)



def player_down(request, player_id=0):
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
    
    req_type = 101
    result_msgs = {-1:'未知错误', 0:'成功', 1:'玩家不在线'}
    result_code = -1
    
    server_id = int(player_id) >> 20
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    req_params = 'req_type=%d&player_id=%s&server_id=%d' % (req_type, player_id, server_id)
    err_msg = ''
    try:
        result = http_post(game_server_url.GM_PLAYER_URL, req_params, timeout_param=10)
        result = json.loads(result)
        
        if result['code'] == 0:
            result_code = result['content'][0]
        write_gm_log(request, [req_type, server_id, player_id, result_code, ''])
    except Exception, e:
        err_msg = '发生错误:%s!' % e  
    
    result_msg = result_msgs.get(result_code, '')
    
    parg = {}
    parg["result_msg"] = result_msg
    parg["err_msg"] = err_msg
    
    return render_to_response('game/feedback.html', parg)

def channel_player_shutup(request, player_id=0):
    channel_id = int(request.session.get('channel_id', '0'))
    
    server_id = int(player_id) >> 20 
    server_id = center_cache.get_server_config(server_id, 'master_server_id', server_id)
    if channel_id != 0:#判断 是否在渠道后台中调用此函数    (是否有权限删除)
        server = Server.objects.using('read').get(id=server_id)
        the_db_config = json.loads(server.log_db_config)
        conn = MySQLdb.connect(host=the_db_config['host'], user=the_db_config['user'], passwd=the_db_config['password'], db=the_db_config['db'], charset="utf8")
        conn.autocommit(1)
        cursor = conn.cursor()#获得当前选择的服务器连接
        sql = 'SELECT COUNT(0) FROM player_%d WHERE channel_id=%d ' % (server_id, channel_id) 
        cursor.execute(sql) 
        total_record = int(cursor.fetchone()[0])
        if 0 >= total_record:
            return HttpResponse('没有权限操作') 
    if channel_id == 0:
        return HttpResponse("请登录渠道后台！")
    
    return player_shutup(request, player_id) 
