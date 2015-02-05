#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from GameManage.models.center import Server
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connections
from GameManage.models.backup import Backup
from GameManage.views.log.exprot_file import QueryExprot
import datetime, calendar
from GameManage.views.base import mkdir
from GameManage.views.base import UserStateManager, getConn
import re
import json
import time
from GameManage.views.task.task_response import SleepTask, task_response, IntervalTask
from GameManage.models.task import TaskDefine
import os
from django.db.models import Q
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    
# 备份列表
def backup_list(request):
    date = request.GET.get('date', '')
    key = request.GET.get('key', '')
    if date != '' and key == 'fe!y!n':
        import glob
        from GameManage.settings import STATIC_ROOT 
        file_str = '<table>'
        file_list = glob.glob(r'%s/export/feiyin/%s/*.txt' % (STATIC_ROOT, date))
        
        for name in file_list:
            file_str += '<tr><td><a href="%s">%s</a></td></tr>' % (name[name.find('/static/'):].replace('\\', '/'), os.path.basename(name))
        file_str += '</table>'
        return HttpResponse(file_str)
    backup_type = request.POST.get('type', '')
    page_num = int(request.GET.get('page_num', '1'))
    page_size = 50    
    
    query = Q()
    
    if backup_type:
        query = query & Q(type=backup_type)
    total_record = Backup.objects.filter(query).count()
    #list_data = Backup.objects.all().order_by('id')
    list_data = []
    if 0 < total_record:    
        list_data = Backup.objects.filter(query)[(page_num - 1) * page_size:page_num * page_size]
    server_id = int(request.GET.get('server_id', '0')) 
    query = []
    query.append(" `status` not in (-1,0) AND `log_db_config` NOT REGEXP '\"fy\"'")
    list_server = Server.objects.using('read').extra(where=[''.join(query)]).order_by('id')
    server_list = []
    for item in list_server:
        server_list.append(int(item.id))
    type_list = Backup.objects.values('type').distinct() 
    parg = {}
    parg["type"] = backup_type
    parg["type_list"] = type_list
    parg["list_server"] = list_server
    parg["list_model"] = list_data
    parg["server_id"] = server_id
    parg["server_list"] = server_list
    parg['page_num'] = page_num
    parg['page_size'] = page_size
    parg['total_record'] = total_record    
    return render_to_response('backup/backup_list.html', parg)

# 编辑、添加备份
def backup_edit(request, backup_id=0):
    backup_id = int(backup_id)
    
    if backup_id > 0 :
        model = Backup.objects.get(id=backup_id)
    else :
        model = Backup()
        model.id = backup_id
        model.name = ''
    
    parg = {}
    parg["model"] = model
    
    return render_to_response('backup/backup_edit.html', parg)

# 保存备份
def backup_save(request, backup_id=0):
    backup_id = int(backup_id)
    if backup_id > 0 :
        model = Backup.objects.get(id=backup_id)
    else :
        model = Backup()
         
    model.type = request.POST.get('type', '')
    model.field_name = request.POST.get('field_name', '')
    model.name = request.POST.get('name', '')
    model.url = request.POST.get('url', '')
    model.sql = request.POST.get('sql', '')
    model.backup_format = request.POST.get('backup_format', '')
    model.auto_exec_interval = int(request.POST.get('auto_exec_interval', '0'))
    if request.POST.get('start_date', '') != '':
        model.start_date = request.POST.get('start_date', '') 
    else:
        model.start_date = None
    if request.POST.get('end_date', '') != '':
        model.end_date = request.POST.get('end_date', '') 
    else:
        model.end_date = None        
    model.remark = request.POST.get('remark', '') 
    model.server_list = request.POST.get('server_list', '').strip()
    if model.name == '':
        return HttpResponse("名称不能为空!")
    if model.backup_format == '':
        return HttpResponse("备份格式不能为空!")     
    try:
        model.save(using='write')
        return HttpResponseRedirect('/backup/list')
    except Exception, e:
        raise Exception, e
        print('backup save error:', e)     
    parg = {}
    parg["model"] = model       
    return render_to_response('backup/backup_edit.html', parg)

def backup_del(request, backup_id=0):
    backup_id = int(backup_id)
    if backup_id:
        Backup.objects.filter(id=backup_id).delete()
    return render_to_response('feedback.html')

def backup_execute(request, backup_id=0):
    msg = ''
    from GameManage.settings import STATIC_ROOT
    backup_type = int(request.GET.get("backup_type", "0"))
    page_num = int(request.GET.get('page_num', '1'))
    all_server = int(request.GET.get('all_server', '0'))
    task_id = int(request.GET.get("task_id", "0"))
    page_size = 20
    query_date = ''
    sdate = request.GET.get('sdate', '')
    edate = request.GET.get('edate', '')
    
    date_type = int(request.GET.get('date_type', '0'))
    ajax = request.GET.get('ajax', False)
    exprot = int(request.GET.get('exprot', '0'))
    close_export = int(request.GET.get('close_export', '0'))
    clear_export_old_file = int(request.GET.get('clear_export_old_file', '0'))
    usm = UserStateManager(request)
    server_id = int(request.GET.get('server_id', '0'))
    
    is_select_server = False
    
    if exprot > 0:
        page_size = 500
    is_post_back = request.GET.get('post_back', False)
    now = datetime.datetime.now()
#    if not is_post_back:#如果第一次进入该页面默认时间范围是昨天数据
#        if sdate == '':
#            sdate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
#        if edate == '':
#            edate = now.strftime('%Y-%m-%d 00:00:00')
    pager_str = 'limit %s,%s' % ((page_num - 1) * page_size, page_size)
    err_msg = ''

    backup_id = int(backup_id)
    request_url = ''
    if backup_id > 0:
        the_query = Backup.objects.get(id=backup_id)
        request_url = the_query.sql
    if the_query.field_name.find('feiyin') != -1:
        fields = the_query.field_name
    else:
        fields = the_query.field_name.split(',')
    file_str = the_query.backup_format
    if the_query.auto_exec_interval > 0:
        sleep_time = the_query.auto_exec_interval
    else:
        sleep_time = 10
    query_sql = the_query.sql.replace('\r\n\t', ' ').replace('\r\n', ' ')

    if the_query.sql == '' or -1 != the_query.sql.find('{{server_id}}'):
        is_select_server = True
    
    query = []
    query.append(" `status` not in (-1,0) AND `log_db_config` NOT REGEXP '\"fy\"'")
    list_server = Server.objects.using('read').extra(where=[''.join(query)]).order_by('id')
    if server_id == 0 and len(list_server) > 0:
        server_id = list_server[0].id
    
    if server_id > 0:#支持服务器条件
        query_sql = query_sql.replace('{{server_id}}', str(server_id))
        query_sql = query_sql.replace('{{log_server}}', str(server_id))

    #date_type
    # 1 daily
    # 2 monthly
    # 3 first
    # 4 closed
    date_name = ''
    day_format = ''
    next_time = 0
    file_str_list = file_str.split('___')
    log_type = file_str_list[len(file_str_list)-1]	
    
    start_date = the_query.start_date
    end_date = the_query.end_date
        
    if date_type == 1:
        date_name = 'daily'
        if start_date != '' and start_date != None and start_date != 'None' and task_id > 0:
            sdate = start_date.strftime('%Y-%m-%d 00:00:00')
            edate = start_date.strftime('%Y-%m-%d 23:59:59')
            day_format = start_date.strftime("%Y%m%d")
        else:
            sdate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
            edate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')            
            day_format = (now - datetime.timedelta(days=1)).strftime("%Y%m%d")
        next_time = 86400
    elif date_type == 2:
        date_name = 'monthly'
        today = datetime.date.today()

        current_month_days = calendar.monthrange(today.year, today.month)[1]
        if today.month > 1:
            last_year = today.year
            last_month = today.month - 1    
            last_month_days = calendar.monthrange(today.year, today.month - 1)[1]      
        else:
            last_year = today.year - 1
            last_month = 12
            last_month_days = 31
        sdate = today.strftime('%s-%s-01 00:00:00' % (last_year, last_month))
        edate = today.strftime('%s-%s-%s 23:59:59' % (last_year, last_month, last_month_days))
        day_format = today.strftime("%Y%m01")
        next_time = 86400 * current_month_days
    elif date_type == 3:
        date_name = 'first'
        sdate = '1970-01-01 00:00:00'
        if start_date != '' and start_date != None and start_date != 'None' and task_id > 0:
            edate = start_date.strftime('%Y-%m-%d 23:59:59')
            day_format = start_date.strftime('%Y%m%d')            
        else:
            edate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')
            day_format = (now - datetime.timedelta(days=1)).strftime('%Y%m%d')
        next_time = -86400
    elif date_type == 4:
        date_name = 'closed'
        sdate = '1970-01-01 00:00:00'
        edate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')
        day_format = (now - datetime.timedelta(days=1)).strftime('%Y%m%d')
        next_time = -86400
    elif date_type == 5:
        if sdate == '' or edate == '':
            return HttpResponse(json.dumps({"msg":"时间不能为空"}))
        sdate = sdate
        edate = edate
        
    if query_date == '' :
        query_sql = query_sql.replace("{{qdate}}", query_date)
        query_sql = query_sql.replace('{{sdate}}', '%s' % sdate).replace('{{edate}}', '%s' % edate)#支持自定对非log表的日期支持   -zhenwei 2012-10-25
    count_sql = 'select count(0) from (%s) newTable' % query_sql
    if query_sql.find('limit') == -1:
        query_sql = '%s %s' % (query_sql, pager_str)
        
    if the_query.remark != '':
        is_select_server = False
    
    next_url = 'http://127.0.0.1:8080' + request.META['PATH_INFO'] + '?' + request.META['QUERY_STRING']
    if is_select_server:
        if server_id > 0:
            try: 
                conn = getConn(server_id)
            except:
                err_msg = '数据库链接出错!'
                if backup_type == 1:
                    #save_log('query_view error', next_url,log_type)
                    if Backup().get_server_id(server_id, list_server) != False:
                        next_url = re.sub(r"page_num=\d+", "page_num=1", next_url)
                        next_url = re.sub(r"server_id=\d+", "server_id=%d" % Backup().get_server_id(server_id, list_server), next_url)
                        taskresult = SleepTask(sleep_time, next_url)
                    else:
                        request_url = ''
                        try:
                            if task_id > 0:
                                the_task = TaskDefine.objects.get(id = task_id)
                                if start_date.strftime('%Y-%m-%d') < the_task.trigger_date.strftime('%Y-%m-%d') and start_date.strftime('%Y-%m-%d') < end_date.strftime('%Y-%m-%d') and end_date.strftime('%Y-%m-%d') < the_task.trigger_date.strftime('%Y-%m-%d'):
                                    next_time = int(time.time()) - int(time.mktime(the_task.trigger_date.timetuple())) + sleep_time + 15
                                    the_query.start_date = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                                else:
                                    the_query.start_date = (the_task.trigger_date).strftime('%Y-%m-%d')
                                    the_query.end_date = (the_task.trigger_date).strftime('%Y-%m-%d')
                                the_query.save()   
                                
                                the_task.counter = 0
                                the_task.request_url = the_task.source_url
                                the_task.save()              
                                
                                request_url = the_task.request_url          
                        except Exception,e:
                            print 'task error',e      
                            msg = 'task error %s'%e          
                        save_log('\nall_is_finish!\n next_time %s\n request_url %s\n'%(next_time,request_url), '%s'%msg, log_type)
                             
                        taskresult = IntervalTask(next_time)
                    return task_response(taskresult)             
    else:
        conn = connections['read']
    
    if next_url.find("server_id=") == -1:
        next_url = next_url + '&server_id=%d' % server_id   
    if err_msg != '':
        return render_to_response('feedback.html', locals())
    cursor = conn.cursor()
    try:
        cursor.execute(count_sql)
    except Exception, e:
        print('query_view error:', e)
        if backup_type == 1:
            #save_log('query_view error', next_url,log_type)
            if Backup().get_server_id(server_id, list_server) != False:
                next_url = re.sub(r"page_num=\d+", "page_num=1", next_url)
                next_url = re.sub(r"server_id=\d+", "server_id=%d" % Backup().get_server_id(server_id, list_server), next_url)
                taskresult = SleepTask(sleep_time, next_url)
            else:
                request_url = ''
                try:
                    if task_id > 0:
                        the_task = TaskDefine.objects.get(id = task_id)
                        if start_date.strftime('%Y-%m-%d') < the_task.trigger_date.strftime('%Y-%m-%d') and start_date.strftime('%Y-%m-%d') < end_date.strftime('%Y-%m-%d') and end_date.strftime('%Y-%m-%d') < the_task.trigger_date.strftime('%Y-%m-%d'):
                            next_time = int(time.time()) - int(time.mktime(the_task.trigger_date.timetuple())) + sleep_time + 15
                            the_query.start_date = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                        else:
                            the_query.start_date = (the_task.trigger_date).strftime('%Y-%m-%d')
                            the_query.end_date = (the_task.trigger_date).strftime('%Y-%m-%d')
                        the_query.save()   
                        
                        the_task.counter = 0
                        the_task.request_url = the_task.source_url
                        the_task.save()              
                        
                        request_url = the_task.request_url          
                except Exception,e:
                    print 'task error',e      
                    msg = 'task error %s'%e          
                save_log('\nall_is_finish!\n next_time %s\n request_url %s\n'%(next_time,request_url), '%s'%msg, log_type)
                     
                taskresult = IntervalTask(next_time)
            return task_response(taskresult)             
    total_record = int(cursor.fetchone()[0])
    total_page = total_record / page_size
    if total_record % page_size != 0:
        total_page += 1
    
    list_data = []
    if total_record > 0:
        cursor.execute(query_sql)
        list_data = cursor.fetchall()
    parg = {}
    parg["list_data"] = list_data
    parg["page_num"] = page_num
    parg["total_record"] = total_record
    parg["sdate"] = sdate
    parg["edate"] = edate
    parg["fields"] = fields
    parg["usm"] = usm
    parg["backup_id"] = backup_id
    parg["list_server"] = list_server
    parg["server_id"] = server_id
    #处理 导出文件
    if 0 < exprot: 
        query_exprot = QueryExprot()
        file_name = []
        if file_str == "{{date}}___orders":
            pass
        else:
            the_server = Server.objects.get(id=server_id)
            the_db_config = json.loads(the_server.log_db_config)
            if file_str.find("{{agent_name}}") != -1 and server_id > 0:
                if 'agent_name' in the_db_config.keys():
                        file_str = file_str.replace("{{agent_name}}", the_db_config['agent_name'])
                        
            if file_str.find("{{server_name}}") != -1 and server_id > 0:
                if 'server_name' in the_db_config.keys():
                    file_str = file_str.replace("{{server_name}}", the_db_config['server_name'])
            if file_str.find("{{server_id}}") != -1 and server_id > 0:
                file_str = file_str.replace("{{server_id}}", str(server_id))

            if file_str.find("{{servername}}") != -1 and server_id > 0: 
                file_str = file_str.replace("{{servername}}", the_server.name)
                
        if file_str.find("{{date}}") != -1:
            if date_type == 5:
                file_str = file_str.replace("{{date}}", sdate.replace('-', '').replace(' ', '').replace(':', '') + '___' + edate.replace('-', '').replace(' ', '').replace(':', ''))
                date_name = ''
            else:
                file_str = file_str.replace("{{date}}", day_format)
        file_name.append(u'%s___%s' % (file_str, date_name))
        file_name = ''.join(file_name)
        #session ID 
        session_id = request.COOKIES.get('sessionid')
        if backup_type == 1:
            jsonstr = query_exprot.gene_file(list_data, fields, file_name, page_num, page_size, total_record, exprot, close_export, clear_export_old_file, session_id)
            jsonstr = str(jsonstr)
            jsonstr = jsonstr.split("\n\n")[1]            
            jsonstr = json.loads(jsonstr)
            next_url = re.sub(r"page_num=\d+", "page_num=%d" % jsonstr["page_num"], next_url)
            if jsonstr["is_finish"] == True:
                save_log('server_id:%s_is_finish' % server_id, '%s\t\t\t%s\t\t\t%s' % (file_name, total_record, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), log_type)
                next_url = re.sub(r"page_num=\d+", "page_num=1", next_url)
                if Backup().get_server_id(server_id, list_server) != False and all_server == 1:
                    #save_log('next_server:%s'%Backup().get_server_id(server_id), '',log_type)
                    next_url = re.sub(r"server_id=\d+", "server_id=%d" % Backup().get_server_id(server_id, list_server), next_url)          
                    taskresult = SleepTask(sleep_time, next_url)
                else:
                    request_url = ''
                    try:
                        if task_id > 0:
                            the_task = TaskDefine.objects.get(id = task_id)
                            if start_date.strftime('%Y-%m-%d') < the_task.trigger_date.strftime('%Y-%m-%d') and start_date.strftime('%Y-%m-%d') < end_date.strftime('%Y-%m-%d') and end_date.strftime('%Y-%m-%d') < the_task.trigger_date.strftime('%Y-%m-%d'):
                                next_time = int(time.time()) - int(time.mktime(the_task.trigger_date.timetuple())) + sleep_time + 15
                                the_query.start_date = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                            else:
                                the_query.start_date = (the_task.trigger_date).strftime('%Y-%m-%d')
                                the_query.end_date = (the_task.trigger_date).strftime('%Y-%m-%d')
                            the_query.save()   
                            
                            the_task.counter = 0
                            the_task.request_url = the_task.source_url
                            the_task.save()              
                            
                            request_url = the_task.request_url          
                    except Exception,e:
                        print 'task error',e      
                        msg = 'task error %s'%e          
                    save_log('\nall_is_finish!\n next_time %s\n request_url %s\n'%(next_time,request_url), '%s'%msg, log_type)
                         
                    taskresult = IntervalTask(next_time)
                return task_response(taskresult)             
            else:
                #save_log('%s:%s:%s:%s'%(server_id,total_record,total_page,page_num), '%s#%s'%(sleep_time,next_url),log_type)                   
                taskresult = SleepTask(sleep_time, next_url)
            return task_response(taskresult) 
        #save_log('ajax:%s:%s:%s:%s'%(server_id,total_record,total_page,page_num), next_url,log_type)
        else:
            jsonstr = query_exprot.gene_file(list_data, fields, file_name, page_num, page_size, total_record, exprot, close_export, clear_export_old_file, session_id)   
            return HttpResponse(jsonstr)


def save_log(msg='', url='', log_type=''):
    from GameManage.settings import STATIC_ROOT 
    save_path = r'%s/log/' % (STATIC_ROOT)
    mkdir(save_path)
    today = datetime.datetime.now().strftime("%Y%m%d")
    targetFile = r'%s/log/log_%s_%s.txt' % (STATIC_ROOT, log_type, today)
    fileHandle = open (targetFile, 'a')
    if msg:
        lastFile = r'%s/log/log_%s_%s.txt' % (STATIC_ROOT, log_type, (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y%m%d'))
        if os.path.exists(lastFile):
            os.remove(lastFile)
        fileHandle.write(('%s\t%s\n' % (msg, url)).encode('utf-8'))
    else:
        pass
    fileHandle.close()
    
        
def backup_create(request):
    from GameManage.settings import STATIC_ROOT 
    backup_ids = request.GET.get("backup_ids", "")
    conn = connections['read']
    cursor = conn.cursor()
    if backup_ids != '':
        sql = " WHERE `id` in (%s)" % backup_ids
    else:
        sql = ''
    cursor.execute("SELECT `auto_exec_interval`,`url` FROM `backup` %s" % sql)
    list_data = cursor.fetchall()
    conn.close()
    item_str = ''
    for items in list_data:
        item_str += '%s#%s\n' % (items[0], '//' + request.get_host() + items[1])
    save_path = r'%s/task' % (STATIC_ROOT)
    mkdir(save_path)
    targetFile = r'%s/task/backup.txt' % (STATIC_ROOT)
    if os.path.exists(targetFile): 
        os.remove(targetFile)    
    fileHandle = open (r'%s/task/backup.txt' % (STATIC_ROOT), 'w')
    fileHandle.write(item_str.encode('utf-8'))
    fileHandle.close()
    return HttpResponse(1)
