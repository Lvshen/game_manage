#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from GameManage.models.log import Query, Statistic, Log, LogDefine, Result, ValueDefine,FieldDefine
from GameManage.models.center import Server
from GameManage.views.base import  get_server_list
from GameManage.statistic_module import StatisticModule
from GameManage.log_cfg import ENUM_LOG_STATUS
from GameManage.views.task import task_response
from GameManage.views.base import GlobalPathCfg
from django.http import HttpResponseRedirect, HttpResponse
from GameManage.views.log import the_statistic_in_center
from GameManage.cache import center_cache
from GameManage.views.base import OperateLogManager
import json, datetime, time


def statistic_list(request, log_type=0):
    list_model = []
    log_type = int(log_type)
    if log_type == 0:
        log_type = int(request.GET.get('log_type', '0'))
        
    if log_type == 0:
        list_model = Statistic.objects.all()
    else:
        list_model = Statistic.objects.filter(log_type=log_type)
    server_id = int(request.GET.get('server_id', '0')) 
    list_server = get_server_list()
    list_log = LogDefine.objects.using('read').all()
    
    logDefine_list = LogDefine.objects.using('read').all()
    logDefineIdName = {}
    ResultTimes = {}
    
    not_center_log_id_list = []
    
    for logDefineItem in logDefine_list:
        logDefineIdName[logDefineItem.id] = logDefineItem.key
        if logDefineItem.status != ENUM_LOG_STATUS.SAVE_CENTER:
            not_center_log_id_list.append(logDefineItem.id)
    
    if server_id > 0:
        result_list = Result.objects.raw('select max(id) id,statistic_id,max(result_time) result_time from result where server_id=%d group by statistic_id' % server_id) 
    else:
        result_list = Result.objects.raw('select max(id) id,statistic_id,max(result_time) result_time from result group by statistic_id')
    
    for item in result_list:
        ResultTimes[item.statistic_id] = item.result_time
    
    
    for item in list_model:
        item.log_typeName = logDefineIdName.get(item.log_type, 0)
        item.last_exec_time = ResultTimes.get(item.id, item.last_exec_time)
        #raise Exception, not_center_log_id_list.__contains__(item.log_type)
        if not_center_log_id_list.__contains__(item.log_type):
            item.is_center_log = False
        else:
            item.is_center_log = True 
    
    parg = {}
    parg["log_type"] = log_type
    parg["list_server"] = list_server
    parg["list_log"] = list_log
    parg["list_model"] = list_model
    parg["server_id"] = server_id
    
    return render_to_response('log/statistic_list.html', parg)

def statistic_edit(request, statistic_id=0, log_type=0):
    statistic_id = int(statistic_id)
    log_type = int(log_type)
    
    if 0 == log_type:
        log_type = int(request.GET.get('log_type', 0))
        
    if 0 == statistic_id:
        statistic_id = int(request.GET.get('statistic_id', 0))
    
    if statistic_id > 0 :
        model = Statistic.objects.get(id=statistic_id)
    else :
        model = Statistic()
        model.id = statistic_id
        model.log_type = log_type
        model.name = ''
    logs = LogDefine.objects.using('read').all()
    
    list_field = FieldDefine.objects.using('read').filter(log_type=log_type)
    
    parg = {}
    parg["model"] = model
    parg["list_field"] = list_field
    parg["logs"] = logs
    
    return render_to_response('log/statistic_edit.html', parg)

def statistic_save(request, statistic_id=0):
    statistic_id = int(statistic_id)
    
    if 0 == statistic_id:
        statistic_id = int(request.GET.get('statistic_id', 0))
    
    if statistic_id > 0 :
        model = Statistic.objects.get(id=statistic_id)
    else :
        model = Statistic()
         
    model.log_type = int(request.POST.get('log_type', '0'))
    model.field_name = request.POST.get('field_name', '')
    model.name = request.POST.get('name', '')
    model.where = request.POST.get('where', '')
    model.count_type = int(request.POST.get('count_type', '0'))
    model.exec_interval = int(request.POST.get('exec_interval', '0'))

    model.last_exec_time = request.POST.get('last_exec_time')
    model.sql = request.POST.get('sql', '')
    
    model.is_auto_execute = int(request.POST.get('is_auto_execute', '0'))
    model.auto_exec_interval = int(request.POST.get('auto_exec_interval', '0'))
    model.remark = request.POST.get('remark', '')  
    if model.last_exec_time == '':
        return HttpResponse("请输入开始时间")
    
    
    try:
        model.save(using='write')
        return HttpResponseRedirect('/statistic/list')
    except Exception, e:
        raise Exception, e
        print('statistic save error:', e)
        
    parg = {}
    parg["model"] = model
        
    return render_to_response('log/statistic_edit.html', parg)


def statistic_remove(request, statistic_id=0):
    model_id = int(statistic_id)
    
    if 0 == model_id:
        model_id = int(request.GET.get('statistic_id', 0))
    
    
    if model_id > 0 :
        model = Statistic.objects.get(id=model_id)

        model.delete(using='write')
    
    return render_to_response('feedback.html')

def statistic_execute(request, statistic_id=0, server_id=0):
    #是否自动任务执行
    auto_task = int(request.GET.get('task', 0))
    model_id = int(statistic_id)
    server_id = int(server_id) 
    the_date = request.GET.get('date', '')
    r_date = request.GET.get('rdate', '')
    
    err_msg = ''
    if 0 == model_id:
        model_id = int(request.GET.get('statistic_id', '0'))
        statistic_id = model_id
    
    if 0 == server_id:
        server_id = int(request.GET.get('server_id', '0'))
        
    if the_statistic_in_center(model_id):
        server_id = 0
        
    #是否Ajax批量执行
    is_ajax_batch_execute = request.GET.get('ajax_batch', False)
    
    model = None
    if statistic_id > 0 :
        model = Statistic.objects.using('write').get(id=statistic_id)
    if model == None :
        return HttpResponse("统计对象为空!")
    
    statisticModule = StatisticModule('')
#    statisticModule.getStatistic()
#    statisticModule.getLogDefine()
#    statisticModule.getFieldDefine()
    statisticModule.getServer(server_id)
    result = statisticModule.Result(False, the_date, '', the_date)
    is_error = True
    try:
        s_model = {}
        s_model['id'] = model.id
        s_model['log_type'] = model.log_type
        s_model['count_type'] = model.count_type
        s_model['name'] = model.name
        s_model['field_name'] = model.field_name
        s_model['where'] = model.where
        s_model['sql'] = model.sql
        s_model['exec_interval'] = model.exec_interval
        s_model['last_exec_time'] = model.last_exec_time
        s_model['is_auto_execute'] = model.is_auto_execute
        s_model['auto_exec_interval'] = model.auto_exec_interval
        s_model['remark'] = model.remark
        s_model['result_data'] = model.result_data
        
        result = statisticModule.statistic_execute(s_model, server_id, the_date)
        
    except Exception, ex:
        result = None
        
        msg = u'统计出错, 服务器ID:%s' % server_id
        print 'views#log#statistic.py   exec statistic error'
        print ex
        OperateLogManager.save_operate_log(0, msg, '', '', 1)
        #return HttpResponse(ex)
    
    if None == result:
        is_reload = False
        if the_date != '' and the_date != None:
            last_exec_time = datetime.datetime.strptime(the_date, '%Y-%m-%d %H:%M:%S')
        else:
            last_exec_time = datetime.datetime.now()
        count_sql = '执行出错'
        if r_date == '':
            if the_date == '':
                r_date = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
            else:
                r_date = the_date
    else:
        is_error = False
        is_reload = result.is_reload
        last_exec_time = result.last_exec_time
        count_sql = result.count_sql
        if r_date == '':
            r_date = result.begin_exec_time.strftime('%Y-%m-%d %H:%M:%S')
    
    if is_ajax_batch_execute: 
        tmp_value = 0
        if is_reload:
            tmp_value = 1
             
        result_str = json.dumps({'is_error': is_error,'is_reload':tmp_value, 'date':str(last_exec_time)})
        
        return HttpResponse(result_str);
    
    #print 'views#log#statistic.py  is_reload:::', is_reload
    if not is_reload:
        last_exec_time = datetime.datetime.strptime(r_date, '%Y-%m-%d %H:%M:%S')
        
        if not is_ajax_batch_execute and not the_statistic_in_center(statistic_id):
            server_list = center_cache.get_server_list()
            server_list = sorted(server_list, key=lambda item : item.id)
            
            server_flag = False
                
            server_list_last_index = server_list.__len__() - 1
            
            if 0 == server_id and server_list_last_index >= 0:
                server_flag = True
            
            for index, item in enumerate(server_list):
                if server_flag:
                    server_id = item.id
                    break
                if item.id == server_id and server_list_last_index != index:
                    server_flag = True
                
            if server_flag:
                is_reload = True
    
    if 0 != auto_task:
        task_result = None
        gl_cfg = GlobalPathCfg()
        current_url = gl_cfg.get_current_url(request)
        p_index = current_url.find('?')
        
        if -1 != p_index:
            current_url = '%s?task=1&statistic_id=%s&server_id=%s' % (current_url[:p_index], model_id, server_id)
        
        if is_reload:
            task_result = task_response.SleepTask(5, current_url)
        else:
            #next_time = time.mktime((last_exec_time + datetime.timedelta(seconds = model.exec_interval)).timetuple())
            #print 'auto_task [%s] statistic_id:%s next_time:%s', (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), statistic_id, next_time)
            #task_result = task_response.FinishTask(next_time, current_url)
            task_result = task_response.IntervalTask(model.exec_interval)
            
        return task_response.task_response(task_result)
    
            
    
    parg = {}
    parg["statistic_id"] = statistic_id
    parg["is_reload"] = is_reload
    parg["err_msg"] = err_msg
    parg["last_exec_time"] = last_exec_time
    parg["r_date"] = r_date
    parg["server_id"] = server_id
    parg["model"] = model
    parg["count_sql"] = count_sql
    
    return render_to_response('log/statistic_execute.html', parg)


def batch_statistic(request):
    statistic_id = int(request.GET.get('statistic_id'))
    
    if 0 == statistic_id:
        return HttpResponse('没有选择统计项')
    
    statistic = Statistic.objects.get(id = statistic_id)
    
    list_server = get_server_list()
    
    parg = {}
    parg['statistic'] = statistic
    parg['list_server'] = list_server
    
    return render_to_response('log/batch_statistic.html', parg)
    
    
    
    
