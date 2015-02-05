#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from GameManage.models.charts import ChartsDefine,ChartsResult
from django.http import HttpResponse
from django.db import connection
from GameManage.cache import center_cache
from GameManage.views.base import UserStateManager
import datetime,time
from GameManage.models.log import Result,Statistic

def charts_result_list(request):
    list_model = ChartsResult.objects.using('read').all()
    parg = {}
    parg["list_model"] = list_model
    return render_to_response('charts/result_list.html', parg)

def charts_result_edit(request, model_id = 0):
    model_id = int(model_id)
    if model_id > 0:
        model = ChartsResult.objects.get(id = model_id)
    else:
        model = ChartsResult()
        model.id = 0
    list_charts = ChartsDefine.objects.using('read').all()
    print list_charts.__len__()
    selected_charts = get_charts(model_id)
    list_selected = {}
    for item in selected_charts:
        list_selected[item[0]] = ''
        
    for item in list_charts:
        if list_selected.get(item.id, None) != None:
            item.is_show = 1
        else:
            item.is_show = 0
    
    parg = {}
    parg["model"] = model
    parg["list_charts"] = list_charts
    return render_to_response('charts/result_edit.html', parg)

def charts_result_save(request, model_id = 0):
    model_id = int(model_id)
    if model_id > 0:
        model = ChartsResult.objects.get(id=model_id)
    else:
        model = ChartsResult()
        #model.id = 0
        
    model.name = request.POST.get('name', '')
    if model.name == '':
        return HttpResponse("名称不能为空!<a href='javascript:history.back();'>点击返回</a>")
    model.remark = request.POST.get('remark', '')    
    err_msg = ''
    try:
        if model.id > 0:
            model.charts.clear()
        model.save(using='write')
        charts_id_list = request.POST.getlist('chartsdefine_id') 

        for charts_id in charts_id_list:
            charts_id = int(charts_id)
            charts_item = ChartsDefine.objects.using('write').get(id = charts_id)
            
            model.charts.add(charts_item) 
        return HttpResponseRedirect('charts/result/list')
    except Exception, e:
        print('notice save error:', e)
        err_msg = e
    
    parg = {}
    parg["model"] = model
    parg["err_msg"] = err_msg
    return render_to_response('charts/result_edit.html', parg)

def get_charts(model_id, is_show = 0):
    sql = "SELECT c.`id`, c.`title`,c.`display_type`,c.`chart_height` FROM `def_charts` c JOIN `charts_result_charts` r ON c.`id` = r.`chartsdefine_id` AND r.`chartsresult_id` = %d "%model_id
    if is_show == 1:
        sql += ' AND c.`is_show` = 1'
    cursor = connection.cursor()
    cursor.execute(sql)
    list_record = cursor.fetchall()
    return list_record

def charts_result_del(request, model_id = 0):
    model_id = int(model_id)
    if model_id > 0:
        model_id = int(model_id)
    else:
        model_id = int(request.GET.get('id', 0))
        
    ChartsResult.objects.filter(id = model_id).delete()
    return HttpResponseRedirect('/charts/result/list')

def charts_result_view(request, model_id = 0):
    server_id = int(request.GET.get('server_id', 0))
    usm = UserStateManager(request)
    the_user = usm.get_the_user()
    model_id = int(model_id)
    chart_result = ChartsResult.objects.get(id = model_id)
    list_charts_def = get_charts(model_id, 1)
    if usm.current_userRole_is_root():
        server_list = center_cache.get_server_list()
    else:
        server_list = center_cache.get_user_server_list(the_user)
    
    if not server_list.__contains__(server_id) and 0 == server_list.__len__():
        return HttpResponse(u'没有权限')
    
    if 0 == server_id:
        server_id = server_list[0].id
    
    summary_list = []
    situation_list = []
    charts = []
    date_trend = []
    top = []
    pie = []
    for item in list_charts_def:
        chart_type = item[2]
        if chart_type == 'summary':
            url = '/charts/summary/%s?server_id=%s' % (item[0], server_id)
            summary_list.append({'src':url, 'chart_height': item[3]})
        elif chart_type == 'situation':
            url = '/charts/situation/%s?server_id=%s' % (item[0], server_id)
            situation_list.append({'src':url, 'chart_height': item[3]})
        elif chart_type == 'spline_time_chart':
            url = '/charts/spline/time/%s?server_id=%s'% (item[0], server_id)
            charts.append({'src':url, 'chart_height': item[3]})
        elif chart_type == 'date_trend':
            url = '/charts/result/view/analyse/%s?server_id=%s'% (item[0], server_id)
            date_trend.append({'src':url, 'chart_height': item[3]})
        elif chart_type == 'top':
            url = '/charts/result/view/pie/%s?server_id=%s&d_type=2'% (item[0], server_id)
            top.append({'src':url, 'chart_height': item[3]})
        elif chart_type == 'pie':
            url = '/charts/result/view/pie/%s?server_id=%s&d_type=1'% (item[0], server_id)
            pie.append({'src':url, 'chart_height': item[3]}) 
    pargs = {}
    pargs['server_list'] = server_list
    pargs['situation_list'] = situation_list
    pargs['summary_list'] = summary_list
    pargs['charts'] = charts
    pargs['server_id'] = server_id
    pargs['date_trend'] = date_trend
    pargs['chart_result'] = chart_result
    pargs['top'] = top
    pargs['pie'] = pie
    return render_to_response('charts/result_view.html', pargs)


def charts_result_analyse(request, query_id = 0, charts_type = 'spline', title = '时段趋势'):
    title = title
    query_id = int(query_id)
    model = ChartsDefine.objects.get(id = query_id)
    list_statistic_sort = get_statistic_in_query(int(model.query_result_id))#获取根据关联表ip排序的数据
    join_results = []
    item_results = []

    now = datetime.datetime.now()   
    sdate = request.GET.get('sdate','')
    edate = request.GET.get('edate','')

        
    server_id = int(request.GET.get('server_id',0))
    query_day = request.GET.get('query_day', 0);
    date_format = '%%Y-%%m-%%d'
    chart_format = '%Y-%m-%d'
    time_slot = 86400000 
    if sdate and edate:
        d1 = datetime.datetime(int(sdate.split("-")[0]),int(sdate.split("-")[1]),int(sdate.split("-")[2]))
        d2 = datetime.datetime(int(edate.split("-")[0]),int(edate.split("-")[1]),int(edate.split("-")[2]))
        days = ( d2 - d1).days + 1
        if days == 1:
            charts_type = 'column'   
        time_slot = Result().cmp_time(days)   
    elif query_day != 0:
        if query_day == '1':
            sdate = now.strftime('%Y-%m-%d 00:00:00')
            edate = now.strftime('%Y-%m-%d 23:59:59')
            charts_type = 'column'
        elif query_day == '-1':
            sdate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
            edate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')
            charts_type = 'column'
        elif query_day == '-2':
            sdate = (now - datetime.timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
            edate = (now - datetime.timedelta(days=2)).strftime('%Y-%m-%d 23:59:59')
            charts_type = 'column'
        elif query_day == '7':
            sdate = (now - datetime.timedelta(days=7)).strftime('%Y-%m-%d 00:00:00')
            edate = now.strftime('%Y-%m-%d 23:59:59')
        elif query_day == '30':
            sdate = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d 00:00:00')
            edate = now.strftime('%Y-%m-%d 23:59:59')
    else:
        sdate = now.strftime('%Y-%m-01 00:00:00')
        edate = now.strftime('%Y-%m-%d 23:59:59')          
    query_date = ' AND `create_time` >= \'%s\' AND `create_time` <= \'%s\''%(sdate, edate) 
    query_server = ''
    if server_id != 0:
        query_server = ' AND `server_id` = %d '%server_id
        
    for item in list_statistic_sort:
        join_results.append(str(item[0]))#id
        item_results.append([item[0], item[1]])

    cursor = connection.cursor()

    select_str = 'DATE_FORMAT(result_time,"%s") AS `date`'% date_format
    for item in join_results:
        select_str += ',sum(case when `statistic_id`=%s then result else 0 end) item%s' % (item, item)
        
    query_sql = 'select %s from result where statistic_id in(%s)%s%s group by `date` ORDER BY `date`' % (select_str, ','.join(join_results), query_server, query_date)

    count_sql = 'select count(*) result from (%s) newTable WHERE 1' % (query_sql)
    cursor.execute(count_sql)
    total_record = int(cursor.fetchone()[0])
    print query_sql
    list_record = []
    if total_record > 0:
        cursor.execute(query_sql)
        list_record = cursor.fetchall()

    template = 'charts/result_analyse.html'
    
    list_record_arr = {}
    i = 1
    tmp_item = []
    
    for item_result in item_results:
        tmp_item = []
        for item in list_record:
            item = list(item)
            item[0] = int(time.mktime(datetime.datetime.strptime(str(item[0]),"%s"%chart_format).timetuple())) * 1000;
            tmp_item.append([item[0],int(item[i])])
            list_record_arr[item_result[1]] = tmp_item
        i = i+1
    list_record_arr = str(list_record_arr).replace('(', '[').replace(')', ']').replace('L', '')
    list_record_arr = str(list_record_arr).replace('u\'', '\'')
   
    parg = {}
    parg["title"] = title
    parg["join_results"] = join_results   
    parg["time_slot"] = time_slot
    parg["chart_format"] = chart_format
    parg["list_record_arr"] = list_record_arr
    parg["charts_type"] = charts_type
    parg["server_id"] = server_id
    parg["query_id"] = query_id
    parg["sdate"] = sdate[0:10]
    parg["edate"] = edate[0:10]
    return render_to_response(template, parg)
#
#def charts_result_top(request, query_id = 0, server_channel = 'server',charts_type = 'bar', title = 'TOP10'):
#    title = title
#    query_id = int(query_id)
#    model = ChartsDefine.objects.get(id = query_id)
#    list_statistic_sort = get_statistic_in_query(int(model.query_result_id))#获取根据关联表ip排序的数据
#    join_results = []
#    item_results = []
#
#    now = datetime.datetime.now()   
#    sdate = request.GET.get('sdate','')
#    edate = request.GET.get('edate','')
#        
#    query_item = int(request.GET.get('query_item', '0'))
#    query_type = int(request.GET.get('query_type', '0'))
#    
#    if not sdate and not edate:
#        sdate = now.strftime('%Y-%m-01 00:00:00')
#        edate = now.strftime('%Y-%m-%d 23:59:59')
#    query_date = ' AND r.`create_time` >= \'%s\' AND r.`create_time` <= \'%s\''%(sdate, edate) 
#        
#    for item in list_statistic_sort:
#        join_results.append(int(item[0]))#id
#        item_results.append([item[0], item[1]])
#        
#    cursor = connection.cursor()
#
#    if query_type == 0:
#        select_str = 's.`name`'
#    else:
#        select_str = 'c.`name`'
#    if query_item != 0:
#        select_str += ',sum(case when r.`statistic_id`=%d then result else 0 end) item' % (query_item)
#    else:
#        select_str += ',sum(case when r.`statistic_id`=%d then result else 0 end) item' % (join_results[0])
#        query_item = int(join_results[0])
#    query_item_name = Statistic.objects.values('name').get(id = query_item)
#    if query_type == 0:
#        query_sql = 'select %s from result r JOIN `servers` s ON r.`server_id` = s.`id` where r.`statistic_id` = %d %s GROUP BY r.`server_id` ORDER BY `item` DESC LIMIT 10' % (select_str, query_item, query_date)
#    else:
#        query_sql = 'select %s from result r JOIN `channel` c ON r.`channel_id` = c.`id` where r.`statistic_id` = %d %s GROUP BY r.`channel_id` ORDER BY `item` DESC LIMIT 10' % (select_str, query_item, query_date)
#    count_sql = 'select count(*) result from (%s) newTable WHERE 1' % (query_sql)
#    cursor.execute(count_sql)
#    total_record = int(cursor.fetchone()[0])
#    print query_sql
#    list_record = []
#    if total_record > 0:
#        cursor.execute(query_sql)
#        list_record = cursor.fetchall()
#
#    template = 'charts/result_top.html'
#    
#    data = []
#    xAxis = []
#    if total_record > 0:
#        for item in list_record:
#            item = list(item)
#            xAxis.append('%s'%item[0])
#            data.append(int(item[1]))         
#    xAxis = str(xAxis).replace('(', '[').replace(')', ']').replace('L', '')
#    xAxis = str(xAxis).replace('u\'', '\'') 
#    parg = {}
#    parg["title"] = title
#    parg["item_results"] = item_results
#    parg["data"] = data
#    parg["xAxis"] = xAxis
#    parg["query_item"] = query_item
#    parg["query_item_name"] = query_item_name
#    parg["charts_type"] = charts_type
#    parg["query_id"] = query_id
#    parg["sdate"] = sdate[0:10]
#    parg["edate"] = edate[0:10]
#    parg["query_type"]  = query_type
#    return render_to_response(template, parg)

def charts_result_pie(request, query_id = 0, server_channel = 'server',charts_type = 'pie', title = '饼图'):
    title = title
    query_id = int(query_id)
    model = ChartsDefine.objects.get(id = query_id)
    list_statistic_sort = get_statistic_in_query(int(model.query_result_id))#获取根据关联表ip排序的数据
    
    join_results = []
    item_results = []

    now = datetime.datetime.now()   
    sdate = request.GET.get('sdate','')
    edate = request.GET.get('edate','')
    
    query_item = int(request.GET.get('query_item', '0'))
    query_type = int(request.GET.get('query_type', '0'))
    request_server_list = request.GET.getlist('server_id')
    request_channel_list = request.GET.getlist('channel_id')
    display_type = int(request.GET.get('d_type', 1))
    
    if request_server_list.__len__() >= 100:
        return HttpResponse(u'非法请求')
    
    if request_channel_list.__len__() >= 100:
        return HttpResponse(u'非法请求')
    
    if not sdate and not edate:
        sdate = now.strftime('%Y-%m-01 00:00:00')
        edate = now.strftime('%Y-%m-%d 23:59:59')
    query_date = ' AND r.`create_time` >= \'%s\' AND r.`create_time` <= \'%s\''%(sdate, edate)
    
    usm = UserStateManager(request)
    the_user = usm.get_the_user()
    
    server_list = []
    channel_list = []
    if usm.current_userRole_is_root():
        server_list = center_cache.get_server_list()
        channel_list = center_cache.get_channel_list()
    else:
        server_list = center_cache.get_user_server_list(the_user)
        channel_list = center_cache.get_user_channel_list(the_user)
    
    if not usm.current_userRole_is_root:
        if 0 == server_list.__len__():
            return HttpResponse(u'没有权限')
        
        if 0 == channel_list.__len__():
            return HttpResponse(u'没有权限')
    
    #限制服务器和渠道选择的数量
    limit_server_count = 10
    limit_channel_count = 10
    
    tmp_index = 0
    if 0 == request_server_list.__len__():
        request_server_list = []
        
        for item in server_list:
            if tmp_index >= limit_server_count:
                break
            request_server_list.append(str(item.id))
            tmp_index = tmp_index + 1
    
    if 0 == request_channel_list.__len__():
        tmp_index = 0 
        for item in channel_list:
            if tmp_index >= limit_channel_count:
                break
            request_channel_list.append(str(item.id))
            tmp_index = tmp_index + 1
    
    
    has_server_count = 0
    for item in server_list:
        for server_id in request_server_list:
            server_id = int(server_id)
            if item.id == server_id:
                has_server_count = has_server_count + 1
                item.selected = True
    
    has_channel_count = 0
    for item in channel_list:
        for channel_id in request_channel_list:
            channel_id = int(channel_id)
            if item.id == channel_id:
                has_channel_count = has_channel_count + 1
                item.selected = True
    
    if (has_server_count != request_server_list.__len__() or has_server_count != request_channel_list.__len__()) and not usm.current_userRole_is_root:
        return HttpResponse(u'没有权限')
        
    
    query_server_id = ' AND r.server_id IN (%s)' %  ','.join(request_server_list)
    
    query_channel_id = ' AND r.channel_id IN (%s)' % ','.join(request_channel_list)
    
    q_str = ''
    limit_count = 0
    
    for item in list_statistic_sort:
        join_results.append(int(item[0]))#id
        item_results.append([item[0], item[1]])
        
    cursor = connection.cursor()
    
    
    if query_type == 0:
        select_str = 's.`name`'
        q_str = query_server_id
        limit_count = limit_server_count
    else:
        select_str = 'c.`name`'
        q_str = query_channel_id
        limit_count = limit_channel_count
        
    if query_item != 0:
        select_str += ',sum(case when r.`statistic_id`=%d then result else 0 end) item' % (query_item)
    else:
        select_str += ',sum(case when r.`statistic_id`=%d then result else 0 end) item' % (join_results[0])
        query_item = int(join_results[0])
    query_item_name = Statistic.objects.values('name').get(id = query_item)
    if query_type == 0:
        query_sql = 'select %s from result r JOIN `servers` s ON r.`server_id` = s.`id` where r.`statistic_id` = %d %s %s GROUP BY r.`server_id` ORDER BY `item` DESC LIMIT %s' % (select_str, query_item, query_date, q_str, limit_count)
    else:
        query_sql = 'select %s from result r JOIN `channel` c ON r.`channel_id` = c.`id` where r.`statistic_id` = %d %s %s GROUP BY r.`channel_id` ORDER BY `item` DESC LIMIT %s' % (select_str, query_item, query_date, q_str, limit_count)
    count_sql = 'select count(0) result from (%s) newTable WHERE 1' % (query_sql)
    cursor.execute(count_sql)
    total_record = int(cursor.fetchone()[0])
    print query_sql
    list_record = []
    if total_record > 0:
        cursor.execute(query_sql)
        list_record = cursor.fetchall()

    parg = {}
    template = ''
    if 1 == display_type: 
        
        template = 'charts/result_pie.html'
        
        data = []
        total = 0
        if total_record > 0:
            for val in list_record:
                total += int(val[1])
            print 'total',total
            for item in list_record:
                item = list(item)
                item[0] = item[0]
                data.append(['%s'%item[0],float(item[1])/total])
        data = str(data).replace('(', '[').replace(')', ']').replace('L', '')
        data = str(data).replace('u\'', '\'')
        
    else:
        charts_type = 'bar'
        template = 'charts/result_top.html'
        title = "TOP10"
        data = []
        xAxis = []
        if total_record > 0:
            for item in list_record:
                item = list(item)
                xAxis.append('%s'%item[0])
                data.append(int(item[1]))         
        xAxis = str(xAxis).replace('(', '[').replace(')', ']').replace('L', '')
        xAxis = str(xAxis).replace('u\'', '\'') 
        parg["xAxis"] = xAxis
    
    
    parg["server_list"] = server_list
    parg["channel_list"] = channel_list
    parg["title"] = title
    parg["item_results"] = item_results
    parg["data"] = data
    parg["query_item"] = query_item
    parg["query_item_name"] = query_item_name
    parg["charts_type"] = charts_type
    parg["query_id"] = query_id
    parg["sdate"] = sdate[0:10]
    parg["edate"] = edate[0:10]
    parg["query_type"]  = query_type
    parg["d_type"] = display_type
    
    return render_to_response(template, parg)

def get_statistic_in_query(queryid):
    sql = "SELECT S.id, S.`name`, S.exec_interval, S.log_type FROM query_result_statistic AS QR, statistic AS S WHERE QR.statistic_id = S.id AND QR.queryresult_id = %d ORDER BY QR.id" % queryid
 
    cursor = connection.cursor()
    cursor.execute(sql)
    list_record = cursor.fetchall()
    return list_record    
