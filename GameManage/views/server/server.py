#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.models.center import Server, Group, Notice, Channel
from django.db import connections
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from GameManage.views.base import UserStateManager, OperateLogManager, get_server_list
from GameManage.enum import ENUM_SERVER_STATUS
from GameManage.cache import center_cache

import os, json, copy, datetime

def server_list(request, group_id=0):
    group_id = int(group_id)
    if group_id == 0:
        group_id = int(request.GET.get('group_id', '0'))
    list_group = Group.objects.using('read').all()
    if group_id > 0:
        list_record = Server.objects.using('read').filter(group__id=group_id).order_by("-status", "create_time")
    else:
        list_record = Server.objects.using('read').all().order_by("-status", "create_time")
    
    STATUS_CHOICES = Server.STATUS_CHOICES
    
    parg = {}
    parg["group_id"] = group_id
    parg["list_group"] = list_group
    parg["STATUS_CHOICES"] = STATUS_CHOICES
    parg["list_record"] = list_record
    
    return render_to_response('server/server_list.html', parg)

def server_make(request):
    list_group = Group.objects.using('read').all()
    rootPath = os.path.dirname(__file__)
    if True:
#    try:
        folderPath = os.path.abspath(os.path.join(rootPath, '../../../static/server/'))
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)
        #clear old file
        for file_item in os.listdir(folderPath):
            try:
                itemsrc = os.path.join(folderPath, file_item)
                if os.path.isfile(itemsrc):
                    os.remove(itemsrc)
            except:
                pass
         
        list_server = get_server_list()
        
        serverList = []
        for item in list_server:
            mongo_port = 27017
            #f item.json_data.find('master_server_id')!=-1:
                #continue #子服不需要生成
            db_address = ''
            mongo_port = 27017
            if item.log_db_config != '':
                try:
                    db_config = json.loads(item.log_db_config)
                except:
                    continue
                mongo_port = db_config.get('mongo_port', 27017)
                db_address = db_config.get('db_addr',item.game_addr)
            
            if None != item.report_url and '' != item.report_url:
                item.report_url = item.report_url.replace('http://', '')
                item.report_url = item.report_url.replace('/', '')
                
                
            serverList.append(u'{"id":%d,"name":"%s","address":"%s","db_address": "%s","gate_port":%d,"db_port":%d,"status":%d,"battle_report_url":"%s"}' % 
                            (item.id, item.name, item.game_addr, db_address, item.game_port, mongo_port, item.status, item.report_url))
           
        #生成GM LIST    
        filePath = os.path.join(folderPath, 'GM.json')
        fileContent = '[%s]' % ','.join(serverList)
        file_handler = open(filePath, "w")
        file_handler.write(fileContent.encode('utf-8'))
        file_handler.close()
            
        
        for item_group in list_group:
            serverList = []
            noticeContent = ''
            list_server = item_group.server.filter(Q(status__gt=0, group__id=item_group.id))
            for item in list_server:
                if item.json_data == None:
                    item.json_data = '' 
                serverList.append(u'{"id":%d,"name":"%s","address":"%s", "port":%d,"state":%d,"brUrl":"%s","rqVer":%d,"commend":%d,"limitVer":[%s],"other":{%s},"order":%d}' % 
                                (item.id, item.name, item.game_addr,  item.game_port, item.status, item.report_url, item.require_ver, item.commend, item.client_ver,item.json_data,item.order))
                
            
            #当前分区公告
            notices = Notice.objects.using('read').filter(id=item_group.notice_select)
            if len(notices) > 0:

                the_notice = notices[0]
                
                size_str = '0.7,0.8'
                if None != the_notice.size and '' != the_notice.size:
                    size_str = the_notice.size
                
                
                noticeContent = u",\"notice\":{\"beginDate\":\"%s\",\"endDate\":\"%s\",\"title\":\"%s\",\"size\":[%s],\"positioin\":[-1,-1],\"url\":\"%s\"}" % (the_notice.begin_time,
                                                                                  the_notice.end_time,
                                                                                  the_notice.title,
                                                                                  size_str,
                                                                                  the_notice.link_url)
            
            fileContent = u'{"serverList":[%s],"payUrl":"%s","customUrl":"%s","noticeUrl":"%s","upgradeUrl":"%s"%s}' % (','.join(serverList), item_group.pay_url, item_group.custom_url, item_group.notice_url, item_group.upgrade_url, noticeContent)
            
            filePath = os.path.join(folderPath, '%s.json' % item_group.key)
            
            file_handler = open(filePath, "w")
            file_handler.write(fileContent.encode('utf-8'))
            file_handler.close()   
#    except Exception, e:
#        print('write server list has error:%s' % e)
    return render_to_response('feedback.html')

def server_edit(request, server_id=0):
    server_id = int(server_id)
    
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))
    
    model = None
    
    if server_id > 0:
        model = Server.objects.using('read').get(id=server_id)
    if model == None:
        model = Server()
        model.id = 0
    
    list_channel = center_cache.get_channel_list()
    if model.id > 0:
        list_channel_selected = model.channel.all()
        channel_selected = {}
        for item in list_channel_selected:
            channel_selected[item.id] = 1
        for item in list_channel:
            item.is_show = channel_selected.get(item.id, 0)
    
    parg = {}
    parg["model"] = model
    parg["list_channel"] = list_channel
    
    return render_to_response('server/server_edit.html', parg)

def server_status_edit(request):
    server_list = request.POST.getlist('serv_id')
    
    
    if server_list == '' or 0 == server_list.__len__():
        return HttpResponse('没有选择服务器')
        
    
    status = int(request.POST.get('serv_status', '-99'))
    if status == -99:
        return HttpResponse('没有保存，请选择状态')
    
    update_sql = " UPDATE `servers` SET `status` = %d WHERE `id` IN (%s) " % (status, ','.join(server_list))
    print server_list
    try:
        local_cursor = connections['write'].cursor()
        local_cursor.execute(update_sql)
    except Exception, e:
        return HttpResponse('出错了错误信息是: %s' % e)
 
    return HttpResponse('修改成功')

def server_save(request, server_id=0): 
    server_id = int(server_id)
    new_server_id = int(request.POST.get('new_server_id', '0'))
    model = None
    source_model = None
    is_add = True
    if server_id==0:
        server_id = int(request.GET.get('server_id', '0'))
    if server_id > 0:
        model = Server.objects.using('write').get(id=server_id)
        source_model = copy.copy(model)
        is_add = False
    if model == None:
        model = Server()
        model.id = new_server_id
    
    exists = False
    update_id = False
    err_msg = ''
    
    if server_id != new_server_id:
        is_exists = Server.objects.all().filter(id = new_server_id)
        if is_exists.__len__() > 0:
            exists = True
            err_msg = '保存的服务器ID已存在'
        else:
            update_id = True
            
    model.client_ver = request.POST.get('client_ver', '')
    model.name = request.POST.get('name', '')
    model.status = int(request.POST.get('status', '2'))
    model.commend = int(request.POST.get('commend', '2'))
    model.require_ver = int(request.POST.get('require_ver', '0'))
    model.game_addr = request.POST.get('game_addr', '')
    model.game_port = int(request.POST.get('game_port', '2008'))
    model.report_url = request.POST.get('report_url', '')
    model.log_db_config = request.POST.get('log_db_config', '')
    model.remark = request.POST.get('remark', '')
    model.order = int(request.POST.get('order', '0'))
    model.json_data = request.POST.get('json_data', '')
    create_time = request.POST.get('create_time', '')
    if create_time == '':
        create_time = datetime.datetime.now()
    else:
        create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    model.create_time = create_time
    
    #保存详细操作日志
    save_server_log(server_id, is_add, request, source_model, model)
      
    template_html = 'server/server_edit.html'
    
    if not exists:
        if model.name != '' and model.game_addr != '':
            try:
                #修改ID
                old_server = copy.copy(model)
                if update_id:
                    model.id = new_server_id
                
                if model.id > 0:
                    model.channel.clear()
                model.save(using='write')
                
                
                for channel_id in request.POST.getlist('channel_id'): 
                    channel_id = int(channel_id) 
                    model.channel.add(Channel.objects.using('write').get(id=channel_id))
                
                #前面保存没有出错
                if update_id:
                    old_server.status = ENUM_SERVER_STATUS.DELETED
                    old_server.save(using='write')
                
                 
                return HttpResponseRedirect('/server/list')
            except Exception, e:
                err_msg = '未知错误%s' % e
                
        else:
            err_msg = '表填写必要数据'
         
    parg = {}
    parg["model"] = model
    parg["err_msg"] = err_msg
    
    return render_to_response(template_html, parg)

def save_server_log(server_id ,is_add, request, source, target):
    the_user_id = UserStateManager.get_the_user_id(request)
    ip = OperateLogManager.get_request_ipAddress(request)
    request_path = '/server/save/%s' % server_id
    if not is_add:
        save_modify_server_log(source, target, the_user_id, ip, request_path)
    else: 
        OperateLogManager.save_operate_log(the_user_id, '新建服务器', request_path, ip)


def save_modify_server_log(source, target, the_user_id, ip, request_path) :
    msg = []
    if source.client_ver !=  target.client_ver :
        msg.append(u'客户端版本')
    if source.name != target.name:
        msg.append(u'名称')
    if source.status !=  target.status :
        msg.append(u'状态')
    if source.commend !=  target.commend :
        msg.append(u'推荐')
    if source.require_ver  != target.require_ver:
        msg.append(u'最低版本') 
    if source.game_addr != target.game_addr :
        msg.append(u'ip')
    if source.game_port != target.game_port :
        msg.append(u'port')
    if source.report_url != target.report_url :
        msg.append(u'url')
    if source.log_db_config != target.log_db_config :
        msg.append(u'db_config') 
    if source.remark != target.remark :
        msg.append(u'备注') 
    if source.order != target.order :
        msg.append(u'排序')
    if source.json_data !=  target.json_data :
        msg.append(u'json_data')
    if source.create_time != target.create_time :
        msg.append(u'开服时间')
    
    if msg.__len__() == 0:
        str_msg = '无修改'
    else:
        str_msg =  ','.join(msg) 
        
    OperateLogManager.save_operate_log(the_user_id, str_msg, request_path, ip)
    

def server_remove(request, model_id=0):
    model_id = int(model_id)
    
    if model_id > 0 :
        try:
            model = Server.objects.using('write').get(id=model_id)
            model.channel.clear()
            model.delete(using='write')
        except Exception, e:
            print('server remove error:', e)
    return render_to_response('feedback.html')
