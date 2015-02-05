#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.models.log import QueryResult
from GameManage.models.charts import ChartsDefine
from django.shortcuts import render_to_response
from GameManage.views.base import UserStateManager
from django.http import HttpResponse
from GameManage.views.charts.base_datasource import check_role, get_month_data, get_today_data, get_week_data, get_yesterday_date 

import datetime

now = datetime.datetime.now()
def get_situation(request, model_id):
    server_id = int(request.GET.get('server_id', 0))
    
    usm = UserStateManager(request)
    
    if not check_role(request, server_id, usm):
        return HttpResponse(u'没有权限')
            
    charts_def = ChartsDefine.objects.get(id = model_id)
    title = charts_def.title
    query_result_id = charts_def.query_result_id
    
    query_result = QueryResult.objects.get(id = query_result_id)
    
    statistic_list = query_result.statistic.all()
    
    today_data_list = []
    yesterday_data_list = []
    week_data_list = []
    month_data_list = []
    
    for statistic in statistic_list:
        today_data_list.append(get_today_data(server_id, statistic, usm))
        yesterday_data_list.append(get_yesterday_date(server_id, statistic, usm))
        week_data_list.append(get_week_data(server_id, statistic, usm))
        month_data_list.append(get_month_data(server_id, statistic, usm))
    
    pargs = {}
    pargs['statistic_list'] = statistic_list
    pargs['title'] = title
    pargs['today_data_list'] = today_data_list
    pargs['yesterday_data_list'] = yesterday_data_list
    pargs['week_data_list'] = week_data_list
    pargs['month_data_list'] = month_data_list
    
    return render_to_response('charts/statistic_situation.html', pargs)
    
