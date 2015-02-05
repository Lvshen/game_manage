#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from GameManage.models.log import QueryResult
from GameManage.models.charts import ChartsDefine
from django.shortcuts import render_to_response
    
def charts_def_list(request):
    
    charts_type = request.GET.get('type', '')
    
    list_data = ChartsDefine.objects.all()
    
    type_list = {}
    for item in list_data:
        type_list[item.charts_type] = item.charts_type
    
    if charts_type != '':
        tmp_list = []
        for item in list_data:
            if item.charts_type ==  charts_type:
                tmp_list.append(item)
            list_data = tmp_list
    
    query_result_list =  QueryResult.objects.all()
     
    for item in list_data:
        for query_result_item in query_result_list:
            if item.query_result_id == query_result_item.id:
                item.query_result_name = query_result_item.name
    #print 'type_list', type_list
    pargs = {}
    pargs['list_data'] = list_data
    pargs['type_list'] = type_list
    pargs['charts_type'] = charts_type
    return render_to_response('charts/list.html', pargs)
    
    
    
def charts_edit(request, model_id = 0):
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    
    model = ChartsDefine()
    model.id = 0
    model.is_show = 0
    model.statistic_id = 0
    model.chart_height = 0
    model.expression_cfg = ''
    if 0 != model_id:
        model = ChartsDefine.objects.get(id = model_id)
     
    query_model = QueryResult.objects.using('read').all().order_by("id")
        
    if model.expression_cfg == None:
        model.expression_cfg = ''

                
    parg = {}
    parg['model'] = model
    parg['query_model'] = query_model
    return render_to_response('charts/edit.html', parg)
    


def charts_save(request, model_id = 0):
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    
    title = request.POST.get('title', '')
    charts_type = request.POST.get('charts_type', '')
    query_result_id = int(request.POST.get('query_result_id', 0))
    display_type = request.POST.get('display_type', '')
    is_show = int(request.POST.get('is_show', 0))
    unit = request.POST.get('unit', '')
    chart_height = int(request.POST.get('chart_height', 0))
    expression_cfg = request.POST.get('expression_cfg', '')
    model = ChartsDefine()
    model.id = 0
    if 0 != model_id:
        model = ChartsDefine.objects.get(id = model_id)
    
    
    model.title = title
    model.charts_type = charts_type
    model.query_result_id = query_result_id
    model.display_type = display_type
    model.is_show = is_show
    model.unit = unit
    model.chart_height = chart_height
    model.expression_cfg = expression_cfg
    
    model.save()
    
    
    return HttpResponseRedirect('/charts/list')
    
def charts_del(request, model_id = 0):
    if 0 == model_id:
        model_id = request.GET.get('id')
    
    ChartsDefine.objects.filter(id=model_id).delete()
    
    return HttpResponseRedirect('/charts/list')
    
    
    
