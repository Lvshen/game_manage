#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.db.models import Q
from GameManage.models.gm import GMDefine
from GameManage.http import http_post
import json
from django.shortcuts import render_to_response

def gm_list(request):
    gm_type = request.GET.get('gm_type', '')
    page_num = int(request.GET.get('page_num', '1'))
    page_size = 150
    
    query = Q() 
        
    if gm_type != '':
        query = query & Q(result_type = gm_type)
    
    total_record = GMDefine.objects.filter(query).count()
    list_gm = []
    if 0 < total_record:
        list_gm = GMDefine.objects.filter(query)[(page_num - 1) * page_size:page_num * page_size]
        
    parg = {}
    
    parg['list_gm'] = list_gm
    parg['page_num'] = page_num
    parg['page_size'] = page_size
    parg['gm_type'] = gm_type
    parg['total_record'] = total_record
    print "hadfadf"
    return render_to_response('game/def_gm_list.html', parg)


def gm_edit(request, model_id = 0):
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    
    if 0 != model_id:
        model = GMDefine.objects.get(id=model_id)
    else:
        model = GMDefine()
        model.id = 0
    
    parg={}
    parg['model'] = model
    
    return render_to_response('game/def_gm_edit.html', parg)
    
    

def gm_save(request):
    model_id = int(request.GET.get('id', 0))
    save_id = int(request.POST.get('save_id', 0))
    model = None
    if model_id == 0 or 0 == GMDefine.objects.filter(id=model_id).count():
        model = GMDefine()
    else:
        model = GMDefine.objects.get(id = model_id)
    if 0 != save_id:
        model.id = save_id
    
    exists = False
    if model_id != save_id:
        if 0 < GMDefine.objects.filter(id=save_id).count():
            exists = True
    err_msg = ''
    if not exists:
        model.title = request.POST.get('title', '')
        model.description = request.POST.get('description', '')
        model.url = request.POST.get('url', '')
        model.params = request.POST.get('params', '')
        model.result_type = request.POST.get('result_type', '')
        model.result_define = request.POST.get('result_define', '')
        model.flag = request.POST.get('flag', '')
        model.save()
    else:
        err_msg = 'ID 已经存在'
    
    parg = {}
    parg['err_msg'] = err_msg
    parg['model'] = model
    
    if '' != err_msg:
        return render_to_response('game/def_gm_edit.html', parg)
    else:
        return gm_list(request)
    
def gm_del(request, model_id=0):
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    
    GMDefine.objects.filter(id = model_id).delete()
    
    return gm_list(request)
    
    
    
    
    
    
