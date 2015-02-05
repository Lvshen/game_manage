#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.models.center import Server, Group, Notice
from django.http import HttpResponseRedirect, HttpResponse
from GameManage.views.base import UserStateManager, OperateLogManager, get_server_list
import copy

def group_list(request):
    list_record = Group.objects.using('read').all()
    list_notice = Notice.objects.using('read').filter(notice_type=3)
    
    parg = {}
    parg["list_record"] = list_record
    parg["list_notice"] = list_notice
    
    return render_to_response('server/group_list.html', parg)

def group_edit(request, model_id=0):
    model_id = int(model_id)
    if model_id == 0:
        model_id = int(request.GET.get('model_id', '0'))
    
    model = None

    if model_id > 0:
        model = Group.objects.using('read').get(id=model_id)
    if model == None:
        model = Group()
        model.id = 0
    
    list_server = get_server_list()

    if model.id > 0:
        list_server_selected = model.server.all()
        server_selected = {}
        for item in list_server_selected:
            server_selected[item.id] = 1
        for item in list_server:
            item.is_show = server_selected.get(item.id, 0)
    
    
    list_notice = Notice.objects.using('read').filter(notice_type=3)
    
    parg = {}
    parg["model"] = model
    parg["list_server"] = list_server
    parg["list_notice"] = list_notice 
    
    return render_to_response('server/group_edit.html', parg)

def group_save(request, model_id=0):
    #是否只修改公告(用于批量修改) 
    only_updateNotice = request.POST.get('notice', False)
    
    model_id = int(model_id)
    if model_id == 0:
        model_id = int(request.GET.get('model_id', '0'))
    
    model = None 
    if model_id > 0:
        model = Group.objects.using('write').get(id=model_id)
    if model == None:
        model = Group() 
    
    source_model = copy.copy(model)
    
    if not only_updateNotice:
        model.key = request.POST.get('key', '')
        model.name = request.POST.get('name', '')
        model.custom_url = request.POST.get('custom_url', '')
        model.pay_url = request.POST.get('pay_url', '')
        model.upgrade_url = request.POST.get('upgrade_url', '')
        model.notice_url = request.POST.get('notice_url', '')
        model.notice_select = request.POST.get('notice_select', '0')
        model.remark = request.POST.get('remark', '').replace('\n', '\\n')
    else:
        model.notice_select = request.POST.get('notice_select', '')
        model.save() 
        return HttpResponse("保存成功！")
    
     
    ajax_post = request.POST.get('ajax', False)
    
    
    try:
        is_updateServerList = False
        
        
        post_server_list = request.POST.getlist('server_id')
        
        source_server_list = []
        if model.id > 0:
            model.server.clear()
            if post_server_list.__len__() != model.server.count():
                source_server_list = model.server.all().values('id') 
                is_updateServerList = True
        model.save(using='write')
          
        for server_id in post_server_list: 
            server_id = int(server_id)
            model.server.add(Server.objects.using('write').get(id=server_id))
            
        save_group_modify_log(request, source_model, model, is_updateServerList, post_server_list, source_server_list)    
        
        if ajax_post:
            return HttpResponse("保存成功！")
        
        return HttpResponseRedirect('/group/list')
    except Exception, e:
        raise Exception ,e
        if ajax_post:
            return HttpResponse("保存出错，请重试")
        print('group save error:', e)
    
    
    parg = {}
    parg["model"] = model
    
    return render_to_response('server/group_edit.html', parg)

def save_group_modify_log(request, source, target, is_updateServerList, post_server_list, source_server_list):
    admin_id = UserStateManager.get_the_user_id(request)
    msg = [] 
    
    msg_str = u"没有操作"
    
    if source.key != target.key:
        msg.append('key')
    if source.name != target.name:
        msg.append('name')
    if source.custom_url != target.custom_url: 
        msg.append('custom_url')
    if source.pay_url != target.pay_url: 
        msg.append('pay_url')
    if source.upgrade_url != target.upgrade_url:
        msg.append('upgrade_url')
    if source.notice_url != target.notice_url:
        msg.append('notice_url')
    if int(source.notice_select) != int(target.notice_select):
        msg.append('notice_select')
    if source.remark != target.remark:
        msg.append('remark')
    
    if is_updateServerList:
        msg.append(u'server(') 
        tmp_list = [] 
        for item in source_server_list: 
            tmp_list.append(str(item['id'])) 
        msg.append(','.join(tmp_list))
        msg.append(':')
        msg.append(','.join(post_server_list))
        msg.append(')')
    
    if msg.__len__() != 0:
        msg_str = ','.join(msg)
    
    request_path = 'group/save/%s' % source.id
    
    OperateLogManager.save_operate_log(admin_id, msg_str, request_path, OperateLogManager.get_request_ipAddress(request))

def group_remove(request, model_id=0):
    model_id = int(model_id)
    
    if model_id > 0 :
        try:
            model = Group.objects.using('write').get(id=model_id)
            model.server.clear()
            model.delete(using='write')
        except Exception, e:
            print('group remove error:', e)
    return render_to_response('feedback.html')
