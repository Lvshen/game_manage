#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.models.log import QueryResult
from GameManage.models.charts import ChartsDefine
from GameManage.models.center import Channel
from django.shortcuts import render_to_response
from GameManage.views.base import UserStateManager, GlobalPathCfg
from django.template import Template, Context
from django.http import HttpResponse
from GameManage.views.charts.base_datasource import check_role, get_today_data, get_yesterday_date, get_week_data, get_month_data

import datetime, calendar

now = datetime.datetime.now()
def get_spline_time_charts(request, model_id, statistic_id = 0):
    server_id = int(request.GET.get('server_id', 0))
    
    usm = UserStateManager(request)
    
    if not check_role(request, server_id, usm):
        return HttpResponse(u'没有权限')
    
    charts_def = ChartsDefine.objects.get(id = model_id)
    title = charts_def.title
    query_result_id = charts_def.query_result_id
    
    query_result = QueryResult.objects.get(id = query_result_id)
    
    statistic_list = query_result.statistic.all()
    
    current_statistic = None
    if 0 == statistic_id:
        current_statistic = statistic_list[0]
    else:
        for item in statistic_list:
            if item.id == statistic_id:
                current_statistic = item
    
    today_data = []
    yesterday_data = []
    week_data = [] 
    month_data = [] 
    #当前月份天数
    today = datetime.date.today()
    current_month_days = calendar.monthrange(today.year, today.month)[1]
    
    for index in range(current_month_days):
        day = index + 1
        
        base_date = datetime.datetime(today.year, today.month, day)
        
        today_data.append({'year':base_date.year, 'month':base_date.month, 'day':base_date.day, 'value':get_today_data(server_id, current_statistic, usm, base_date)})
        
        yesterday_data.append({'year':base_date.year, 'month':base_date.month, 'day':base_date.day, 'value':get_yesterday_date(server_id, current_statistic, usm, base_date)})
        
        week_data.append({'year':base_date.year, 'month':base_date.month, 'day':base_date.day, 'value':get_week_data(server_id, current_statistic, usm, base_date)})
        
        month_data.append({'year':base_date.year, 'month':base_date.month, 'day':base_date.day, 'value':get_month_data(server_id, current_statistic, usm, base_date)})
    
    
    path_cfg = GlobalPathCfg()
    template_path = path_cfg.get_spline_time_charts_template_path()
    
    file_tpl = open(template_path, 'r')
    tpl_content = file_tpl.read()
    file_tpl.close()
    t = Template(tpl_content)
    c = Context({"today_data":today_data, "yesterday_data": yesterday_data, "week_data": week_data, "month_data":month_data})
    c = t.render(c)
    
    pargs = {}
    pargs['data'] = c
    pargs['type'] = 'spline'
    pargs['title'] = title
    pargs['unit'] = '用户数'
    pargs['sub_title'] = title
    
    return render_to_response('charts/spline_time_charts.html', pargs)




    
    
