#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.models.center import  Group, Upgrade, Channel
from django.http import HttpResponseRedirect, HttpResponse
from GameManage.cache import center_cache
import os

#更新设置
def upgrade_list(request):
    
    group_id = int(request.GET.get('group_id', 0))
    
    list_group = center_cache.get_group_list()
    
    list_record = []
    if group_id == 0:
        list_record = Upgrade.objects.all()
    else:
        list_record = Upgrade.objects.filter(group__id=group_id)
    
    parg = {}
    parg["list_record"] = list_record
    parg["list_group"] = list_group
    parg["group_id"] = group_id
    
    return render_to_response('server/upgrade_list.html', parg)

def upgrade_clear(request):
    list_group = Group.objects.using('read').all()
    rootPath = os.path.dirname(__file__)
    
    for item_group in list_group:
        folderPath = os.path.abspath(os.path.join(rootPath, '../../../static/upgrade/%s/' % item_group.key))
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
    return render_to_response('feedback.html')

def upgrade_make(request,model_id=0):
    list_upgrade = Upgrade.objects.using('read').all()
    rootPath = os.path.dirname(__file__)
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('model_id', '0'))
    
    is_ajax = False
    if '1' == request.GET.get('ajax', '0'):
        is_ajax = True
#    if True:
    try:

        for item in list_upgrade:
            
            if model_id > 0 and model_id != item.id:
                continue
            
            upgradeInfo = u'{"newVerCode":%d,"newVerName":"%s","apkSize":"%s","apkDlLink":%s,"verMsg":"%s","updateLink":"%s","clientVer":[%s]}' % (item.ver_num, item.ver_name, item.filesize, item.download_url, item.remark, item.page_url, item.client_ver)
            fileContent = upgradeInfo.encode('utf-8')

            for item_group in item.group.all():
                
                folderPath = os.path.abspath(os.path.join(rootPath, '../../../static/upgrade/%s/' % item_group.key))
                if not os.path.exists(folderPath):
                    os.mkdir(folderPath)
                
                for item_channel in item.channel.all():
                    filePath = os.path.join(folderPath, '%s.json' % item_channel.key)
                    if os.path.exists(filePath):
                        if os.path.isfile(filePath):
                            os.remove(filePath)
                    file_handler = open(filePath, "w")
                    file_handler.write(fileContent)
                    file_handler.close()   

    except Exception, e:
        print('write server list has error:%s' % e)
    
    if is_ajax:
        return HttpResponse('{"code":0}')
    return render_to_response('feedback.html')


def upgrade_edit(request, model_id=0):
    model_id = int(model_id)
    
    if model_id == 0:
        model_id = int(request.GET.get('model_id', '0'))
    
    model = None
    if model_id > 0:
        model = Upgrade.objects.using('read').get(id=model_id)
        
    channel_list = center_cache.get_channel_list()
    group_list = center_cache.get_group_list()
    if model == None:
        model = Upgrade()
        model.id = 0
    else:
        model.remark = model.remark.replace('\\n', '\r\n')
        
        list_channel_selected = model.channel.all()
        channel_selected = {}
        for item in list_channel_selected:
            channel_selected[item.id] = 1
        for item in channel_list:
            item.is_show = channel_selected.get(item.id, 0)
                
        for item in group_list:
            if len(model.group.filter(id=item.id)) > 0:
                item.is_show = 1
            else:
                item.is_show = 0
    
    parg = {}
    parg["model"] = model
    parg["channel_list"] = channel_list
    parg["group_list"] = group_list
                
    return render_to_response('server/upgrade_edit.html', parg)

def upgrade_save(request, model_id=0):
    model_id = int(model_id)
    
    if model_id == 0:
        model_id = int(request.GET.get('model_id', '0'))
    
    model = None
    if model_id > 0:
        model = Upgrade.objects.using('write').get(id=model_id)
    if model == None:
        model = Upgrade()
        #model.id = 0
    
    model.client_ver = request.POST.get('client_ver', '')
    model.ver_num = int(request.POST.get('ver_num', '0'))
    model.ver_name = request.POST.get('ver_name', '')
    model.download_url = request.POST.get('download_url', '')
    model.filesize = request.POST.get('filesize', '')
    model.page_url = request.POST.get('page_url', '')
    model.remark = request.POST.get('remark', '').replace('\r', '').replace('\n', '\\n')
    model.create_time = request.POST.get('create_time', '')
    model.pub_ip = request.META.get('REMOTE_ADDR', '')
    model.pub_user = int(request.session.get('userid', '0'))
    if True:
#    try:

        if model.id > 0:
            model.channel.clear()
            model.group.clear()
        model.save(using='write')
        for channel_id in request.POST.getlist('channel_id'): 
            channel_id = int(channel_id)
            model.channel.add(Channel.objects.using('write').get(id=channel_id))
        for group_id in request.POST.getlist('group_id'): 
            group_id = int(group_id)
            model.group.add(Group.objects.using('write').get(id=group_id))
        return HttpResponseRedirect('/upgrade/list')
#    except Exception,e:
#        print('upgrade save error:',e)
    
    
    parg = {}
    parg["model"] = model

    return render_to_response('server/upgrade_edit.html', parg)

def upgrade_remove(request, model_id=0):
    model_id = int(model_id)
    
    if model_id == 0:
        model_id = int(request.GET.get('model_id', '0'))
    
    if model_id > 0 :
        try:
            model = Upgrade.objects.using('write').get(id=model_id)
            model.channel.clear()
            model.delete(using='write')
        except Exception, e:
            print('upgrade remove error:', e)
    return render_to_response('feedback.html')

