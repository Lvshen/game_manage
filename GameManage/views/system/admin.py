#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from admin_status import admin_status
from GameManage.models.admin import Admin, Role
from GameManage.models.center import Channel, Server
from GameManage.views.base import get_server_list
from django.http import HttpResponseRedirect
from GameManage.cache import center_cache
import datetime

def admin_list(request):
    status = request.GET.get('status', '')
    is_remove_list = False
    if status == '':
        status = admin_status.NORMAL
    elif status == 'del':
        status = admin_status.DEL
        is_remove_list = True
    list_record = Admin.objects.using('read').filter(status=status)
    
#    for si in list:
#        if si.id==1:
#            print si.server.all()[0].name
    
    parg = {}
    parg["is_remove_list"] = is_remove_list
    parg["list_record"] = list_record
    
    return render_to_response('system/admin_list.html', parg)

def admin_edit(request, admin_id=0):
    admin_id = int(admin_id)
    if 0 == admin_id:
        admin_id = int(request.GET.get('admin_id', request.POST.get('admin_id', 0)))
    
    if admin_id > 0:
        model = Admin.objects.using('read').get(id=admin_id)
        model.password = ''
    else:
        model = Admin()
        model.id = admin_id
    
    roles = Role.objects.using('read').all()
    
    list_server = get_server_list()
    
    list_channel = center_cache.get_channel_list()
    item = []
    if model.id > 0: 
        #******设置服务器状态是否选中 ***********
        list_server_selected = model.server.all()
        server_selected = {}
        for item in list_server_selected:
            server_selected[item.id] = 1
        for item in list_server:
            item.is_show = server_selected.get(item.id, 0)
        #********   设置服务器状态 END *****************
        
        #*******设置渠道 状态是否选中 ***********
        
        list_channel_selected = model.channel.all()
        channel_selected = {}
        for item in list_channel_selected:
            channel_selected[item.id] = 1
        for item in list_channel:
            item.is_show = channel_selected.get(item.id, 0)
        
        #********   设置渠道状态END ***********
    
    parg = {}
    parg["item"] = item
    parg["roles"] = roles
    parg["list_server"] = list_server
    parg["list_channel"] = list_channel
    parg["model"] = model
    
    return render_to_response('system/admin_edit.html', parg)


def admin_save(request, admin_id=0):
    admin_id = int(admin_id)
    if 0 == admin_id:
        admin_id = int(request.GET.get('admin_id', request.POST.get('admin_id', 0)))
    
    if admin_id > 0:
        the_admin = Admin.objects.using('write').get(id=admin_id)
    else:
        the_admin = Admin()
    print the_admin.last_time 
    the_admin.role = Role.objects.using('write').get(id=int(request.POST.get('role_id', '0')))   
    the_admin.username = request.POST.get('username', '')
    tmp_password = request.POST.get('password', '')
    if tmp_password != '':
        the_admin.password = tmp_password
        the_admin.password = the_admin.md5_password()
    err_msg = None

    #验证数据
    if the_admin.username != "" and (the_admin.password != "" or admin_id > 0):
        if the_admin.id > 0:
            the_admin.server.clear()
            the_admin.channel.clear()
        the_admin.save(using='write')
        
        for channel_id in request.POST.getlist('channel_id'):
            channel_id = int(channel_id)
            the_admin.channel.add(Channel.objects.using('write').get(id=channel_id))
        
        for server_id in request.POST.getlist('server_id'):
            server_id = int(server_id)
            the_admin.server.add(Server.objects.using('write').get(id=server_id))
        
#        for menu_id in request.POST.getlist('menu_id'): 
#            menu_id = int(menu_id)
#            role.menu.add(Menu.objects.get(id=menu_id))
#            return HttpResponseRedirect('/role/list')
        return HttpResponseRedirect('/admin_user/list')
    else:
        err_msg = u'请正确填写账户信息!'
    return render_to_response('feedback.html', {'user':the_admin, 'err_msg':err_msg})
 

def admin_remove(request, admin_id=0):
    is_recover = request.GET.get('recover', False)
    the_admin = Admin.objects.using('write').get(id=admin_id)
    if the_admin == None:
        err_msg = u'用户不存在'
    else:
        if not is_recover:
            err_msg = u'删除成功'
            the_admin.status = admin_status.DEL
        else:
            err_msg = u'恢复成功'
            the_admin.status = admin_status.NORMAL
        the_admin.save()
        
    return render_to_response('feedback.html', { 'err_msg':err_msg})
 

def change_password(request):
    the_admin_id = int(request.session.get('userid', '0'))
    the_admin = None
    if the_admin_id > 0 :
        the_admin = Admin.objects.using('read').get(id=the_admin_id)
    
    parg = {}
    parg["the_admin"] = the_admin
    
    return render_to_response('system/admin_change_password.html', parg)


def change_password_do(request):   
    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('new_password', '')
    template_name = 'system/admin_change_password.html'
    the_admin_id = int(request.session.get('userid', '0'))
    the_admin = None
    if the_admin_id > 0 :
        the_admin = Admin.objects.using('read').get(id=the_admin_id)
    tmp_admin = Admin()
    tmp_admin.password = old_password
    if the_admin and the_admin.password == tmp_admin.md5_password() :
        the_admin.password = new_password
        the_admin.password = the_admin.md5_password()
        the_admin.last_time = datetime.datetime.now()
        the_admin.save(using='write')
        err_msg = u'密码已经修改成功!'
    else:
        err_msg = u'旧密码输入不正确!'
    
    parg = {}
    parg["old_password"] = old_password
    parg["new_password"] = new_password
    parg["err_msg"] = err_msg
    
    return render_to_response(template_name, parg)

def unlock(request, admin_id=0):
    err_msg = ''
    if request.method == "POST":
        user_name = request.POST.get('username', '')
        pwd = request.POST.get('password', '')
        tmp_admin = Admin()
        tmp_admin.username = user_name
        tmp_admin.password = pwd
        list_data = Admin.objects.filter(username = tmp_admin.username, password = tmp_admin.md5_password())
        if 0 == list_data.__len__():
            err_msg = u'账号不存在或密码错误'
        else:
            admin = list_data[0]
            admin.lock_time = datetime.datetime.now()
            admin.login_count = 0
            admin.save()
            return render_to_response('feedback.html')
    
    return render_to_response('system/unlock.html', {'err_msg':err_msg})
        
    

def admin_set(request, admin_id=0, admin_status=0):
    admin_id = int(admin_id)
    if admin_id > 0 :
        the_admin = Admin.objects.using('read').get(id=admin_id)
        the_admin.status = admin_status
        the_admin.save(using='write')
    
    parg = {}
    parg["the_admin"] = the_admin
    
    return render_to_response('feedback.html', parg)

