#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response 
from GameManage.models.admin import Role, Menu
from django.http import HttpResponseRedirect

def role_list(request):
    
    list_record = Role.objects.all()
    
    parg = {}
    parg["list_record"] = list_record
    
    return render_to_response('system/role_list.html', parg)

def role_edit(request, role_id=0):
    
    role_id = int(role_id)
    
    if 0 == role_id:
        role_id = int(request.GET.get('role_id', request.POST.get('role_id', 0)))
    
    if role_id > 0:
        role = Role.objects.get(id=role_id)
    else:
        role = Role()
        role.id = role_id

    menu_list = Menu.objects.all()
    if role.id > 0:
        for item in menu_list:
            if len(role.menu.filter(id=item.id)) > 0:
                item.is_checked = 1
            else:
                item.is_checked = 0
                
    
    
    return render_to_response('system/role_edit.html', {'model':role, 'menu_list':menu_list})


def role_save(request, role_id=0):
    role_id = int(role_id)
    if 0 == role_id:
        role_id = int(request.GET.get('role_id', request.POST.get('role_id', 0)))
        
    if role_id > 0:
        role = Role.objects.using('write').get(id=role_id)
        role.menu.clear()
    else:
        role = Role()
    err_msg = ''
    role.name = request.POST.get('name', u'管理员')    
    try:
        role.save(using='write')
        
        for menu_id in request.POST.getlist('menu_id'): 
            menu_id = int(menu_id)
            role.menu.add(Menu.objects.using('write').get(id=menu_id))
        return HttpResponseRedirect('/role/list')
    except Exception, e:
        err_msg = 'role save error:%s' % e
    
    parg = {}
    parg["err_msg"] = err_msg
    
    return render_to_response('feedback.html', parg)

def role_remove(request, role_id=0):
    role_id = int(role_id)
    if 0 == role_id:
        role_id = int(request.GET.get('role_id', request.POST.get('role_id', 0)))
        
    if role_id > 0:
        role = Role.objects.using('write').get(id=role_id)
    else:
        role = Role()
    
    role.menu.clear()

    role.delete(using='write')
    
    return render_to_response('feedback.html')
