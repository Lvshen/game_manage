#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.db.models import Q
from GameManage.models.center import UserType
from GameManage.views.base import UserStateManager
from django.http import HttpResponseRedirect

def user_type_list(request, err_msg = ''):
    data_list = UserType.objects.all()
    
    parg = {}
    parg['data_list'] = data_list
    parg['err_msg'] = err_msg
    
    return render_to_response('player/user_type_list.html', parg)

def user_type_edit(request, model_id=0, err_msg = ''):
    model_id = int(model_id)
    if model_id==0:
        model_id = int(request.GET.get('id', '0'))
    
    model = None
    if 0 < model_id:
        model = UserType.objects.get(id = model_id)
    else:
        model = UserType()
        model.id = 0 
    parg = {}
    parg['model'] = model
    parg['err_msg'] = err_msg
    
    return render_to_response('player/user_type_edit.html', parg)
    

def user_type_save(request, model_id=0):
    model_id = int(model_id)
    if model_id==0:
        model_id = int(request.POST.get('id', '0'))
    if model_id==0:
        model_id = int(request.GET.get('id', '0'))
        
    err_msg = ''
    func_ver = 0
    try:
        func_ver = int(request.POST.get('func_ver', ''))
    except:
        err_msg = '版本号格式错误'
        
    usm = UserStateManager(request)
    model = None
     
    if 0 == model_id:
        model = UserType()
        
    else:
        if 0 < model_id:
            model = UserType.objects.get(id = model_id)
    
    if None == model or not usm.current_userRole_is_root():
        err_msg = '非法操作'
    else:
        model.name = request.POST.get('name', '')
        model.type_id = int(request.POST.get('type_id', -1))
        model.login_config = request.POST.get('login_config', '')
        model.func_name = request.POST.get('func_name', '')
        model.func_ver = func_ver
        model.remark = request.POST.get('remark', '')
        
        if '' == err_msg:
            try:
                model.save()
            except Exception, ex:
                err_msg = '保存出错'
    
    if '' != err_msg:
        response = user_type_edit(request, model_id, err_msg)
    else:
        response = HttpResponseRedirect('/player/type')
    
    return response

def user_type_del(request):
    model_id = int(request.GET.get('id', '0'))
    err_msg  = ''
    
    if 0 == id:
        err_msg = '没有选择用户类型'
    else:
        UserType.objects.filter(id = model_id).delete()
        
    return user_type_list(request, err_msg)
