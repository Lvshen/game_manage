#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
from GameManage.models.center import User, SafeQuestion
from GameManage.models.center import Channel
from GameManage.views.base import md5, getConn
from GameManage.cache import center_cache
from django.db import connection

def user_list(request):
    channel_id = int(request.session.get('channelId', '0'))
    if channel_id > 0:
        channel = center_cache.get_channel_list()
    
    page_size = 30
    page_num = int(request.GET.get('page_num', '1'))
    if page_num < 1:
        page_num = 1
    
    user_type = int(request.GET.get('type', '-1'))
    user_key = request.GET.get('key', '')
    model = User()
    query = Q()
     
    query = Q(user_type=0)
        
    if user_key != '':
        key_type = int(request.GET.get('key_type', '0'))
        if key_type == 0:
            try:
                query = query & Q(id=int(user_key))
            except:
                print('key_value has error')
        elif key_type == 2:
            query = query & Q(mobile_key=user_key)
        else:
            query = query & Q(username__icontains=user_key)
            
    if channel_id > 0:
        query = query & Q(channel_key=channel.key)

    list_record = []
    if query:
        total_record = User.objects.using('read').filter(query).count()
        if total_record > 0:
            list_record = User.objects.using('read').filter(query)[(page_num - 1) * page_size:page_num * page_size]
    else:
        total_record = User.objects.using('read').count()
        if total_record > 0:
            list_record = User.objects.using('read').all()[(page_num - 1) * page_size:page_num * page_size]
    
    parg = {}
    parg["user_key"] = user_key
    parg["list_record"] = list_record
    
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    
    return render_to_response('player/user_list.html', parg)

def user_lock(request, user_id=0, is_lock=0):
    
    model_id = int(user_id)
    is_lock = int(is_lock)
    
    if model_id == 0:
        model_id = int(request.GET.get('user_id', '0'))
    if is_lock == 0:
        is_lock = int(request.GET.get('is_lock', '0'))
    
    if model_id > 0 :
        try:
            model = User.objects.get(id=model_id)
            if is_lock == 1:
                if not model.is_lock():
                    model.status -= 5
            else:
                if model.is_lock():
                    model.status += 5

            model.save(using='write')
        except Exception, e:
            print('lock user error:', e)
    
    return render_to_response('feedback.html')

def user_password(request, user_id=0):
    user_id = int(user_id)
    
    if user_id == 0:
        user_id = int(request.GET.get('user_id', '0'))
    
    msg = ''
    if request.method == 'POST':
        password = request.POST.get('password', '')
        if user_id > 0 and password != '':
            try:
                the_user = User.objects.get(id=user_id, user_type=0)
                the_user.password = md5(password.lower())
                the_user.save(using='write')
                msg = '操作成功!'        
            except Exception, e:
                print('set password error:', e)
                msg = e
    
    parg = {}
    parg["user_id"] = user_id
    parg["msg"] = msg

    return render_to_response('player/user_password.html', parg)

def clear_mibao(request, user_id=0):
    user_id = int(user_id)
    
    code = 1
    msg = ''
    
    if user_id == 0:
        user_id = int(request.GET.get('user_id', request.POST.get('user_id', '0')))
        the_user = User.objects.get(id=user_id, user_type=0)
        if None != the_user:
            safeQuestion_list = SafeQuestion.objects.filter(user = the_user)
            for item in safeQuestion_list:
                item.delete(using='write')
            code = 0
            msg = '操作成功!'
        else:
            msg = '账号不存在'
    
    return HttpResponse('{"code":%s, "msg":"%s"}' % (code, msg))

def user_convert(request, server_id=0):
    server_id = int(server_id)
    err_msg = ''
    if server_id > 0:
        try:
            conn = getConn(server_id)
        except:
            err_msg = '数据库链接出错!'
    else:
        conn = connection
    if err_msg != '':
        parg = {}
        parg["err_msg"] = err_msg
        return render_to_response('feedback.html', parg)
    cursor = conn.cursor()
    
    start_pos = int(request.GET.get('pos', 0))
    if start_pos == 0:
        query_sql = 'select id from log_create_role where log_user=(select max(player_id) from player_%d)' % (server_id,)
        cursor.execute(query_sql)
        last_player_id = cursor.fetchone()
        if last_player_id != None:
            start_pos = int(last_player_id[0])
    

    sql = 'select log_user,log_result,f1,log_time,id from log_create_role where id>%d order by id limit 100' % start_pos
    cursor.execute(sql)
    list_record = cursor.fetchall()
    for item in list_record:
        try:
            #先判断存在与否
            sql = 'select count(0) from player_%d where player_id=%d' % (server_id, item[0])
            cursor.execute(sql)
            count_list = cursor.fetchone()
            total_record = int(count_list[0])
            
            if total_record == 0:
                the_user = User.objects.using('read').get(id=item[1])
                if the_user.user_type == 0:
                    link_key = the_user.id
                else:
                    link_key = the_user.link_key
                channel_id = 0
                try:
                    the_channel = Channel.objects.using('read').get(key=the_user.channel_key)
                    channel_id = the_channel.id
                except:
                    pass
                try:
                    sql = '''insert into player_%d(player_id,player_name,user_type,link_key,channel_id,create_time,last_ip,last_time,login_num,status,mobile_key)
                            values(%s,"%s",%s,"%s",%s,"%s","%s","%s",0,0,"%s")''' % (server_id, item[0], item[2].replace('\\', '\\\\'), the_user.user_type, link_key, channel_id, item[3], the_user.last_ip, the_user.last_time, the_user.mobile_key)
                    cursor.execute(sql)
                except Exception, e:
                    print('convert user has error', e, item[0])
        except Exception, e:
            print('convert user has error', e, item[0])
        start_pos = item[4]
    is_reload = True
    if len(list_record) < 100:
        err_msg = '同步完成!'
        is_reload = False
    cursor.close()
    
    parg = {}
    parg["server_id"] = server_id
    parg["start_pos"] = start_pos
    parg["is_reload"] = is_reload
    parg["err_msg"] = err_msg
    
    return render_to_response('player/user_convert.html', parg)
