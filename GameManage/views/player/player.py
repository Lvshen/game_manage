#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2012-7-6

@author: sanlang
'''

from django.shortcuts import render_to_response
from GameManage.models.center import Server,Channel, Group
from GameManage.models.log import LogDefine, FieldDefine, ValueDefine
from GameManage.views.base import UserStateManager, getConn, get_server_list
from GameManage.cache import center_cache
import datetime
import json
import MySQLdb
from django.db import connection

def player_silver_detail(request):
    server_id = request.POST.get("server_id","")
    query_incoming = request.POST.getlist("incoming_type")
    query_outcoming = request.POST.getlist("outcoming_type")
    sdate=request.POST.get("sdate","")
    edate=request.POST.get("edate","")
    page_num=int(request.GET.get('page_num','1'))
    user_id=request.POST.get("user_id","")
    user_name=request.POST.get("user_name","")
    err_msg = ''
    page_size=30
    
    list_server = center_cache.get_server_list()
    
    if server_id=="":
        server_id="0"
    server_id=int(server_id)
    
    if server_id<1 and len(list_server)>0:
        server_id=list_server[0].id
    
    if user_id=="":
        user_id="0"
    user_id=int(user_id)   
    
    query_where=" and 1=1"
    try:
        if sdate!="":
            sdate=datetime.datetime.strptime(sdate,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            query_where+=" and a.log_time>='%s'"%sdate
        if edate!="":
            edate=datetime.datetime.strptime(edate,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            query_where+=" and a.log_time<='%s'"%edate
    except:
        sdate=""
        edate=""
    
    logDefine = LogDefine.objects.get(key='silver')
    
    fieldDefine = FieldDefine.objects.get(log_type=logDefine.id,name=u'操作项目')
    incoming_list=ValueDefine.objects.filter(field_id=fieldDefine.id,value_id__lt=10000)
    silverType_Dic={}
    for inItem in incoming_list:
        silverType_Dic[inItem.value_id]=inItem.value
        if len(query_incoming)>0:
            if str(inItem.value_id) in query_incoming:
                inItem.is_show=True
            else: 
                inItem.is_show=False
        else:
            if request.method =="GET":
                inItem.is_show=True
            else: 
                inItem.is_show=False
    
    outcoming_list=ValueDefine.objects.filter(field_id=fieldDefine.id,value_id__gte=10000)
    for outItem in outcoming_list:
        silverType_Dic[outItem.value_id]=outItem.value
        if len(query_outcoming)>0:
            if str(outItem.value_id) in query_outcoming:
                outItem.is_show=True
            else: 
                outItem.is_show=False
        else:
            if request.method =="GET":
                outItem.is_show=True
            else: 
                outItem.is_show=False
    
    query_type=[]
    if len(query_incoming)>0:
        query_type=query_type+query_incoming
        
    if len(query_outcoming)>0:  
        query_type=query_type+query_outcoming
#     
#    if len(query_type)>0:
#        query_where+=" and log_data in (%s)"(','.join(query_type))
    
    server_in=""
    if len(query_type)>0:
        server_in="("
        for typeItem in query_type:
            if server_in=="(":
                server_in+="%s"%typeItem
            else:
                server_in+=",%s"%typeItem
        server_in+=")"
    
    if server_in!="" and len(query_type)!=(len(incoming_list)+len(outcoming_list)):
        query_where+=" and a.log_data in %s"%server_in
    
#    if user_name!="":
#        query_where+=" and b.f1=%s"%user_name    
        
    if server_id>0:    
        try:
            conn = getConn(server_id)
        except:
            err_msg = '数据库链接出错!'
            
    cursor = conn.cursor()
    
    if user_id<1:
        if user_name!="":
            query_role_sql="SELECT log_user FROM log_create_role WHERE f1='%s'"%user_name
            cursor.execute(query_role_sql)
            role_object=cursor.fetchone()
            if role_object!=None:
                user_id=int(role_object[0])
                
    if user_id>0:
        query_where+=" and a.log_user=%s"%user_id

    query_sql="SELECT a.log_user,b.f1,a.log_time,a.log_result,a.f2,a.log_data,a.f3 FROM log_silver a,log_create_role b WHERE a.log_user=b.log_user %s order by a.id desc"%query_where
    query_count_sql="SELECT count(1) FROM log_silver a where 1=1 %s"%query_where
    
    cursor.execute(query_count_sql)
    total_record=int(cursor.fetchone()[0])
    
    pager_str = 'limit %s,%s'%((page_num-1)*page_size,page_size)
    query_sql=query_sql+' '+pager_str
    
    print query_count_sql
    print query_sql
    
    cursor.execute(query_sql)     
    silver_list_temp = cursor.fetchall()
    
    fieldDefine_f3 = FieldDefine.objects.get(log_type=logDefine.id,name=u'备注')
    valueDefine_f3_list=ValueDefine.objects.filter(field_id=fieldDefine_f3.id)
    f3_dic={}
    for vdItem in valueDefine_f3_list:
        f3_dic[vdItem.value_id]=vdItem.value
    
    silver_list=[]
    for silverItem in silver_list_temp:
        role_name=""
        if silverItem[5]!="": 
            role_name=silverType_Dic[int(silverItem[5])]
        detail_name=""
        if silverItem[6]!="":
            detail_name=f3_dic[int(silverItem[6])] 
        silver_list.append((silverItem[0],silverItem[1],silverItem[2],silverItem[3],silverItem[4],silverItem[5],role_name,silverItem[6],detail_name))
     
    cursor.close()
    
    if user_id<1:
        user_id=""
    
    
    parg = {}
    parg["list_server"] = list_server
    parg["server_id"] = server_id
    parg["incoming_list"] = incoming_list
    parg["outcoming_list"] = outcoming_list
    parg["sdate"] = sdate
    parg["edate"] = edate
    parg["user_id"] = user_id
    parg["user_name"] = user_name
    parg["silver_list"] = silver_list
    
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    
    return render_to_response('player/player_silver_detail.html',parg)


def player_block(request,server_id=0,player_id=0):
    player_id = int(player_id)
    server_id = int(server_id)
    
    if player_id == 0:
        player_id = int(request.GET.get('player_id', '0'))
    
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))

    if player_id > 0 :
        try:
            conn = getConn(server_id)
            cursor = conn.cursor()
            if request.GET.get('is_lock','1')=='1':
                the_status = -1
            else:
                the_status = 0

            query_sql = 'update player_%d set status=%d where player_id=%d'%(server_id,the_status,player_id)
            
            print(query_sql)
            cursor.execute(query_sql)
            cursor.close()
        except Exception,e:
            raise Exception, e
            print('lock user error:',e)
    
    parg = {}
    parg["player_id"] = player_id
    parg["the_status"] = the_status

    return render_to_response('player/player_block.html',parg)

def player_list(request,server_id=0):
    page_size=30
    page_num=int(request.GET.get("page_num","1"))
    is_block = int(request.GET.get("block", 0))
    group_id = int(request.GET.get("group_id", 0))
    post_back = int(request.GET.get('post_back', '0'))
    
    list_group = center_cache.get_group_list()
        
    if(page_num<1):
        page_num=1
    
    usm = UserStateManager(request)
    the_user = usm.get_the_user() 
    
    
    list_channel= center_cache.get_channel_list()
    
    itemChannelList={}
    for item in list_channel:
        itemChannelList[item.id]=item.name
    
    list_group_server = [] 
    if group_id != 0: 
        list_group_server = center_cache.get_group_server_list(group_id)
    
    if usm.current_userRole_is_root():
        list_server = center_cache.get_server_list()
    else:
        list_server = center_cache.get_user_server_list(the_user)
    
    tmp_list_server = [] 
    if 0 != list_group_server.__len__():
        for item in list_group_server:
            if list_server.__contains__(item):
                tmp_list_server.append(item)
        list_server = tmp_list_server
        
    itemServerList = {}
    for item in list_server:
        itemServerList[item.id]=item.name
   
    player_key = request.GET.get('key','')
    key_type = request.GET.get('key_type','0')
    user_type = int(request.GET.get('user_type','-1'))
    channel_id = int(request.session.get('channelId','0'))
    
    server_id= int(request.GET.get("server_id","0"))
    
    if server_id<=0:
        server_id= int(request.session.get("serverId","0"))
    if server_id<=0 and len(list_server)>0:
        server_id=list_server[0].id
   
    #账号状态
    status_condition = 0
    if is_block == 1:
        status_condition = -1
    
    total_record=0
    player_list=[]
    player_list1=[]
    
    if 0 != post_back and  server_id>0: 
        conn = getConn(server_id)
        cursor = conn.cursor()
    
        query=[]
        query.append("status=%d" % status_condition)
        if channel_id>0:
            query.append('channel_id=%d'%channel_id)
      
        if player_key!="":
            if key_type=='0':
                query.append('player_id=\'%s\''%player_key)
            elif key_type=='1':
                query.append('player_name like \'%s%%\''%player_key.encode('utf-8'))
            elif key_type=='2':
                query.append('link_key=\'%s\''%player_key)
            elif key_type=='3':
                query.append('mobile_key=\'%s\''%player_key)
        if user_type>-1:
            query.append('user_type=%d'%player_key)
        
        if not usm.current_userRole_is_root():
            channel_list = center_cache.get_user_channel_list(the_user)
            channel_id_list_query = ' channel_id in (%s) ' % ','.join([str(item.id) for item in channel_list])
            query.append(channel_id_list_query)
            
        if len(query)>0:
            sql1='select count(1) from player_%d where %s'%(server_id,' and '.join(query))
            sql2='select player_id,player_name,channel_id,user_type,link_key,login_num,mobile_key,last_time,create_time,status from player_%d where %s order by id desc limit %d,%d'%(server_id,' and '.join(query),(page_num-1)*page_size,page_num*page_size)
        else:
            sql1='select count(1) from player_%d'%server_id
            sql2='select player_id,player_name,channel_id,user_type,link_key,login_num,mobile_key,last_time,create_time,status from player_%d order by id desc limit %d,%d'%(server_id,(page_num-1)*page_size,page_num*page_size)
        
        print(sql1,sql2)
        cursor.execute(sql1)
        count_list=cursor.fetchone()
        total_record=int(count_list[0])
        if total_record>0:
            cursor.execute(sql2)
            player_list1=cursor.fetchall()
        user_type_name = {0:'游爱',1:'当乐',2:'UC',3:'91',4:'云游',5:'飞流',6:'乐逗',8:'小虎',9:'4399',10:'facebook',11:'qq'}
        for item in player_list1:
            item = list(item)

            item[2]=itemChannelList.get(int(item[2]),item[2])
                
            item[3]=user_type_name.get(int(item[3]),item[3])
                 
            player_list.append(item)
        cursor.close()
    parg = {}
    parg["server_id"] = server_id
    parg["list_group"] = list_group
    parg["list_server"] = list_server
    parg["player_key"] = player_key
    parg["server_id"] = server_id
    parg["player_list"] = player_list
    parg["is_block"] = is_block
    parg["usm"] = usm
    
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    
    return render_to_response('player/player_list.html',parg)

#def player_info(request,playerId):
#    return render_to_response('player/player_info.html')
#
#
#def user_login(request):
#    from django.http import HttpResponse
#    import time
#    response = HttpResponse()
#    response['Content-Type']='application/json'
#    timestamp = int(time.time())
#    return render_to_response('player/user_login.html',locals())
