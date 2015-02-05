#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.views.base import UserStateManager, get_server_list
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, Template
from GameManage.models.center import Server, Notice, Group, Channel
from GameManage.models.admin import Admin
from GameManage.cache import center_cache
from GameManage.views.base import GlobalPathCfg
import os, time

#游戏公告
def notice_list(request, notice_type=0):
    server_id = int(request.GET.get('server_id', 0))
    
    usm = UserStateManager(request)
    the_user = usm.get_the_user()
    
    if the_user.id == 0:
        server_list = get_server_list()
    else:
        server_list = the_user.server.all()
        if server_list.__len__() == 0:
            server_list = get_server_list()
        else:
            if server_id <= 0:
                server_id = server_list[0].id
     
    if server_list.__len__() == 0:
        return HttpResponse("没有服务器可管理")
    
    if server_id > 0:
        if notice_type >0:
            list_record = Notice.objects.using('read').filter(server = server_id, notice_type= notice_type)
        else:
            list_record = Notice.objects.using('read').filter(server = server_id)
    else:
        if notice_type > 0:
            list_record = Notice.objects.using('read').filter(notice_type=notice_type)
        else:
            list_record = Notice.objects.using('read').all()
    
    template_path = 'server/notice_list.html'
    if notice_type == 4:
        template_path = 'server/push_list.html'
    
    parg = {}
    parg["server_list"] = server_list
    parg["server_id"] = server_id
    parg["list_record"] = list_record
    parg["usm"] = usm
     
    return render_to_response(template_path, parg)

def notice_edit(request, model_id=0, notice_type=0):
    model_id = int(model_id)
    
    if model_id == 0:
        model_id = int(request.GET.get('notice_id', '0'))
    
    model = None
    if model_id > 0:
        model = Notice.objects.using('write').get(id=model_id)
        notice_type = model.notice_type
    if model == None:
        model = Notice()
        model.id = 0
    
    if model.size == None:
        model.size = ''
#    channel_list = Channel.objects.all()
#    if model.id>0:
#        for item in channel_list:
#            if len(model.channel.filter(id=item.id))>0:
#                item.is_show=1
#            else:
#                item.is_show=0
    
    the_user_id = int(request.session.get('userid', '0'))
    the_user = Admin.objects.using('write').get(id=the_user_id)
    
    list_server = []
    list_group = []
    list_channel = []
    if notice_type == 4:
        list_group = Group.objects.using('write').all()
        if model.id > 0:
            list_group_selected = model.group.all()
            group_selected = {}
            for item in list_group_selected:
                group_selected[item.id] = 1
            for item in list_group:
                item.is_show = group_selected.get(item.id, 0)
    else:
        
        if the_user == 0:
            list_server = get_server_list()
        else:
            list_server = the_user.server.all()
            if list_server.__len__() == 0:
                list_server = get_server_list()
        
        if model.id > 0:
            list_server_selected = model.server.all()
            server_selected = {}
            for item in list_server_selected:
                server_selected[item.id] = 1
            for item in list_server:
                item.is_show = server_selected.get(item.id, 0)
    
    list_channel = center_cache.get_channel_list()
    
    list_channel_selected = model.channel.all()
    channel_selected = {} 
    for item in list_channel_selected:
        channel_selected[item.id] = 1
    for item in list_channel:
        item.is_show = channel_selected.get(item.id, 0)
    
    
    template_path = 'server/notice_edit.html'
    if notice_type == 4:
        template_path = 'server/push_edit.html'
    
    parg = {}
    parg["notice_type"] = notice_type
    parg["model"] = model
    parg["list_server"] = list_server
    parg["list_group"] = list_group
    parg["list_channel"] = list_channel
    return render_to_response(template_path, parg)

def notice_save(request, model_id=0):
    model_id = int(model_id)
    title = request.POST.get('title', '').replace('\n', '\\n').replace('\r', '')
    content = request.POST.get('content', '')
    post_list_server = request.POST.getlist('server_id')
    post_list_channel = request.POST.getlist('channel_id')
    usm = UserStateManager(request)
    link_url = request.POST.get('link_url', '')
    import re
    size = request.POST.get('size', '')
    if re.sub('[\-\d+\,\.]+','',size) != '':
        size = ''
        
    allow_create = True
    #权限判断   //如果不是管理员账号
    if not usm.current_userRole_is_root():
        the_user = usm.get_the_user()
        user_server_list = the_user.server.all()#获取当前登陆的管理员账号有权限管理的服务器列表
        user_server_id = []
        for user_server in user_server_list:
            user_server_id.append(user_server.id)
        
        #添加公告的服务器不在当前登陆角色的服务器列表内，则作为没有权限操作
        for server_id in post_list_server:
            if not user_server_id.__contains__(int(server_id)):
                allow_create = False
                break
    if not allow_create:
        return HttpResponse('没有权限添加')
    
    
    if model_id == 0:
        model_id = int(request.GET.get('notice_id', '0'))
    
    model = None
    if model_id > 0:
        model = Notice.objects.using('write').get(id=model_id)
    if model == None:
        model = Notice()
        #model.id = 0
    
    notice_type = int(request.POST.get('type', '0'))
    
    model.client_ver = request.POST.get('client_ver', '')
    model.status = int(request.POST.get('status', '0'))
    model.pub_ip = request.META.get('REMOTE_ADDR', '')
    model.pub_user = int(request.session.get('userid', '0'))
    model.size = size
    model.link_url = link_url
    model.title = title
    model.content = content
    model.begin_time = request.POST.get('begin_time', '')
    model.end_time = request.POST.get('end_time', '')
    model.notice_type = notice_type
    model.intervalSecond = int(request.POST.get('intervalSecond', '0'))
    ajax_post = request.POST.get('ajax', False)
    
    try:
        if model.id > 0:
            model.server.clear()
            model.group.clear()
            model.channel.clear()
        model.save(using='write')
        
        
        #如果不是"游戏滚动公告" 和 “推送消息”则生成静态文件
        
        if link_url == '' and notice_type != 1 and notice_type != 4:
            link_url = create_notice_html(request, model.id, title, content)
            model.link_url = link_url
            model.save()
        
#        for channel_id in request.POST.getlist('channel_id'): 
#            channel_id = int(channel_id)
#            model.channel.add(Channel.objects.get(id=channel_id))
        for server_id in post_list_server: 
            server_id = int(server_id)
            model.server.add(Server.objects.using('write').get(id=server_id))
            
        for group_id in request.POST.getlist('group_id'): 
            group_id = int(group_id)
            model.group.add(Group.objects.using('write').get(id=group_id))
        
        list_channel = Channel.objects.using('write').all()
        
        for channel_id in post_list_channel:
            channel_id = int(channel_id)
            for item in list_channel:
                if item.id == channel_id:
                    model.channel.add(item)
        
        if ajax_post:
            return HttpResponse("保存成功！");
        return HttpResponseRedirect('/notice/list')
    except Exception, e: 
        print('notice save error:', e)
        if ajax_post:
            return HttpResponse("保存出错请重试！出错信息:%s" % e)
    
    parg = {}
    parg["model"] = model 
    
    return render_to_response('server/notice_edit.html', parg)

def create_notice_html(request, model_id, title, content):
    gl_path = GlobalPathCfg()
    file_name = '%s.html' % model_id
    file_url = gl_path.get_notice_html_url(request, file_name)
    save_path = gl_path.get_notice_html_save_path(file_name) 
    file_tpl = open(gl_path.get_notice_html_template_path(), 'r')
    tpl_content = file_tpl.read()
    file_tpl.close()
    t = Template(tpl_content)
    html_file = open (save_path, 'w')
    c = Context({"title":title, "content": content}) 
    c = t.render(c)
    html_file.write(c.encode('utf-8'))
    html_file.close()
    return file_url

def push_create(request):
    
    usm = UserStateManager(request)
    #需要管理员账号
    if not usm.current_userRole_is_root():
        return HttpResponse(u'没有权限操作')
    
    list_content = {}
    list_push = Notice.objects.filter(notice_type=4)
    rootPath = os.path.dirname(__file__)
    try:
        folderPath = os.path.abspath(os.path.join(rootPath, '../../../static/notice/push'))
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)
        
        
        for model in list_push:
            title = model.title
            content = model.content
            fileContent = '{"id":%d,"title":"%s","message":"%s","url":"%s","time":"%s","version":[%s]}' % (model.id,
                                                                            title,
                                                                            content,
                                                                            model.link_url.encode('utf-8'),
                                                                            int(time.mktime(model.begin_time.timetuple()) * 1000),
                                                                            model.client_ver.encode('utf-8'))
            for server in model.group.all():
                if list_content.get(server.key, None) == None:
                    list_content[server.key] = []
                
                list_content[server.key].append(fileContent)
        print(list_content)       
        for item in list_content:
            filePath_template = os.path.abspath(os.path.join(rootPath, '../../../static/notice/push/%s.json'))
            filePath = filePath_template % item
            file_handler = open(filePath, "w")
            file_handler.write('[%s]' % (','.join(list_content[item])))
            file_handler.close()   
            
    except Exception, e:
        print('create push file:', e)
    
    return render_to_response('feedback.html')
    
def notice_createStaticFile(request, model_id=0):
    
    model_id = int(model_id)
    
    if model_id == 0:
        model_id = int(request.GET.get('notice_id', '0'))
    msg = u'成功'
    if model_id > 0:
        filePath_template = ""
        fileContent = ""
        filePath = ""
        
        try:
            model = Notice.objects.using('write').get(id=model_id)
            
            model_server_list = model.server.all()
            model_channel_list = model.channel.all()
            usm = UserStateManager(request)
            
            allow_create = True
            #权限判断   //如果不是管理员账号
            if not usm.current_userRole_is_root():
                the_user = usm.get_the_user()
                user_server_list = the_user.server.all()#获取当前登陆的管理员账号有权限管理的服务器列表
                
                #需要生成公告的服务器不在当前登陆角色的服务器列表内，则作为没有权限操作
                for model_server in model_server_list:
                    if not user_server_list.__contains__(model_server):
                        allow_create = False
                        break
            if not allow_create:
                return HttpResponse('没有权限生成')
            
            rootPath = os.path.dirname(__file__)
            
            
            if model.notice_type == 1:
                filePath_template = os.path.abspath(os.path.join(rootPath, '../../../static/notice/scroll/%s/'))
                
                
                
                fileContent = "{\"beginDate\":\"%s\",\"endDate\":\"%s\",\"intervalSecond\":%s,\"txt\":\"%s\"}" % (model.begin_time,
                                                                                  model.end_time,
                                                                                  model.intervalSecond,
                                                                                  model.title.encode('utf-8'))

            if model.notice_type == 2:
                size_str = '0.7,0.8'
                if None != model.size and '' != model.size:
                    size_str = model.size
                
                filePath_template = os.path.abspath(os.path.join(rootPath, '../../../static/notice/game/%s/'))
                fileContent = "{\"beginDate\":\"%s\",\"endDate\":\"%s\",\"title\":\"%s\",\"size\":[%s],\"positioin\":[-1,-1],\"url\":\"%s\"}" % (model.begin_time,
                                                                                  model.end_time,
                                                                                  model.title.encode('utf-8'),
                                                                                  size_str.encode('utf-8'),
                                                                                  model.link_url.encode('utf-8'))

            if model.notice_type == 3:
                size_str = '0.7,0.8'
                if None != model.size and '' != model.size:
                    size_str = model.size
                filePath_template = os.path.abspath(os.path.join(rootPath, '../../../static/notice/login/%s/'))
                fileContent = "{\"beginDate\":\"%s\",\"endDate\":\"%s\",\"title\":\"%s\",\"size\":[%s],\"positioin\":[-1,-1],\"url\":\"%s\"}" % (model.begin_time,
                                                                                  model.end_time,
                                                                                  model.title.encode('utf-8'),
                                                                                  size_str.encode('utf-8'),
                                                                                  model.link_url.encode('utf-8'))
            
            for ser in model_server_list:
                filePath = filePath_template % ser.id
                if not os.path.exists(filePath):
                    os.mkdir(filePath)
                for channel in model_channel_list:
                    fp = '%s/%s.json' % (filePath, channel.key)
                    file_handler = open(fp, "w")
                    file_handler.write(fileContent)
                    file_handler.close()   
        except Exception, e:
            msg = u'失败,原因 %s' % e
            print('notice createStaticFile error:', e)
    
    return HttpResponse(msg);

def notice_remove(request, model_id=0):
    model_id = int(model_id)
    
    if model_id == 0:
        model_id = int(request.GET.get('notice_id', '0'))
    if model_id > 0 :
        try:
            model = Notice.objects.using('write').get(id=model_id)
            try:
                rootPath = os.path.dirname(__file__)
                if model.notice_type == 4:
                    for group in model.group.all(): 
                        filePath_template = os.path.abspath(os.path.join(rootPath, '../../../static/notice/push/%s.json' % group.key))
                        os.remove(filePath_template)
                else:
                    for item in model.server.all():
                        print os.path.join(rootPath, '../../../static/notice/%s/%s.json' % ({1:'scroll', 2:'game', 3:'login', 4:'push'}.get(model.notice_type, ''), item.id))
                        filePath_template = os.path.abspath(os.path.join(rootPath, '../../../static/notice/%s/%s.json' % ({1:'scroll', 2:'game', 3:'login', 4:'push'}.get(model.notice_type, ''), item.id)))
                        os.remove(filePath_template)
            except:
                print('delete file error')
            model.server.clear()
            model.delete(using='write')
        except Exception, e:
            print('notice remove error:', e)
    return render_to_response('feedback.html')


