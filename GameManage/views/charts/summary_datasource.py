#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.models.log import QueryResult
from GameManage.models.charts import ChartsDefine
from django.shortcuts import render_to_response
from GameManage.views.base import UserStateManager
from django.http import HttpResponse
from GameManage.cache import center_cache, memcached_util
from GameManage.views.charts.base_datasource import get_today_data, check_role
from django.db import connections
from GameManage.views.base import md5
import datetime, json, re

now = datetime.datetime.now()
def get_summary(request, model_id):
    server_id = int(request.GET.get('server_id', 0))
    usm = UserStateManager(request)
    
    if not check_role(request, server_id, usm):
        return HttpResponse(u'没有权限')
    
    charts_def = ChartsDefine.objects.get(id = model_id)
    title = charts_def.title
    query_result_id = charts_def.query_result_id
    
    query_result = QueryResult.objects.get(id = query_result_id)
    
    statistic_list = query_result.statistic.all()
    
    express_list = []
    if None != charts_def.expression_cfg and '' != charts_def.expression_cfg:
        #print charts_def.expression_cfg
        express_list = json.loads(charts_def.expression_cfg)
    
    data_list = []
    
    for statistic in statistic_list:
        result = get_today_data(server_id, statistic, usm)
        statistic.result = result
        data_list.append({"name":statistic.name, "result":result})
    
    for item in express_list: 
        e = json.dumps(item.get("expression"))
        for statistic in statistic_list:
            e = e.replace('#%s#'% statistic.id, str(statistic.result))
        try:
            exec 'result = %s ' % json.loads(e)
        except Exception, ex:
            print ex
            result = 0
        data_list.append({"name":item.get("name"), "result":result, "unit":item.get("unit", '')})
    
     
    pargs = {}
    pargs['statistic_list'] = data_list
    pargs['title'] = title
    
    return render_to_response('charts/statistic_summary.html', pargs)
    


def get_data(server_id, statistic, usm):
    the_user = usm.get_the_user()
    
    mc = memcached_util.MemcachedUtil()
    channel_list = []
    
    if usm.current_userRole_is_root():
        channel_list = center_cache.get_channel_list(mc)
    else:
        channel_list = center_cache.get_user_channel_list(the_user, mc)
    
    conn = connections['read']
    cursor = conn.cursor()
    
    channel_id_list = [str(item.id) for item in channel_list]
    
    begin_date = now.strftime('%Y-%m-%d 00:00:00')
    end_date = (now + datetime.timedelta(days = 1)).strftime('%Y-%m-%d 00:00:00')
    
    server_conditions = ''
    if 0 != server_id:
        server_conditions = ' AND server_id=%s ' % server_id
    
    sql = "SELECT SUM(`result`) FROM `result` WHERE statistic_id=%s AND create_time BETWEEN '%s' AND '%s' AND channel_id IN (%s) %s " % (statistic.id ,begin_date, end_date, ','.join(channel_id_list), server_conditions)
    
    key = md5(sql)
    result = mc.get(key)
    if None == result:
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        if result == None:
            return 0
        result = float(result)
        mc.set(key, result)
        
    return result
    
   
    
    
    
    
    
