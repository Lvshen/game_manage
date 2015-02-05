#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from GameManage.models.log import Log, LogDefine, ValueDefine, FieldDefine
from django.http import HttpResponseRedirect, HttpResponse
from GameManage.models.log import Query
from GameManage.views import log
from GameManage.views.base import UserStateManager, filter_inject_sql, filter_sql, getConn, md5
from GameManage.views.log.exprot_file import QueryExprot
from django.db import connections
from GameManage.cache.memcached_util import MemcachedUtil, clear_cache, CACHE_TYPE
from GameManage.cache import log_cache, center_cache
from GameManage.views.log import the_log_in_center
import datetime, re

'''
查询相关 ，重要
'''
def query_view(request, query_id=0):
    query_id = int(query_id)
    
    if 0 == query_id:
        query_id = int(request.GET.get('id', request.POST.get('id', 0)))
    
    s_list = request.POST.getlist('s')
    if 0 == s_list.__len__():
        s_list = request.GET.getlist('s')
    
    page_num = int(request.GET.get('page_num', '1'))
    sdate = request.GET.get('sdate', '')
    edate = request.GET.get('edate', '')
    query_channel = request.GET.getlist('channel_id')
    group_id = int(request.GET.get('group_id', '0'))
    ajax = request.GET.get('ajax', False)
    exprot = int(request.GET.get('exprot', '0'))
    close_export = int(request.GET.get('close_export', '0'))
    clear_export_old_file = int(request.GET.get('clear_export_old_file', '0'))
    is_post_back = request.GET.get('post_back', False)
    exprot_file_key = request.GET.get('exprot_file_key', '')
    exprot_file_key = exprot_file_key.strip()
    more_serv_exprot = False
    if exprot_file_key != '':
        more_serv_exprot = True
    begin_exec_time = datetime.datetime.now()
    page_size = 50
    mc = MemcachedUtil()
    if exprot > 0:
        page_size = 500
    
    list_group = []
    usm = UserStateManager(request)
    the_user = usm.get_the_user() 
    if query_id > 0:
        the_query = log_cache.get_query(query_id, mc)
        
    log_define = log_cache.get_logDefine(the_query.log_type, mc)
     
    #是否在中央服务器的查询
    is_centerQuery = False
    
    if log.the_log_in_center(log_define):  #check_user
        is_centerQuery = True
        is_select_server = False 
    else:
        is_centerQuery = False
        is_select_server = True
    
    has_sql = False
    if the_query.sql != '':
        has_sql = True
    
    if not has_sql or -1 != the_query.sql.find('{{server_id}}'):
        is_select_server = True
    
    
    list_query = log_cache.get_query_list_by_logType(the_query.log_type, mc)
    if is_select_server:
        list_group = center_cache.get_group_list()
    
    if group_id != 0 and usm.current_userRole_is_root():
        list_server = center_cache.get_server_list(group_id, mc)
    else:
        if usm.current_userRole_is_root(): 
            list_server = center_cache.get_server_list(mc_util = mc)
        else:
            list_server = center_cache.get_user_server_list(the_user)
     
    #取出字段定义
    list_field = log_cache.get_fielddef_list_by_logType(the_query.log_type, mc)
    
    server_id = int(request.GET.get('server_id', '0'))
    if is_centerQuery and s_list.__len__() == 0:  
        s_list = [str(item.id) for item in list_server]
        if not usm.current_userRole_is_root() and s_list.__len__() == 0:
            return HttpResponse(u"非法操作")
    elif server_id == 0 and len(list_server) > 0:
        server_id = list_server[0].id
        if server_id == 0:
            return HttpResponse(u"非法操作")
    
    
    if usm.current_userRole_is_root():
        list_channel = center_cache.get_channel_list(mc)
    else:
        list_channel = center_cache.get_user_channel_list(the_user, mc)
    
    #是否在页面上显示查询channel
    allowChannel = False 
    
    if query_channel.__len__() == 0 and not usm.current_userRole_is_root():
        query_channel = []
        for item in list_channel:
            query_channel.append(str(item.id))
    
    if (not has_sql and list_channel.__len__() > 0) or  (-1 != the_query.sql.find('{{qchannel')):
        allowChannel = True
    
    for item1 in list_channel:
        if query_channel.__len__() > 0:
            if str(item1.id) in query_channel:
                item1.is_show = 1 
        else:
            item1.is_show = 0
    
    field_value = request.GET.get('field_value', '')
    field_value = filter_inject_sql(field_value)
    field_id = int(request.GET.get('field_id', '0'))
    
    if has_sql:
        field_value = request.GET.getlist('field_value')
    
    err_msg = ''
     
    pager_str = 'limit %s,%s' % ((page_num - 1) * page_size, page_size)
    
    fields = the_query.select.split(',')

    query_date = ''
    
    now = datetime.datetime.now()

    if not is_post_back:#如果第一次进入该页面默认时间范围是昨天数据
        if sdate == '':
            sdate = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
        
        if edate == '':
            edate = now.strftime('%Y-%m-%d 00:00:00')

    if not has_sql or the_query.sql.find('{{keyword}}') != -1:
        is_search = True
    else:
        is_search = False
    
    has_sdate = True
    has_edate = True
    
    if the_query.sql != '':
        if -1 == the_query.sql.find('{{sdate}}'):
            has_sdate = False
         
        if -1 == the_query.sql.find('{{edate}}'):
            has_edate = False 
            
        if -1 != the_query.sql.find('{{qdate}}'):
            has_sdate = True
            has_edate = True
            
        if -1 == the_query.sql.find('{{qchannel'): 
            allowChannel = False
    
    keywords = []
    lost_param = False
    if has_sql:
        sql = the_query.sql
        r_keyword_name = '(@keywords.+)'
        keyword_name_ary = re.findall(r_keyword_name, sql, re.I)
        
        if keyword_name_ary.__len__() != 0:
            keyword_name = keyword_name_ary[0]
            names_str = keyword_name.split(':')[1]
            names = names_str.split(',')
            for i in range(names.__len__()):
                name = names[i]
                value = ''
                if field_value.__len__() > i:
                    value = field_value[i]
                keywords.append({"name":name, "value":value})
            the_query.sql = re.sub(keyword_name, '', sql, re.I)
        else:
            k_len = the_query.sql.lower().count('{{keyword}}')
            for i in range(k_len):
                value = ''
                if field_value.__len__() > i:
                    value = field_value[i]
                if value == '':
                    lost_param = True
                keywords.append({"name":'输入框%s'%i, "value":value})
            
    #print keywords.__len__()
    list_data = []
    total_record = 0
    parg = {}
    parg['keywords'] = keywords
    parg['has_sql'] = has_sql
    parg['is_centerQuery'] = is_centerQuery
    parg['has_sdate'] = has_sdate
    parg['has_edate'] = has_edate
    parg["allowChannel"] = allowChannel
    parg["the_query"] = the_query
    parg["usm"] = usm
    parg["list_query"] = list_query
    parg["is_select_server"] = is_select_server
    parg["list_group"] = list_group
    parg["list_server"] = list_server
    parg["list_channel"] = list_channel
    parg["s_list"] = s_list
    parg["server_id"] = server_id
    parg["query_id"] = query_id
    parg["is_search"] = is_search
    parg["group_id"] = group_id
    parg["field_id"] = field_id
    parg["field_value"] = field_value
    parg["list_field"] = list_field
    parg["sdate"] = sdate
    parg["edate"] = edate
    parg["fields"] = fields
    
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    
    if not is_post_back and not ajax: #如果没有点击查询按钮并不是ajax提交则不查询数据（第一次进入页面不查询数据）    ——zhenwei  2012-10-22
        return render_to_response('log/query_view.html', parg)
    
    if is_select_server and not is_centerQuery:
        if server_id > 0:
            try: 
                conn = getConn(server_id)
            except:
                err_msg = '数据库链接出错!'
    else:
        conn = connections['read']
        
    if err_msg != '':
        return render_to_response('feedback.html', locals())  
    
    try:
        if sdate != '':
            sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            query_date = ' a.log_time>=\'%s\'' % sdate
        if edate != '':
            if query_date != '':
                query_date += ' and '
            edate = datetime.datetime.strptime(edate, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            query_date += ' a.log_time<=\'%s\'' % edate
    except:
        sdate = ''
        edate = ''
    
    
    #是否有channel 查询条件
    channel_condition = query_channel.__len__() > 0
    query_key = ''
    if not has_sql:
        
        query_field = the_query.select
        query_where = the_query.where
        query_order = the_query.order
        query_group = the_query.group
     
        field_name = ''
        for field_item in list_field:
            query_field = query_field.replace(field_item.name, field_item.field_name);
            query_where = query_where.replace(field_item.name, field_item.field_name);
            query_order = query_order.replace(field_item.name, field_item.field_name);
            query_group = query_group.replace(field_item.name, field_item.field_name);
            if field_id == field_item.id:
                field_name = field_item.field_name
        
        
        #处理字段值查询
        if field_name != '':
            the_values = ValueDefine.objects.filter(field_id=field_id, value=field_value)
            if len(the_values) > 0:
                field_value = the_values[0].value_id 
            if query_where != '':
                query_where += ' and '
            query_where += u'a.%s=\'%s\'' % (field_name, field_value)

        if query_date != '':
            if query_where != '':
                query_where += ' and '
            query_where += query_date
        
        if channel_condition:
            if query_where != '':
                query_where += ' and '
            query_where += 'a.log_channel in(%s)' % (','.join(query_channel))
          
        
        if query_where != '':
            query_where = 'where %s' % query_where
            
        
        if query_order != '':
            query_order = ' order by a.%s' % query_order

            if the_query.order_type == 1:
                query_order += ' desc'

        
        count_sql = 'select count(0) from log_%s a %s' % (log_define.key, query_where)

        query_sql = 'select %s from log_%s a %s %s %s' % (query_field, log_define.key, query_where, query_order, pager_str)
        
        query_key = md5('%s_%s'% (query_sql, server_id))
        if exprot_file_key == '':
            exprot_file_key = md5('%s_%s'% (query_sql, server_id))
        #print(query_sql)
    else:
            
        query_sql = the_query.sql.replace('\r\n\t', ' ').replace('\r\n', ' ')
        
        if is_centerQuery and s_list.__len__() > 0:
            server_list_str = ' IN (%s) ' % (','.join(s_list))
            query_sql = re.sub('=[\s]*{{server_id}}', server_list_str, query_sql)
        elif server_id > 0:
            query_sql = query_sql.replace('{{server_id}}', str(server_id))
        
        if query_date != '' :
            query_sql = query_sql.replace("{{qdate}}", query_date)
            query_sql = query_sql.replace('{{sdate}}', '%s' % sdate).replace('{{edate}}', '%s' % edate)#支持自定对非log表的日期支持   -zhenwei 2012-10-25
        else :
            query_sql = query_sql.replace('and {{qdate}}', '').replace('where {{qdate}}', '')
            query_sql = query_sql.replace('\'{{sdate}}\'', 'DATE(\'2001-01-01\')').replace('\'{{edate}}\'', 'NOW()')#支持自定对非log表的日期支持   -zhenwei 2012-10-25
        
        if lost_param:
            err_msg = '请输入查询条件'
            return render_to_response('feedback.html', {"err_msg":err_msg})
#        if field_value != '':
#            query_sql = query_sql.replace("{{keyword}}", field_value)
#        else:
#            if -1 != query_sql.find('{{keyword}}'):
#                err_msg = '请输入查询条件'
#                return render_to_response('feedback.html', {"err_msg":err_msg})
         
        if channel_condition: 
            query_sql = query_sql.replace('{{qchannel}}', 'log_channel in(%s)' % (','.join(query_channel))) 
        else:
            query_sql = query_sql.replace('and {{qchannel}}', '').replace('where {{qchannel}}', '')
        
        if channel_condition:
            query_sql = query_sql.replace('{{qchannela}}', 'a.log_channel in(%s)' % (','.join(query_channel)))
        else:
            query_sql = query_sql.replace('and {{qchannela}}', '').replace('where {{qchannela}}', '')
            
        if channel_condition:
            query_sql = query_sql.replace('{{qchannelb}}', 'b.log_channel in(%s)' % (','.join(query_channel)))
        else:
            query_sql = query_sql.replace('and {{qchannelb}}', '').replace('where {{qchannelb}}', '')
            
        if channel_condition:
            query_sql = query_sql.replace('{{qchannelid}}', 'channel_id in (%s)' % (','.join(query_channel)))
        
        
        query_sql = filter_keyword(query_sql, field_value)
        
        count_sql = 'select count(0) from (%s) newTable' % query_sql
        
        if exprot_file_key == '':
            exprot_file_key = md5('%s_%s'% (query_sql, server_id))
        
        if query_sql.find('limit') == -1:
            query_sql = '%s %s' % (query_sql, pager_str)
        
        query_key = md5('%s_%s'% (query_sql, server_id))
    
    parg['has_sdate'] = has_sdate
    parg['has_edate'] = has_edate
     
    print count_sql
    print query_sql 
    #raise Exception, count_sql
    #desc = cursor.description 
    cursor = conn.cursor()
    # update log_create_role
    channelKey_id_dic = {}
    
    query_memcache = mc
    if the_query.cache_validate != None and 0 != the_query.cache_validate:
        query_memcache = MemcachedUtil(valid_date = the_query.cache_validate)
    
    for item1 in list_channel:
        channelKey_id_dic[item1.key] = int(item1.id)
    try:
        count_query_key = md5('%s_%s'% (count_sql, server_id))
        total_record = log_cache.get_query_count(count_sql, count_query_key, cursor, query_memcache)
    except Exception, e:
        raise Exception, e
        print('query_view error:', e)
        return render_to_response('feedback.html', {"err_msg":"查询数据时出错"}) 
    
    
    total_page = total_record / page_size
    if total_record % page_size != 0:
        total_page += 1
    
    list_data = []
    if total_record > 0:
        query_sql = filter_sql(query_sql)
        
        list_data = log_cache.get_query_data(query_key, cursor, query_sql, query_memcache)
        
        list_data = log_cache.get_query_display_data(query_key, query_memcache, lambda args: query_display_process(args[0], args[1], args[2], args[3]), the_query, list_data, fields, list_field) 
        
    #cursor.close()
    end_exec_time = datetime.datetime.now()
    
    parg["list_data"] = list_data
    parg["err_msg"] = err_msg
    
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    parg["exec_time"] = (end_exec_time - begin_exec_time).microseconds / 1000
    
    
    #处理 导出文件
    if 0< exprot: 
        query_exprot = QueryExprot()
        file_name = query_exprot.get_gene_file_name(query_id, exprot_file_key)
        #print 'file_name::::::::::::::::::::::::::::::::', file_name
        #session ID 
        session_id = request.COOKIES.get('sessionid')
        return query_exprot.gene_file(list_data, fields, file_name, page_num, page_size, total_record, exprot, close_export, clear_export_old_file, session_id, exprot_file_key, more_serv_exprot)
    
    if ajax:
        return render_to_response('log/query_view_block.html', parg)
    
    
    return render_to_response('log/query_view.html', parg)

def filter_keyword(sql, input_data):
    
    s = sql
    d = input_data
    r = "((\w+|\w+\.\w+)\s?(=|!=|>=|<=)\s?'?{{keyword}}'?)"
    print r
    result = re.findall(r,s,re.I)
    d_len = d.__len__()
    for i in range(len(result)):
        item = result[i][0]
        print(item)
        if  d_len - 1 < i:
            s = s.replace(item,'')
        elif d[i]=='':
            s = s.replace(item,'')
        else:
            s = s.replace(item,item.replace('{{keyword}}',d[i]))
    
    print('^',s,'$')
    r2 = '((where|and|or)\s+){2,}'
    
    result_count = len(re.findall(r2,s,re.I))
    print(result_count)
    for i in range(result_count):
        result = re.search(r2,s,re.I)
        if result:
            item = result.group()
            print ':', item
            s = s.replace(item,item.split(' ')[0] + " ")
        print('^',s,'$')
        
        
    r2 = '((where|order|group)\s+){2,}'
    
    result_count = len(re.findall(r2,s,re.I))
    print(result_count)
    for i in range(result_count):
        result = re.search(r2,s,re.I)
        if result:
            item = result.group()
            tmp = item.split(' ')
            field = ''
            for k in range(tmp.__len__()):
                if k == 0:
                    continue
                if '' != tmp[k]:
                    field = tmp[k]
                    break
                
            s = s.replace(item,field + " ")
        print('^',s,'$')
        
    #-----------------
    
    r2 = '(((where|and|or)\s+)+)$'
    
    result = re.findall(r2,s,re.I)
    print('result2',result)
    #s = re.sub(r2, '', s, re.I)
    
    reobj = re.compile(r2,re.I)
    s = reobj.sub('',s)
    
    r2 = '(((where|and|or)\s+)+)\)'
    reobj = re.compile(r2,re.I)
    s = reobj.sub(')',s)
    
    return s
    

def query_display_process(the_query, list_data, fields, list_field): 
    #处理值定义
    def_value = get_def_value(the_query, list_field)
    
    field_def_list = FieldDefine.objects.all().filter(log_type=the_query.log_type) 
    list_data = list(list_data)
    for a in range(len(list_data)):
        b = 0
        item = list(list_data[a])
        if item[b] == None:
            list_data[a] = None
            continue
        for field in fields:
            item[b] = display_format(field_def_list, field, item[b], def_value)
            b += 1
        list_data[a] = item
    return list_data

def get_def_value(the_query, list_field):
    def_values = {}
    for field_item in list_field:
        if the_query.select.find(field_item.name) != -1:
            values = ValueDefine.objects.filter(field_id=field_item.id)
            item_values = {}
            for item in values:
                item_values[item.value_id] = item.value
            def_values[field_item.name] = item_values
    return def_values

def display_format(field_def_list, field, value, def_values): 
    is_format = False
    for field_def in field_def_list:
        if field_def.name == field:
            is_format = True
            value = log.format_value(field_def, value)
    
    if not is_format:
        if field.find(u'时间') != -1:
            try:
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            except:
                value = float(value)
                value = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
                
        elif field.find(u'日期') != -1:
            value = value.strftime('%Y-%m-%d')
        elif field.find(u'小时') != -1:
            value = value.strftime('%Y-%m-%d %H')
            
    if def_values.get(field, None) != None and def_values.get(field, {}) != {} and value != '':
        try:
            value = def_values[field].get(int(value), value)
        except:
            pass
            #raise Exception, u'字段值定义错误'
             
    return value

def query_list(request, log_type=0):
    list_model = []
    log_type = int(log_type)
    if log_type == 0:
        log_type = int(request.GET.get('log_type', '0'))
    
    list_log = LogDefine.objects.using('read').all() 
    if log_type > 0:
        list_model = Query.objects.using('read').filter(log_type=log_type).order_by("id")
    else:
        list_model = Query.objects.using('read').all().order_by("id")
    
    logDefine_list = LogDefine.objects.using('read').all()
    logDefineIdName = {}
    for logDefineItem in logDefine_list:
        logDefineIdName[logDefineItem.id] = logDefineItem.key
      
    for item in list_model:
        item.log_typeName = logDefineIdName[item.log_type]
        
    pargs = {}
    pargs["log_type"] = log_type
    pargs["logDefine_list"] = logDefine_list
    pargs["list_log"] = list_log
    pargs["list_model"] = list_model
    
    return render_to_response('log/query_list.html', pargs)

def query_edit(request, query_id=0, log_type=0):
    query_id = int(query_id)
    log_type = int(log_type)
    
    if query_id == 0:
        query_id = int(request.GET.get('query_id', '0'))
        
    if log_type == 0:
        log_type = int(request.GET.get('log_type', '0'))
    
    if query_id > 0 :
        model = Query.objects.using('read').get(id=query_id)
        if model.cache_validate == None:
            model.cache_validate = 0
    else :
        model = Query()
        model.id = query_id
        model.name = ''
        model.cache_validate = 0
    model.log_type = log_type
    logs = LogDefine.objects.using('read').all()
    
    list_field = FieldDefine.objects.using('read').filter(log_type=log_type)
    
    pargs = {}
    pargs["query_id"] = query_id
    pargs["log_type"] = log_type
    pargs["model"] = model
    pargs["logs"] = logs
    pargs["list_field"] = list_field
    
    return render_to_response('log/query_edit.html', pargs)

def query_save(request, query_id=0):
    query_id = int(query_id)
    
    if query_id == 0:
        query_id = int(request.GET.get('query_id', '0'))
        
    if query_id > 0 :
        model = Query.objects.get(id=query_id)
    else :
        model = Query()
    
    model.log_type = int(request.POST.get('log_type', '0'))
    model.select = request.POST.get('select', '')
    model.name = request.POST.get('name', '')
    model.where = request.POST.get('where', '')
    model.group = request.POST.get('group', '')
    model.order = request.POST.get('order', '')
    model.cache_validate = int(request.POST.get('cache_valid', 0))
    model.order_type = int(request.POST.get('order_type', '0'))
    model.sql = request.POST.get('sql', '')
    try:
        log_define = LogDefine.objects.get(id=model.log_type)
        if the_log_in_center(log_define):  #check_user
            is_select_server = False
        else:
            is_select_server = True
        
#        if model.sql!='' and model.sql.find("{{qchannel}}")==-1:
#            err_msg = 'sql没有渠道选择!需要有{{qchannel}}标记!'
#            return render_to_response('feedback.html',locals())
        
        model.save(using='write')
        return HttpResponseRedirect('/query/list')
    except Exception, e:
        print('statistic save error:', e)
    
    pargs = {}
    pargs["query_id"] = query_id
    pargs["model"] = model
    pargs["log_define"] = log_define
    pargs["is_select_server"] = is_select_server
    
    return render_to_response('log/query_edit.html', locals())


def query_clear_cache(request):
    clear_cache(CACHE_TYPE.LOG_CACHE)
    return render_to_response('feedback.html')

def query_remove(request, query_id=0):
    model_id = int(query_id)
    
    if model_id == 0:
        model_id = int(request.GET.get('query_id', '0'))
    
    if model_id > 0 :
        model = Query.objects.get(id=model_id)

        model.delete(using='write')
    return render_to_response('feedback.html')
