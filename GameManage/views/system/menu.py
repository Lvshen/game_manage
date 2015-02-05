#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.models.admin import Admin, Menu
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from GameManage.cache import menu_cache 
from GameManage.views.base import UserStateManager
'''
管理员设置，权限管理，模块管理
'''

def menu_script(request):
    usm = UserStateManager(request) 
    parg = {}
    parg["list_menu"] = menu_cache.get_menu_list(usm) 
    print('~~~~~~~~~parg values: ', parg.values())
    print('~~~~~~~~~parg keys: ', parg.keys())
    return render_to_response('system/menu_script.html', parg)

#def login_script(request):
#    the_channel_id=int(request.session.get('channelId','0'));
#    
#    the_channel_list=Channel.objects.filter()

def menu_list(request):
    
    list_record = Menu.objects.using('read').all()
    
    parg = {}
    parg["list_record"] = list_record
    
    return render_to_response('system/menu_list.html', parg)

def menu_edit(request, menu_id=0, parent_id=0):
    menu_id = int(menu_id)
    if 0 == menu_id:
        menu_id = int(request.GET.get('menu_id', request.POST.get('menu_id', 0)))
    
    if menu_id > 0 :
        menu = Menu.objects.using('write').get(id=menu_id)
    else:
        menu = Menu()
        menu.id = menu_id
        menu.parent_id = parent_id
    
    list_menu = Menu.objects.using('read').filter(parent_id=0)
    
    parg = {}
    parg["menu"] = menu
    parg["list_menu"] = list_menu
    
    return render_to_response('system/menu_edit.html', parg)

def menu_save(request, menu_id=0):
    menu_id = int(menu_id)
    if 0 == menu_id:
        menu_id = int(request.GET.get('menu_id', request.POST.get('menu_id', 0)))
    
    if menu_id > 0 :
        menu = Menu.objects.using('write').get(id=menu_id)
    else:
        menu = Menu()
    
    menu.parent_id = int(request.POST.get('parent_id', '0'))
    menu.order = int(request.POST.get('order', '0'))
    menu.is_show = int(request.POST.get('is_show', '0'))
    menu.is_log = int(request.POST.get('is_log', '0'))
    menu.name = request.POST.get('name', '')
    menu.url = request.POST.get('url', '')
    menu.icon = request.POST.get('icon', '')
    menu.css = request.POST.get('css', '')
    try:
        menu.save(using='write')
        return HttpResponseRedirect('/menu/list')
    except Exception, e:
        print('menu error:', e)
    return render_to_response('feedback.html')

def menu_remove(request, menu_id=0):
    menu_id = int(menu_id)
    if 0 == menu_id:
        menu_id = int(request.GET.get('menu_id', request.POST.get('menu_id', 0)))
    if menu_id > 0 :
        menu = Menu.objects.get(id=menu_id)

        menu.delete(using='write')
    
    return render_to_response('feedback.html')
