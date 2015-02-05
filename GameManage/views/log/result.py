#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from GameManage.models.log import Log, LogDefine, ValueDefine, FieldDefine, Statistic, Result, QueryResult
from django.http import HttpResponseRedirect
from django.db import connection 
from GameManage.cache import center_cache
from GameManage.views.base import UserStateManager, get_server_list
from GameManage.models.center import  Channel, Group
import datetime, time
#from collections import OrderedDict
from GameManage.views.log.exprot_file import QueryExprot
'''
统计相关 ，重要
'''
def result_list(request, statistic_id=0, show_type='list'):
    statistic_id = int(statistic_id)
    if 0 == statistic_id:
        statistic_id = int(request.GET.get('id', request.POST.get('id', 0)))
    
    statistic_type = 0#int(statistic_type)
    the_date = datetime.datetime.now()
    sdate = request.GET.get('sdate', the_date.strftime('%Y-%m-1'))
    edate = request.GET.get('edate', the_date.strftime('%Y-%m-%d'))
    query_channel = request.GET.getlist('c')#channel_id
    query_server = request.GET.getlist('s')#server_id
    list_record = []
    usm = UserStateManager(request)
    the_user = usm.get_the_user()
    
    statistic = None
    if statistic_id > 0:
        statistic = Statistic.objects.get(id=statistic_id)
    
    log_def = LogDefine.objects.get(id = statistic.log_type)
    
    if statistic == None or log_def == None:
        return HttpResponseRedirect('/statistic/list')

    canSelectServer = True
    
    #if the_log_in_center(log_def): #check_user 
        #canSelectServer = False 
      
    
    if usm.current_userRole_is_root():
        list_server = get_server_list()
    else: 
        list_server = the_user.server.all().order_by("id")
    
    if canSelectServer:
        for serverItem in list_server:
            if len(query_server) > 0:
                if str(serverItem.id) in query_server:
                    serverItem.is_show = 1    
            else:
                serverItem.is_show = 1
    
    if usm.current_userRole_is_root():
        list_channel = center_cache.get_channel_list()
    else:
        list_channel = center_cache.get_user_channel_list(the_user)
    
    #新增激活特殊处理， 因为新增激活没有服务器id
    if statistic_id != 1:
        if query_server.__len__() <= 0:
            query_server = []
            for item in list_server:  
                query_server.append(str(item.id))
    
    channel_condition = True
     
    if query_channel.__len__() == 0:
        query_channel = []
        for item in list_channel:
            query_channel.append(str(item.id))
    
     
    for item1 in list_channel:
        if len(query_channel) > 0:
            if str(item1.id) in query_channel:
                item1.is_show = 1 
        else:
            item1.is_show = 0#取消默认全选  -zhenwei 2012-10-24
    
    query_date = ''
    try:
        if sdate != '':
            sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d').strftime('%Y-%m-%d')
            query_date = ' and result_time>=\'%s\'' % sdate
        if edate != '':
            if query_date != '':
                query_date += ' and '
            edate = datetime.datetime.strptime(edate, '%Y-%m-%d').strftime('%Y-%m-%d')# %H:%M:%S
            query_date += ' result_time<=\'%s\'' % edate
    except:
        sdate = ''
        edate = ''
    
    query_channel_str = ''
    
   
    server_condition = True
     
    if (usm.user_server_count() == 0 or usm.is_Administrator(the_user)) and (list_server.__len__() == query_server.__len__()):
        server_condition = False
        
    if statistic_id == 1:#新增激活特殊处理，不筛选服务器
        server_condition = False
    
    if (usm.user_channel_count() == 0  or usm.is_Administrator(the_user)) and (list_channel.__len__() == query_channel.__len__()):
        channel_condition = False
    
    if channel_condition:
        query_channel_str = ' and channel_id in (%s)' % (','.join(query_channel))
    
    query_server_str = ''
    if server_condition:
        query_server_str = ' and server_id in (%s)' % (','.join(query_server))
    
     
    page_size = 20
    page_num = int(request.GET.get('page_num', '1'))
    if page_num < 1:
        page_num = 1
    
    spos = (page_num - 1) * page_size
    
    statistic_types = [{'id':0, 'name':'默认统计', 'key':''},
                     {'id':1, 'name':'按小时', 'key':'hour'},
                     {'id':2, 'name':'按星期', 'key':'week'},
                     {'id':3, 'name':'按日数', 'key':'day'},
                     {'id':4, 'name':'按月数', 'key':'month'},
                     {'id':5, 'name':'按季度', 'key':'quarter'}]#{'id':5,'name':'按年份','key':'year'}
    statistic_type_str = statistic_types[statistic_type]['key']
    
    list_statistic = Statistic.objects.using('read').filter(log_type=statistic.log_type)
    
    cursor = connection.cursor()
    count_sql = 'select count(distinct result_time) as result from result where statistic_id=%s%s%s%s' % (statistic_id, query_server_str, query_channel_str, query_date)
    
    cursor.execute(count_sql)
    total_record = int(cursor.fetchone()[0])
    #raise Exception, count_sql
    #cursor.close()
    list_record_arr = {}
    if total_record > 0 :
        list_record = Result.objects.raw('select id,statistic_id,result_time,sum(result) result from result where statistic_id=%s%s%s%s group by result_time ORDER BY result_time DESC limit %d,%d' % (statistic_id, query_server_str, query_channel_str, query_date, spos, page_size))

    tmp_item = []
    temp = 0
    for item in list_record:
        temp = int(time.mktime(datetime.datetime.strptime(str(item.result_time),"%s"%'%Y-%m-%d %H:%M:%S').timetuple())) * 1000;
        tmp_item.append([temp,int(item.result)])
        list_record_arr[statistic.name] = tmp_item
    for key,val  in list_record_arr.items():
        list_record_arr[key] = sorted(val)
    list_record_arr = str(list_record_arr).replace('(', '[').replace(')', ']').replace('L', '')
    list_record_arr = str(list_record_arr).replace('u\'', '\'')
              
    if show_type == 'list':
        template = 'log/result_list.html'
    else:
        template = 'log/result_chart.html'
    
    parg = {}
    parg["statistic"] = statistic
    parg["usm"] = usm
    parg["statistic_id"] = statistic_id
    parg["list_statistic"] = list_statistic
    parg["canSelectServer"] = canSelectServer
    parg["list_server"] = list_server
    parg["list_channel"] = list_channel
    parg["sdate"] = sdate
    parg["edate"] = edate
    parg["statistic_type"] = statistic_type
    parg["list_record"] = list_record
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    parg["list_record_arr"] = list_record_arr 
    if query_channel.__len__() == 1:
        parg["channel_id"]  = int(query_channel[0])    
    return render_to_response(template, parg)

def result_remove(request, model_id=0):
    model_id = int(model_id)
    if model_id > 0 :
        model = Result.objects.get(id=model_id)

        model.delete(using='write')
    
    return render_to_response('feedback.html')


def result_clear(request, statistic_id=0):
    statistic_id = int(statistic_id)
    if statistic_id == 0:
        statistic_id = int(request.GET.get('statistic_id', '0'))
    
    if statistic_id > 0: 
        Result.objects.filter(statistic__id=statistic_id).delete()
         
    return render_to_response('feedback.html')
    


def result_query_list(request): 
    list_model = QueryResult.objects.using('read').all()
    parg = {}
    parg["list_model"] = list_model
    return render_to_response('log/result_query_list.html', parg)


def result_query_edit(request, model_id=0):
    model_id = int(model_id)
     
    if 0 == model_id:
        model_id = int(request.GET.get('model_id', request.POST.get('model_id', 0)))
    
    if model_id > 0:
        model = QueryResult.objects.get(id=model_id)
    else:
        model = QueryResult()
        model.id = 0
    
    list_statistic = Statistic.objects.using('read').all()
    selected_statistic = get_statistic_in_query(model_id)
    list_selected = {}
    for item in selected_statistic:
        list_selected[item[0]] = ''
    
    if model.id > 0:
        for item in list_statistic:
            if list_selected.get(item.id, None) != None:
                item.is_show = 1
            else:
                item.is_show = 0
    
    parg = {}
    parg["model"] = model
    parg["list_statistic"] = list_statistic
    
    return render_to_response('log/result_query_edit.html', parg)



def get_statistic_in_query(queryid):
    sql = "SELECT S.id, S.`name`, S.exec_interval, S.log_type FROM query_result_statistic AS QR, statistic AS S WHERE QR.statistic_id = S.id AND QR.queryresult_id = %d ORDER BY QR.id" % queryid
 
    cursor = connection.cursor()
    cursor.execute(sql)
    list_record = cursor.fetchall()
    return list_record

def result_query_save(request, model_id=0):
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('model_id', request.POST.get('model_id', 0)))
    
    if model_id > 0:
        model = QueryResult.objects.get(id=model_id)
    else:
        model = QueryResult()
        #model.id = 0
        
    model.name = request.POST.get('name', '')
    model.remark = request.POST.get('remark', '')    
    err_msg = ''
    try:
        if model.id > 0:
            model.statistic.clear()
        model.save(using='write')
        
        statistic_id_str = request.POST.get('result_list') 
        for statistic_id in statistic_id_str.split('|'):
            statistic_id = int(statistic_id)
            statistic_item = Statistic.objects.using('write').get(id=statistic_id)
            
            model.statistic.add(statistic_item) 
        return HttpResponseRedirect('/result/query/list')
    except Exception, e:
        print('notice save error:', e)
        err_msg = e
    
    parg = {}
    parg["model"] = model
    parg["err_msg"] = err_msg
    
    return render_to_response('log/result_query_edit.html', parg)


def result_query_remove(request, model_id=0):
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('model_id', request.POST.get('model_id', 0)))
        
    if model_id > 0 :
        model = QueryResult.objects.get(id=model_id)
        model.statistic.clear()
        model.delete(using='write')
    
    return render_to_response('feedback.html')

def result_query(request, query_id=0, show_type='list'):
    query_id = int(query_id)
    tmp_group_id = request.GET.get('group_id', 0)
    group_id = 0
    try:
        group_id =  int(tmp_group_id)
    except:
        pass
    query_channel = request.GET.getlist('c')#channel_id
    usm = UserStateManager(request)
    the_user = usm.get_the_user()
    
    if usm.current_userRole_is_root():
        list_channel = center_cache.get_channel_list()
    else:
        list_channel = center_cache.get_user_channel_list(the_user)
        
    for item1 in list_channel:
        if query_channel.__len__() > 0:
            if str(item1.id) in query_channel:
                item1.is_show = 1 
        else:
            item1.is_show = 1
    
    query_server = request.GET.getlist('s')#server_id
    
    the_query = QueryResult.objects.get(id=query_id)
    
    list_statistic = the_query.statistic.all()
    
    list_statistic_sort = get_statistic_in_query(query_id)#获取根据关联表ip排序的数据
    
    join_results = []
    list_statistic_name = []
    exec_interval = 0
    item_results = []
    for item in list_statistic_sort:
        exec_interval = item[2]#exec_interval
        join_results.append(str(item[0]))#id
        item_results.append([item[0], item[1]])
        
        #处理统计数据 
    
    list_group = []
    
    if usm.current_userRole_is_root():
        list_group = Group.objects.all()
        if 0 != group_id:
            list_server = Group.objects.get(id = group_id).server.all()
        else:
            list_server = get_server_list()
    else:
        list_server = the_user.server.all().order_by("id")
    
    #if canSelectServer:
    for serverItem in list_server:
        if len(query_server) > 0:
            if str(serverItem.id) in query_server:
                serverItem.is_show = 1    
        else:
            serverItem.is_show = 1
    
    sdate = request.GET.get('sdate', '')
    edate = request.GET.get('edate', '')
#    print(sdate,edate)

    
    if query_channel.__len__() == 0 and not usm.current_userRole_is_root():
        query_channel = []
        for item in list_channel:
            query_channel.append(str(item.id))
    
    if query_server.__len__() == 0  and not usm.current_userRole_is_root():
        query_server = []
        for item in list_server:  
            query_server.append(str(item.id))
        
    query_channel_str = ''
    if query_channel.__len__() > 0 :
        query_channel_str = ' and channel_id in (%s)' % (','.join(query_channel))
    
    query_server_str = ''
    if query_server.__len__() > 0 :
        query_server_str = ' and server_id in (%s)' % (','.join(query_server))
        
    page_size = 20
    page_num = int(request.GET.get('page_num', '1'))
    if page_num < 1:
        page_num = 1
    
    spos = (page_num - 1) * page_size

    date_format = '%%Y-%%m-%%d'
    chart_format = '%Y-%m-%d'
    time_slot = 86400000     
    charts_type = 'spline'
    def_date = request.GET.get("def_date","")

    now = datetime.datetime.now()
    if sdate and edate:
        d1 = datetime.datetime(int(sdate.split("-")[0]),int(sdate.split("-")[1]),int(sdate.split("-")[2]))
        d2 = datetime.datetime(int(edate.split("-")[0]),int(edate.split("-")[1]),int(edate.split("-")[2]))
        days = ( d2 - d1).days + 1
        if days == 1:
            charts_type = 'column'   
        time_slot = Result().cmp_time(days)
    else:
        sdate = now.strftime('%Y-%m-01')
        edate = now.strftime('%Y-%m-%d')
           
    if def_date == 'day':
        pass
    elif def_date == 'month':
        date_format = '%%Y-%%m'
        chart_format = '%Y-%m'
        time_slot = 30 * 86400000
    elif def_date == 'year':
        date_format = '%%Y'
        chart_format = '%Y'
        time_slot = 12 * 30 * 86400000
    edate = datetime.datetime.strptime(edate, '%Y-%m-%d')
    edate = edate + datetime.timedelta(days=1)
    sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d')
    query_date = ' AND `result_time` >= \'%s\' AND `result_time` < \'%s\''%(sdate, edate) 
                            
    cursor = connection.cursor()
    count_sql = 'select count(distinct DATE_FORMAT(result_time,"%s")) result from result where statistic_id in(%s)%s%s%s' % (date_format,','.join(join_results), query_server_str, query_channel_str, query_date)
    cursor.execute(count_sql)
    total_record = int(cursor.fetchone()[0])
    
    list_record = []

        
    if total_record > 0:
        select_str = 'DATE_FORMAT(result_time,"%s") AS `date`'% date_format
        for item in join_results:
            select_str += ',sum(case when `statistic_id`=%s then result else 0 end) item%s' % (item, item)
        
        query_sql = 'select %s from result where statistic_id in(%s)%s%s%s group by `date` order by `date` DESC limit %d,%d' % (select_str, ','.join(join_results), query_server_str, query_channel_str, query_date, spos, page_size)
        print(query_sql)
        cursor.execute(query_sql)
        list_record = cursor.fetchall()
    #cursor.close()
    
    #print total_record
    #print '------------------'
    #print query_sql
    if show_type == 'list':
        template = 'log/result_query.html'
    else:
        template = 'log/result_query_chart.html'
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
    for key,val  in list_record_arr.items():
        list_record_arr[key] = sorted(val)
    list_record_arr = str(list_record_arr).replace('(', '[').replace(')', ']').replace('L', '')
    list_record_arr = str(list_record_arr).replace('u\'', '\'')

    list_statistic_name = str(list_statistic_name).replace('u\'', '\'') 
    
    parg = {}
    parg["usm"] = usm
    parg["query_id"] = query_id
    parg["list_statistic"] = list_statistic 
    parg["list_group"] = list_group
    parg["group_id"] = group_id
    parg["list_server"] = list_server
    parg["list_channel"] = list_channel
    parg["sdate"] = sdate.strftime('%Y-%m-%d')
    edate = edate - datetime.timedelta(days = - 1)
    parg["edate"] = edate.strftime('%Y-%m-%d')
    parg["list_statistic_sort"] = list_statistic_sort
    parg["list_record"] = list_record
    parg["exec_interval"] = exec_interval
    parg["list_record_arr"] = list_record_arr
    parg["list_statistic_name"] = list_statistic_name
    if query_channel.__len__() == 1:
        parg["channel_id"]  = int(query_channel[0])
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    
    parg["def_date"] = def_date
    parg["time_slot"] = time_slot
    parg["charts_type"] = charts_type
    parg["chart_format"] = chart_format
    return render_to_response(template, parg)

def result_analyse(request, query_id=0, show_type='list'):
    query_id = int(query_id)
    base_group_id = int(request.GET.get('base_group_id', 0))
    op_group_id = int(request.GET.get('op_group_id', 0))
    query_statistic_item = request.GET.getlist('f')
    query_item = request.GET.get('query_item', 0)
    select_op = request.GET.get("select_op","")
    query_channel = request.GET.getlist('c')#channel_id
    
    usm = UserStateManager(request)
    the_user = usm.get_the_user()
    
    query_channel_1 = ''
    query_channel_2 = ''
    channel_1 = int(request.GET.get('channel_1', 0))
    channel_2 = int(request.GET.get('channel_2', 0))


    if channel_1:
        query_channel_1 = ' and channel_id = %d ' % channel_1
    if channel_2:
        query_channel_2 = ' and channel_id = %d ' % channel_2
        
    if usm.current_userRole_is_root():
        list_channel = center_cache.get_channel_list()
    else:
        list_channel = center_cache.get_user_channel_list(the_user)
        
    for item1 in list_channel:
        if query_channel.__len__() > 0:
            if str(item1.id) in query_channel:
                item1.is_show = 1 
        else:
            item1.is_show = 1
    
    query_server1 = request.GET.getlist('s1')#server_id
    query_server2 = request.GET.getlist('s2')#server_id
    base_server = request.GET.get('base_server','')
    op_server = request.GET.get('op_server','')
    if not base_server:
        if query_server1.__len__() > 0:
            base_server = ','.join(query_server1)
    elif not query_server1:
        query_server1  = base_server.split(',')
    elif query_server1:
        base_server  = ','.join(query_server1)
        
    if not op_server:
        if query_server2.__len__() > 0:    
            op_server = ','.join(query_server2)
    elif not query_server2:
        query_server2  = op_server.split(',') 
    elif query_server2:
        op_server  = ','.join(query_server2)
    
    the_query = QueryResult.objects.get(id=query_id)
    
    list_statistic = the_query.statistic.all()
    
    list_statistic_sort = get_statistic_in_query(query_id)#获取根据关联表ip排序的数据
    
    join_results = []
    list_statistic_name = []
    exec_interval = 0
 
    statistic_results = []
    canSelectServer = True
    item_results = []
    for item in list_statistic_sort:
        statistic_results.append(str(item[0]))
        join_results.append([str(item[0]),item[1]])#id
        item_results.append(int(item[0]))
               
    for item3 in join_results:
        if query_statistic_item.__len__() > 0:
            query_item = ','.join(query_statistic_item)
            if str(item3[0]) in query_statistic_item:
                item3.append(1)
                list_statistic_name.append(item3[1]) 
        else:
            if query_item:
                query_statistic_item = query_item.split(',')
            item3.append(1)
            list_statistic_name.append(item3[1]) 
    
    list_group = []
    
    if usm.current_userRole_is_root():
        list_group = Group.objects.all()
        if 0 != base_group_id:
            list_server_base = Group.objects.get(id = base_group_id).server.all()
        else:
            list_server_base = get_server_list()
        if 0 != op_group_id:
            list_server_op = Group.objects.get(id = op_group_id).server.all()
        else:
            list_server_op = get_server_list()            
    else:
        list_server_base = the_user.server.all().order_by("id")
        list_server_op = the_user.server.all().order_by("id")
    
    #if canSelectServer:
    for serverItem in list_server_base:

        if len(query_server1) > 0:
            if str(serverItem.id) in query_server1:
                serverItem.is_show = 1    
        else:
            serverItem.is_show = 1

    for serverItem in list_server_op:

        if len(query_server2) > 0:
            if str(serverItem.id) in query_server2:
                serverItem.is_show = 1    
        else:
            serverItem.is_show = 1
                
    the_date = datetime.datetime.now()
    sdate = request.GET.get('sdate', the_date.strftime('%Y-%m-1'))
    edate = request.GET.get('edate', the_date.strftime('%Y-%m-%d'))
#    print(sdate,edate)
    query_date = ''
    try:
        if sdate != '':
            sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d').strftime('%Y-%m-%d')# %H:%M:%S
            query_date = ' and result_time>=\'%s\'' % sdate
        if edate != '':
            if query_date != '':
                query_date += ' and '
            edate = datetime.datetime.strptime(edate, '%Y-%m-%d').strftime('%Y-%m-%d')
            query_date += ' result_time<=\'%s\'' % edate
    except:
        sdate = ''
        edate = ''
    
    if query_channel.__len__() == 0 and not usm.current_userRole_is_root():
        query_channel = []
        for item in list_channel:
            query_channel.append(str(item.id))
    
    if query_server1.__len__() == 0  and not usm.current_userRole_is_root():
        query_server1 = []
        for item in list_server_base:  
            query_server1.append(str(item.id))

    if query_server2.__len__() == 0  and not usm.current_userRole_is_root():
        query_server2 = []
        for item in list_server_op:  
            query_server2.append(str(item.id))
                    
#    query_channel_str = ''
#    if query_channel.__len__() > 0 :
#        query_channel_str = ' and channel_id in (%s)' % (','.join(query_channel))
#    
    query_server_str1 = ''
    query_server_str2 = ''
    if query_server1.__len__() > 0 :
        query_server_str1 = ' and server_id in (%s)' % (','.join(query_server1))

    if query_server2.__len__() > 0 :
        query_server_str2 = ' and server_id in (%s)' % (','.join(query_server2))
                
    page_size = int(request.GET.get('page_size',15))
    page_num = int(request.GET.get('page_num', '1'))
    if page_num < 1:
        page_num = 1
    
    spos = (page_num - 1) * page_size

    if query_statistic_item.__len__() == 1:
        count_statistic = ''.join(query_statistic_item)
    elif query_statistic_item.__len__() > 1:
        count_statistic = ','.join(query_statistic_item)
    else:
        count_statistic = ','.join(statistic_results)
        
    date_format = '%%Y-%%m-%%d'
    chart_format = '%Y-%m-%d'
    def_date = request.GET.get("def_date","")
    minTickSize = [1,"day"]
    if def_date == 'day':
        pass
    elif def_date == 'month':
        date_format = '%%Y-%%m'
        chart_format = '%Y-%m'
        minTickSize = [1,"month"]
    elif def_date == 'year':
        date_format = '%%Y'
        chart_format = '%Y'
        minTickSize = [1,"year"]
            
    cursor = connection.cursor()


        
    select_str1 = 'DATE_FORMAT(result_time,"%s") AS `date`'% date_format
    select_str2 = 'DATE_FORMAT(result_time,"%s") AS `date`'% date_format
    select_str12 = 'a.`date`'
    for item in query_statistic_item:
        select_str1 += ',sum(case when `statistic_id`=%s then result else 0 end) item%s' % (item, item)
        select_str2 += ',sum(case when `statistic_id`=%s then result else 0 end) item%s' % (item, item)
        select_str12 += ',(a.`item%s`-b.`item%s`) item%s' % (item,item,item)

    if select_op == '0':
        query_sql1 = 'select %s from result where statistic_id in(%s)%s%s group by `date` ORDER BY `date` DESC ' % (select_str1, count_statistic, query_server_str1, query_date)
        query_sql2 = 'select %s from result where statistic_id in(%s)%s%s group by `date` ORDER BY `date` DESC ' % (select_str2, count_statistic, query_server_str2, query_date)
    else:
        query_sql1 = 'select %s from result where statistic_id in(%s)%s%s group by `date` ORDER BY `date` DESC ' % (select_str1, count_statistic, query_channel_1, query_date)
        query_sql2 = 'select %s from result where statistic_id in(%s)%s%s group by `date` ORDER BY `date` DESC ' % (select_str2, count_statistic, query_channel_2, query_date)
        
    query_sql = 'SELECT %s from (%s) a join (%s) b ON a.`date` = b.`date`'%(select_str12,query_sql1,query_sql2)
    count_sql = 'select count(*) result from (%s) newTable WHERE 1 %s' % (query_sql, '')
    cursor.execute(count_sql)
    total_record = int(cursor.fetchone()[0])

    list_record = []
    if total_record > 0:
        query_sql = query_sql + ' ' + 'LIMIT %s,%s'%(spos,page_size)
        cursor.execute(query_sql)
        list_record = cursor.fetchall()
    #cursor.close()
    
#    print(total_record,query_sql)
    if show_type == 'list':
        template = 'log/result_analyse.html'
    else:
        template = 'log/result_query_chart.html'
    list_record_arr = {}
    i = 1
    tmp_item = []
    
    for item_result in join_results:
        if item_result[0] in query_statistic_item:
            tmp_item = []
            for item in list_record:
                item = list(item)
                item[0] = int(time.mktime(datetime.datetime.strptime(str(item[0]),"%s"%chart_format).timetuple())) * 1000;
                tmp_item.append([item[0],int(item[i])])
                list_record_arr[item_result[1]] = tmp_item
            i = i+1
    for key,val  in list_record_arr.items():
        list_record_arr[key] = sorted(val) 
    list_record_arr = str(list_record_arr).replace('(', '[').replace(')', ']').replace('L', '')
    list_record_arr = str(list_record_arr).replace('u\'', '\'')
    
    time_slot = 86400000
    if def_date == 'day':                                               
        d1 = datetime.datetime(int(sdate.split("-")[0]),int(sdate.split("-")[1]),int(sdate.split("-")[2]))
        d2 = datetime.datetime(int(edate.split("-")[0]),int(edate.split("-")[1]),int(edate.split("-")[2]))
        days = ( d2 - d1).days +1
    
        time_slot = Result().cmp_time(days)
    elif def_date == 'month':
        time_slot = 86400000 * 30
    elif def_date == 'year':
        time_slot = 86400000 * 30 * 12
    #处理 导出文件
    exprot = int(request.GET.get('exprot', '0'))
    close_export = int(request.GET.get('close_export', '0'))
    clear_export_old_file = int(request.GET.get('clear_export_old_file', '0'))    
    if 0< exprot: 
        query_exprot = QueryExprot()
        file_name = ''.join(query_statistic_item)
        file_name = file_name+'___'+sdate.replace('-','').replace(':','')+'___'+edate.replace('-','').replace(':','')
        #session ID 
        session_id = request.COOKIES.get('sessionid')
        return query_exprot.gene_file(list_record, [u'时间']+list_statistic_name, file_name, page_num, page_size, total_record, exprot, close_export, clear_export_old_file, session_id)
            
    parg = {}
    parg["usm"] = usm
    parg["query_id"] = query_id
    parg["list_statistic"] = list_statistic 
    parg["list_group"] = list_group
    parg["base_group_id"] = base_group_id
    parg["op_group_id"] = op_group_id
    parg["list_server_base"] = list_server_base
    parg["list_server_op"] = list_server_op
    parg["list_channel"] = list_channel
    parg["base_server"] = base_server
    parg["op_server"] = op_server
    parg["sdate"] = sdate
    parg["edate"] = edate
    parg["list_statistic_sort"] = list_statistic_sort
    parg["list_record"] = list_record
    parg["exec_interval"] = exec_interval
    parg["list_record_arr"] = list_record_arr
    parg["list_statistic_name"] = list_statistic_name
    
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    parg["select_op"] = select_op
    parg["canSelectServer"] = canSelectServer
    parg["channel_1"] = channel_1
    parg["channel_2"] = channel_2
    parg["def_date"] = def_date
    parg["minTickSize"] = minTickSize
    parg["join_results"] = join_results   
    parg["time_slot"] = time_slot
    parg["chart_format"] = chart_format
    parg["query_item"] = query_item
    return render_to_response(template, parg)
