#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.models.admin import Admin
from GameManage.models.center import Channel, Server
from GameManage.views.base import UserStateManager
from django.db.models import Q
from GameManage.models.center import  Question, Group
from django.http import HttpResponse
from GameManage.cache import center_cache
import json, MySQLdb, datetime

def manage_question_list(request, user_id=0, status= -1):
    ajax = request.GET.get('ajax', False)
    if status == -1 :
        status = int(request.GET.get('status', '-1'))
    
    search_type = int(request.GET.get('search_type', '-1'))
    question_type = int(request.GET.get('question_type', '-1'))
    group_id = int(request.GET.get('group_id', -1))
    kefu_name = request.GET.get('kefu_name', '')
    vip = -1
    try:
        vip = int(request.GET.get('vip', -1))
    except:
        vip = -1
    
    the_user_id = int(request.session.get('userid', '0'))
    the_user = Admin.objects.using('read').get(id=the_user_id)
    
    usm = UserStateManager(request)
    
    list_group = Group.objects.using('read').all()
    
    server_id = int(request.GET.get('server_id', '0'))
    
    if server_id == 0:
        server_id = int(request.session.get("serverId", '0')) 
    
    if user_id == 0 or user_id == '0':
        user_id = request.GET.get('user_id', '')
    
    status = int(status)
    page_num = int(request.GET.get('page_num', '1'))
    page_size = 20
    total_page = 1
    if page_num < 1:
        page_num = 1
     
    kefu_list = Admin.objects.using('read').filter(role__id = 3)
    for kefuItem in kefu_list:
        kefuServerList = kefuItem.server.all()
        kefuServerIdList = "{\'server\':["
        for kefuServerItem in kefuServerList:
            if kefuServerIdList == "{\'server\':[":
                kefuServerIdList += "{\'serverId\':'%s',\'serverName\':'%s'}" % (kefuServerItem.id, kefuServerItem.name)
            else:
                kefuServerIdList += ",{\'serverId\':'%s',\'serverName\':'%s'}" % (kefuServerItem.id, kefuServerItem.name)
        kefuServerIdList += "]}"
        #print kefuServerIdList
        kefuItem.kefuServerIdList = kefuServerIdList
    
    # *** 过滤 服务器列表 ***
    if usm.current_userRole_is_root():
        list_server = center_cache.get_server_list()
    else:
        list_server = center_cache.get_user_server_list(the_user)
        
    group_server_list = []    
    if group_id > 0 :
        group = Group.objects.using('read').get(id = group_id)
        for item in group.server.all():
            group_server_list.append(item)
    
        tmp_list = []    
        for item in group_server_list:
            if list_server.__contains__(item):
                tmp_list.append(item)
    
        list_server = tmp_list
        tmp_list = None
        group_server_list = None
    
    # *** 过滤 服务器列表 END  ***
        
    
    theUserServerId = []
    itemServerList = {}
    for item in list_server:
        itemServerList[item.id] = item.name
        
        if len(the_user.server.filter(id=item.id)) > 0:
            item.is_show = 1
            theUserServerId.append(item.id)
      
    query = Q()
    
    if user_id != '':
        if search_type == 1:
            query = query & Q(post_user=user_id)
        elif search_type == 2:
            query = query & Q(question__contains = user_id)
        elif search_type == 3:
            query = query & Q(score=user_id)
          
    
    if -1 != vip:
        query = query & Q(post_user_id = vip)
    
    if -1 != question_type:
        query = query & Q(question_type=question_type)
    
    if server_id > 0:
            query = query & Q(server_id=server_id)
    else: 
        if not usm.current_userRole_is_root():
            server_id_list = [item.id for item in list_server]
            query = query & Q(server_id__in = server_id_list)
    
    if '' != kefu_name:
        query = query & Q(reply_user = kefu_name)
    
    if not usm.current_userRole_is_root():
        channel_list = center_cache.get_user_channel_list(the_user)
        channel_id_list = [item.id for item in channel_list]
        channel_id_list.append(0)
        query = query & Q(channel_id__in = channel_id_list)
        
    if status != -1:
        query = query & Q(status=status)

    total_record = Question.objects.using('read').filter(query).count()
    list_record = Question.objects.using('read').filter(query)[(page_num - 1) * page_size:page_num * page_size]
            
    for item in list_record:
        if item.server_id > 0:
            item.serverName = itemServerList.get(item.server_id, '--')
        else:
            item.serverName = "--"

    if total_record > page_size:
        total_page = total_record / page_size
        if total_record % page_size > 0:
            total_page += 1
    
    parg = {}
    parg["server_id"] = server_id
    parg["list_server"] = list_server
    parg["user_id"] = user_id
    parg["usm"] = usm
    parg["kefu_list"] = kefu_list
    parg["the_user_id"] = the_user_id
    parg["list_record"] = list_record
    parg["search_type"] = search_type
    parg["status"] = status
    parg["list_group"] = list_group
    parg["kefu_name"] = kefu_name
    
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    parg["question_type"] = question_type
    parg["group_id"] = group_id
    
    if ajax:  
        return render_to_response('server/question_list_block.html', parg)
    
     
    return render_to_response('server/question_list.html', parg)


#客服回复问题（如果是渠道后台,则需要判断被回复的玩家所在渠道是否在本渠道）
def manage_question_answer(request):
    question_id = int(request.POST.get('question_id', 0))
    answer = request.POST.get('answer', '')
    the_admin_id = int(request.session.get('userid', '0'))
    channel_id = int(request.session.get('channel_id', '0'))
    reply_name = 'admin'
    
    if channel_id != 0 and the_admin_id == 0: #用渠道账号登陆并 不是 管理员后台进入的
        channel_item = Channel.objects.get(id=channel_id)
        reply_name = channel_item.name
        entity = Question.objects.using('read').get(id=question_id)
        server_id = int(entity.post_user) >> 20 #移位得到服务器id
        server = Server.objects.using('read').get(id=server_id)
        the_db_config = json.loads(server.log_db_config)
        conn = MySQLdb.connect(host=the_db_config['host'], user=the_db_config['user'], passwd=the_db_config['password'], port=the_db_config.get('port',3306), db=the_db_config['db'], charset="utf8")
        conn.autocommit(1)
        cursor = conn.cursor()
        #查询角色表，并查看角色是否在本渠道上开的用户
        sql = ' SELECT COUNT(0) FROM player_%d WHERE player_id=%d AND channel_id = %d' % (server_id , entity.post_user, channel_id)
        cursor.execute(sql)
        total_record = int(cursor.fetchone()[0])
        if total_record <= 0 :
            return HttpResponse("此用户不是本渠道")
    
    question = None
    
    if question_id > 0:
        question = Question.objects.get(id=question_id)
    
    if answer != '' and question != None:
        question.answer = answer
        the_user_id = int(request.session.get('userid', '0'))
        the_user = None
        if the_user_id > 0:
            the_user = Admin.objects.get(id=the_user_id)
            reply_name = the_user.username
        question.reply_user = reply_name
        question.status = 1
        question.reply_time = datetime.datetime.now()
        question.save(using='write')
     
    
    return HttpResponse('')
    
    


def manage_question_remove(request, question_id=0):
    question_id = int(question_id)
    ajax = request.GET.get('ajax', False)
    question = None 
    if question_id < 1:
        question_id = int(request.GET.get('question_id', '0'))
    
    if question_id > 0:
        question = Question.objects.get(id=question_id)
    
    if question != None:
        question.delete(using='write')
        
    if ajax : 
        return HttpResponse("删除成功！")

    return render_to_response('feedback.html')

#
#def question_convert(request):
#    conn_list = {}
#    
#    local_cursor = connections['write'].cursor()
##    try:
##        Player._meta.db_table = 'player_%d'%server_id
##        sql, _ = connection.creation.sql_create_model(Player,no_style())
##        sql = sql[0].replace('CREATE TABLE','CREATE TABLE if not exists')
##        print(sql)
##        local_cursor.execute(sql)
##    except Exception,e:
##        print('create table has error',e)
##    list_question = Question.objects.filter(post_user=0).distinct()[:500]
#    sql = 'select server_id,post_user_id from question where post_user=0 group by post_user_id limit 100'
#    local_cursor.execute(sql)
#    list_question = local_cursor.fetchall()
#    for item in list_question:
#        sql = 'select log_user from log_create_role where log_result=%d order by id desc limit 1' % item[1]
#        if conn_list.get(item[0], None) != None:
#            the_conn = conn_list[item[0]]
#        else:
#            the_conn = getConn(item[0])
#            conn_list[item[0]] = the_conn
#            
#        cursor = the_conn.cursor()  
#        cursor.execute(sql)
#        the_player = cursor.fetchone()
#        the_player_id = -1
#        if the_player != None:
#            the_player_id = int(the_player[0])
#
#        print(item[0], the_player_id, item[1])
#        sql = 'update question set post_user=%d where post_user=0 and post_user_id=%d and server_id=%d' % (the_player_id, item[1], item[0])
#        local_cursor.execute(sql)
#        #item.save()
#
#    is_reload = True    
#    if len(list_question) < 100:
#        err_msg = '同步完成!'
#        is_reload = False
#    
#    return render_to_response('server/question_convert.html', locals())


