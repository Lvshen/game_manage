#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from GameManage.models.center import User, Player, Server, Channel
from GameManage.models.log import Log, LogDefine, ValueDefine, FieldDefine
from GameManage.views.log import field_types, the_log_in_center
from GameManage.log_cfg import ENUM_LOG_STATUS
from GameManage.views.base import getConn, UserStateManager, get_server_list, GlobalPathCfg
from django.http import HttpResponseRedirect, HttpResponse
from django.core.management.color import no_style
from django.db import connection, connections
from GameManage.statistic_module import StatisticModule 
import json, MySQLdb
from GameManage.cache import center_cache

def log_list(request):
    
    #server_list = Server.objects.using('read').all()
    
    list_record = LogDefine.objects.using('read').all()
    
    parg = {}
    parg["list_record"] = list_record
    
    return render_to_response('log/log_list.html', parg)

def log_edit(request, log_id=0):
    log_id = int(log_id)
    if 0 == log_id:
        log_id = int(request.GET.get('id', request.POST.get('id', 0)))
    if log_id > 0 :
        log_def = LogDefine.objects.using('read').get(id=log_id)
    else:
        log_def = LogDefine()
        log_def.id = log_id
    return render_to_response('log/log_edit.html', {'model':log_def})
    

def log_save(request, log_id=0):
    new_key = request.POST.get('key', '')
    save_center = int(request.POST.get('save_center', '0'))
    
    is_ajax = request.POST.get('ajax', False)
    log_id = int(log_id)
    if 0 == log_id:
        log_id = int(request.GET.get('id', request.POST.get('id', 0)))
    log_def = None
    err_msg = ''
#    sql = ''
    if log_id > 0 :
        log_def = LogDefine.objects.get(id=log_id)

    if log_def :
        if log_def.key != new_key:
#            sql = 'ALTER TABLE log_%s RENAME log_%s'%(log_def.key,new_key)
            log_def.key = new_key
    else:
        log_def = LogDefine()
        log_def.key = new_key
#        sql = 'CREATE TABLE log_%s LIKE log_0'%log_def.key

    log_def.name = request.POST.get('name', '')
    log_def.remark = request.POST.get('remark', '')
    
    status = ENUM_LOG_STATUS.NORMAL
    if 1 == save_center:
        status = ENUM_LOG_STATUS.SAVE_CENTER
    
    log_def.status = status
    
    if log_def.name != '' and log_def.remark != '':
        log_def.save(using='write')
#        if sql!='':
#            cursor = connection.cursor()
#            cursor.execute(sql)
#            #cursor.close()    
        HttpResponseRedirect("/log/list")
    else:
        err_msg = '所有数据不能为空!'
    
    if is_ajax:
        if err_msg == '':
            return HttpResponse('完成')
        return HttpResponse(err_msg)
    return render_to_response('log/log_edit.html', {'model':log_def})

def log_set(reuqest, log_id=0, log_status=0):
    if log_id > 0 :
        log_def = LogDefine.objects.get(id=log_id)
    if log_def :
        log_def.status = log_status
        log_def.save(using='write')
        
    return render_to_response('feedback.html')

def log_server(request, log_id=0):
    if log_id > 0 :
        log_def = LogDefine.objects.get(id=log_id)
    
    list_server = get_server_list()
    
    parg = {}
    parg["list_server"] = list_server
    parg["log_def"] = log_def
    
    return render_to_response('log/log_server.html', parg)

def log_remove(request, log_type=0):
    if log_type > 0 :
        log_def = LogDefine.objects.get(id=log_type)
    else:
        log_def = LogDefine()

    log_def.delete(using='write')
    
    return render_to_response('feedback.html')

def log_clear(request, server_id=0, log_type=0, clear_type=0):
    server_id = int(server_id)
    log_type = int(log_type)
    clear_type = int(clear_type)
    err_msg = ''
    if log_type > 0 :
        log_def = LogDefine.objects.get(id=log_type)
        try:
            if server_id > 0:
                try:
                    conn = getConn(server_id)
                except:
                    err_msg = '数据库链接出错!'
            else:
                conn = connection
            if clear_type == 0:
                sql = 'delete from log_%s' % log_def.key
            else:
                sql = 'drop table log_%s' % log_def.key
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
        except Exception, e:
            print('clear data error:%s' % e)
    
    parg = {}
    parg["err_msg"] = err_msg
    
    return render_to_response('feedback.html', parg)


def log_syncdb(request, server_id=0):
    err_msg = ''
    server_id = int(server_id)
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))
    
    if server_id > 0:
        try:
            the_server = Server.objects.using('read').get(id=server_id)
            the_db_config = json.loads(the_server.log_db_config)
                
            conn = MySQLdb.connect(host=the_db_config['host'], user=the_db_config['user'], passwd=the_db_config['password'], port=the_db_config.get('port',3306), charset='utf8')
            conn.autocommit(1)    
        except Exception, ex:
            err_msg = '数据库链接出错! %s' % ex
    else:
        conn = connection
    
    is_ajax = request.GET.get('ajax', '')
    if is_ajax == '1':
        is_ajax = True
        
        
    if err_msg != '':
        if is_ajax:
            render = HttpResponse('{"code":1, "msg":"%s"}' % err_msg)
        else:
            render = render_to_response('feedback.html', locals()) 
        return render
    
    cursor = conn.cursor()
    if server_id > 0:
        try:
            sql = 'CREATE DATABASE IF NOT EXISTS %s default charset utf8 COLLATE utf8_unicode_ci;' % the_db_config['db']
            cursor.execute(sql)
        except Exception, e:
            print('create datebase has error', e)
        conn.select_db(the_db_config['db']);
        try:
            Log._meta.db_table = 'log_0'
            sql, _ = connection.creation.sql_create_model(Log, no_style())
            sql = sql[0].replace('CREATE TABLE', 'CREATE TABLE if not exists')
    #        print(sql)
            cursor.execute(sql)
        except Exception, e:
            print('create table log_0 has error', e)

    try:
        sql = 'show tables'
        
        cursor.execute(sql)
        list_record = cursor.fetchall()
        tables = []
        for item in list_record:
            tables.append(item[0])
            
        if server_id > 0 :
            log_def_list = LogDefine.objects.filter(status=ENUM_LOG_STATUS.NORMAL)
        else:
            log_def_list = LogDefine.objects.filter(status=ENUM_LOG_STATUS.SAVE_CENTER)
            
        for log_def in log_def_list:
            if tables.count('log_%s' % log_def.key) == 0:
                sql = 'CREATE TABLE log_%s LIKE log_0' % log_def.key
                cursor.execute(sql)
  
    except Exception, e:
        print('create table log_x has error', e)
#    if True: 
    try:
        Log._meta.db_table = 'player_%s' % server_id
        sql, _ = connection.creation.sql_create_model(Player, no_style())
        sql = sql[0].replace('CREATE TABLE', 'CREATE TABLE if not exists').replace('player_0', 'player_%s' % server_id)
#        print(sql)
        cursor.execute(sql)
    except Exception, e:
        print('create table player has error', e)
        
    try:
        sql_indexes = connection.creation.sql_indexes_for_model(Player, no_style())
        for sql in sql_indexes:
            sql = sql.replace('player_0', 'player_%s' % server_id)
            try:
                print(sql)
                cursor.execute(sql)
            except Exception, e:
                print('create index player_x has error', e)
    except Exception, e:
        print('create index player has error', e)
        
    cursor.close()
    
    parg = {}
    parg["err_msg"] = err_msg 
    
    if is_ajax:
        render = HttpResponse('{"code":0}')
    else:
        render = render_to_response('feedback.html', parg)
    return render

def sync_log_index(request, server_id=0):
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))
    
    log_list = []
    server_list = []
    if server_id == 0:
        log_list = LogDefine.objects.filter(status = ENUM_LOG_STATUS.SAVE_CENTER)
    else:
        server_list = center_cache.get_server_list()
        log_list = LogDefine.objects.filter(status = ENUM_LOG_STATUS.NORMAL)
        
    return render_to_response('log/sync_log_index.html', {"server_id": server_id, "log_list": log_list, "server_list":server_list})

def do_log_sync_index(request, server_id=0, log_id=0):
    server_id = int(server_id)
    log_id = int(log_id)
    if server_id == 0:
        server_id = int(request.GET.get('server_id', '0'))
    
    get_sql = int(request.GET.get('get_sql', request.POST.get('get_sql', 0)))
    save_path = ''
    if 1 == get_sql:
        sql_file_name = 'create_index_sql_%s.sql' % server_id
        gpc = GlobalPathCfg()
        save_path = gpc.get_create_index_save_path(sql_file_name)
    
    if log_id == 0:
        log_id = int(request.GET.get('log_id', '0'))
    
    error = "{code:1}"
    if log_id == 0:
        return HttpResponse(error)
    
    if 0 == LogDefine.objects.all().filter(id=log_id).count():
        return HttpResponse(error)
    
    conn = None
    if 0 == server_id:
        conn = connections['write']
    else:
        conn = getConn(server_id)
    model = LogDefine.objects.get(id=log_id)
    table_name = 'log_%s' % model.key
    index_list = get_table_index(conn, table_name)
    need_index_list = get_create_index_field_list(model.id)
    for field_def in need_index_list:
        has_index = False
        column_name = field_def[0]
        new_index_name = "index_%s_%s" % (table_name, column_name)
        for index in index_list:
            index_column_name = index[4] 
            index_name = index[2]
            
            if pass_index_name(index_name):
                continue;
            
            if index_column_name == column_name: 
                #索引名字不一样删除索引
                has_index = True
                if  new_index_name != index_name:
                    delete_index(conn, index_name, table_name, save_path)
                    has_index = False
        
        if not has_index:
            create_index(conn, new_index_name, table_name, column_name, save_path)
    
    return HttpResponse("{code:0}")

#过滤的索引名称
def pass_index_name(index_name):
    if index_name == 'PRIMARY':
        return True
            
def create_index(conn, index_name, table_name, column_name, save_path):
    sql_tmp = "CREATE INDEX %s ON %s (%s)"
    sql = sql_tmp % (index_name, table_name, column_name)
    if '' == save_path:
        cursor = conn.cursor()
        cursor.execute(sql)
    else:
        file_handler = open(save_path, "a")
        file_handler.write(sql + ';')
        file_handler.close()

def delete_index(conn, index_name, table_name, save_path):
    sql = "DROP INDEX %s ON %s" % (index_name, table_name)
    
    if '' == save_path:
        cursor = conn.cursor()
        cursor.execute(sql)
    else:
        file_handler = open(save_path, "a")
        file_handler.write(sql + ';')
        file_handler.close()

def get_create_index_field_list(log_def_id):
    conn = connections['read']
    sql = 'SELECT field_name FROM def_field WHERE log_type = %s AND create_index = 1 ' % log_def_id 
    cursor = conn.cursor()
    data_list = []
    try:
        cursor.execute(sql)
        data_list = cursor.fetchall()
    except:
        return data_list
    finally:
        conn.close()
    return data_list

def get_table_index(conn, table_name):
    sql = " SHOW INDEX FROM %s " % table_name 
    cursor = conn.cursor()
    list_data = []
    try:
        cursor.execute(sql)
        list_data = cursor.fetchall()
    except:
        return list_data
    return list_data

def log_syncdb_data(request, server_id=0):
    err_msg = ''
    
    server_id = int(server_id)
    if 0 == server_id:
        server_id = int(request.GET.get('server_id', 0))
    
    if 0 == server_id:
        server_id = int(request.POST.get('server_id', 0))
    
    if server_id > 0:
        try:
            conn = getConn(server_id)
        except:
            err_msg = '数据库链接出错!'
    else:
        conn = connection
        
    if err_msg != '':
        parg = {}
        parg["err_msg"] = err_msg
        return render_to_response('feedback.html', parg)
    cursor = conn.cursor()
    is_reload = True
    page_size = 50
    try:
        #sql = 'select id,log_result from log_create_role where log_channel=0 limit %d'%page_size
        sql = 'select id,log_result from log_create_role where log_channel=0 and log_result>0 limit %d' % page_size
        print(sql)
        cursor.execute(sql)
        list_record = cursor.fetchall()
        if len(list_record) < 10:
            is_reload = False
        for item in list_record:
            the_user = User.objects.get(id=item[1])
            if the_user.channel_key != '':
                the_channel = Channel.objects.get(key=the_user.channel_key)
                sql = 'update log_create_role set log_channel=%d where id=%d' % (the_channel.id, int(item[0]))
                print(sql)
                cursor.execute(sql)
    except Exception, e:
        print('syncdb data has error', e)

    #cursor.close()  
    
    page_num = int(request.GET.get('page_num', '0'))
    sync_num = page_num * page_size
    page_num += 1
    
    parg = {}
    parg["server_id"] = server_id
    parg["is_reload"] = is_reload
    parg["sync_num"] = sync_num
    parg["page_num"] = page_num
    
    return render_to_response('log/log_sync_data.html', parg)


def log_syncdb_player(request, server_id=0):
    from pymongo import Connection
    server_id = int(server_id)
    err_msg= ''
    if server_id == 0:
        err_msg = '参数错误!'
        return render_to_response('log/log_sync_player.html', locals())
    try: 
        the_server = Server.objects.get(id=server_id)
        the_db_config = json.loads(the_server.log_db_config)
        conn = MySQLdb.connect(host=the_db_config['host'], user=the_db_config['user'], passwd=the_db_config['password'], db=the_db_config['db'], charset='utf8')
        conn.autocommit(1)
        cursor = conn.cursor()
    except:
        err_msg = 'mysql数据库链接出错!'
        return render_to_response('log/log_sync_player.html', locals())
    if True:
#    try:
        mg_conn = Connection(the_db_config['host'], the_db_config.get('mongo_port', 27017))
        mg_db = mg_conn['sid%d' % server_id]
        mg_player = mg_db['sg.player']
#    except:
#        err_msg = 'mongo数据库链接出错!'
#        return render_to_response('log_sync_player.html',locals())
    
    pos = int(request.GET.get('pos', 0))
    if pos == 0:
        mg_count = mg_player.count()
        sql = 'select count(distinct log_user) from log_create_role'
        
        cursor.execute(sql)
        mysql_count = int(cursor.fetchone()[0])
            
        if mg_count <= mysql_count:
            err_msg = '数据总数量一致,无需再次同步!'
            return render_to_response('log/log_sync_player.html', locals())
    page_size = 100
    list_player = mg_player.find({"player_id":{"$gt":pos}}, {"player_id":1, "uid":1, "nn":1}).sort("player_id", 1).limit(page_size)
    begin_player = 0
    last_player = 0
    is_reload = True
    total_record = 0
    list_record = []
    for item in list_player:
        try:
            list_record.append(item)
            last_player = item['player_id']
            if begin_player == 0:
                begin_player = last_player
            total_record += 1
        except:
            print('has unkonw error')
        #print(last_player)
    pos = last_player
    if pos == 0:
        is_reload = False
    sql = 'select count(distinct log_user) from log_create_role where log_user between %d and %d' % (begin_player, last_player)
    cursor.execute(sql)
    mysql_count = int(cursor.fetchone()[0])
    #print(sql,total_record,mysql_count)
    sync_list = []
    if mysql_count != total_record:
        for item in list_record:
            sql = 'select count(0) from log_create_role where log_user=%d' % item['player_id']
            cursor.execute(sql)
            total_record = int(cursor.fetchone()[0])
            #print(sql,total_record)
            if total_record == 0:
                sync_list.append(str(item['player_id']))
                try:
                    sql = 'insert into log_create_role(log_type,log_data,log_server,log_user,log_result,log_time,f1)values(6,0,%d,%d,%d,now(),"%s")' % (server_id, item['player_id'], item['uid'], item['nn'].replace('\\', '\\\\').encode('utf-8'))
                    #print(sql)
                    cursor.execute(sql)
                except Exception, e:
                    print('has error sync role %d,%s' % (item['player_id'], e))
        sync_list = u'已同步%s' % ','.join(sync_list)
    else:
        sync_list = u'无需同步'
    conn.close()
    mg_conn.close()
    
    parg = {}
    parg["total_record"] = total_record
    parg["server_id"] = server_id
    parg["pos"] = pos
    parg["sync_list"] = sync_list
    parg["err_msg"] = err_msg
    parg["is_reload"] = is_reload
    
    return render_to_response('log/log_sync_player.html', parg)


def field_list(request, log_type=0):
    log_type = int(log_type)
    if 0 == log_type:
        log_type = int(request.GET.get('log_type', request.POST.get('log_type', 0)))
    
    log_def = LogDefine.objects.using('read').get(id=log_type)
    list_record = FieldDefine.objects.using('read').filter(log_type=log_type)
    fields = []
    values = []
    for item in list_record:
        fields.append(item.field_name)
        values.append('\'%s\'' % item.name)
    
    insert_sql = 'insert into log_%s(log_type,%s)values(%s,%s);' % (log_def.key, ','.join(fields), log_def.id, ','.join(values))
    
    parg = {}
    parg["log_type"] = log_type
    parg["list_record"] = list_record
    parg["insert_sql"] = insert_sql
    
    return render_to_response('log/field_list.html', parg)

def field_edit(request, field_id=0, log_type=0):
    field_id = int(field_id)
    if 0 == field_id:
        field_id = int(request.GET.get('id', request.POST.get('id', 0)))
    if 0 == log_type:
        log_type = int(request.GET.get('log_type', request.POST.get('log_type', 0)))
        
    if field_id > 0:
        field_def = FieldDefine.objects.get(id=field_id)
    else:
        field_def = FieldDefine()
        field_def.id = field_id
        field_def.log_type = log_type
    fields = []
    for item in Log._meta.fields:
        if item.name != 'id' and item.name != 'log_type':
            fields.append(item.name)
            
    return render_to_response('log/field_edit.html', {'model':field_def, 'fields':fields, 'field_types':field_types})

def field_save(request, field_id=0):
    field_id = int(field_id)
    if 0 == field_id:
        field_id = int(request.GET.get('id', request.POST.get('id', 0)))
    
    if field_id > 0:
        field_def = FieldDefine.objects.get(id=field_id)
    else:
        field_def = FieldDefine()
    field_def.log_type = int(request.POST.get('log_type', '0'))
    field_def.name = request.POST.get('name', '')
    field_def.field_type = request.POST.get('field_type', '')
    field_def.field_name = request.POST.get('field_name', '')
    field_def.field_format = request.POST.get('field_format', '')
    
    field_def.create_index = int(request.POST.get('create_index', '0'))
    
    err_msg = ''
    try:
        field_def.save(using='write')
        return HttpResponseRedirect('/field/list/%d' % field_def.log_type)
    except Exception, e:
        err_msg = 'field save error:%s' % e
    
    parg = {}
    parg["err_msg"] = err_msg
    
    return render_to_response('feedback.html', parg)

def field_remove(request, field_id=0):
    field_id = int(field_id)
    if 0 == field_id:
        field_id = int(request.GET.get('field_id', request.POST.get('field_id', 0)))
    
    if field_id > 0:
        field_def = FieldDefine.objects.get(id=field_id)
    else:
        field_def = FieldDefine()
    
    field_def.delete(using='write')
    
    return render_to_response('feedback.html')


def value_list(request, field_id=0):
    field_id = int(field_id)
    if 0 == field_id:
        field_id = int(request.GET.get('field_id', request.POST.get('field_id', 0)))
        
    field_def = FieldDefine.objects.using('read').get(id=field_id)
    log_type = field_def.log_type
    list_record = ValueDefine.objects.using('read').filter(field_id=field_id)
    
    parg = {}
    parg["log_type"] = log_type
    parg["field_id"] = field_id
    parg["list_record"] = list_record
    
    return render_to_response('log/value_list.html', parg)

def value_save(request, field_id=0, def_id=0):
    if 0 == field_id:
        field_id = int(request.GET.get('field_id', request.POST.get('field_id', 0)))
        
    if field_id == 0:
        HttpResponseRedirect('/')
    
    value = request.POST.get('value', '')
    if def_id > 0:
        value_def = ValueDefine.objects.get(id=def_id)
        value_def.value = value
        value_def.value_id = int(request.POST.get('value_id', 0))
        value_def.save(using='write')
    else:
        if value.find('\n') == -1:
            value_def = ValueDefine()
            value_def.field_id = field_id
            value_def.value_id = int(request.POST.get('value_id', 0))
            value_def.value = value
            value_def.save(using='write')
        else:
            values = value.replace('\r', '').split('\n')
            for value in values:
                value_def = ValueDefine()
                value_def.field_id = field_id
                value_def.value_id = value.split(',')[0]
                value_def.value = value.split(',')[1]
                value_def.save(using='write')
            

    return HttpResponse("保存成功！");

def value_remove(request, def_id=0):
    
    def_id = int(def_id)
    if 0 == def_id:
        def_id = int(request.GET.get('id', request.POST.get('id', 0)))
    if def_id > 0:
        value_def = ValueDefine.objects.get(id=def_id)
    else:
        value_def = ValueDefine()
    if value_def :
        value_def.delete(using='write')
    
    return render_to_response('feedback.html')


def update_channel(request):
    server_id = int(request.GET.get('server_id', '0'))
      
    log_def_id = int(request.GET.get('log_def_id', '0'))
    
    log_def = LogDefine.objects.get(id = log_def_id)
 
    if server_id <= 0 and not the_log_in_center(log_def): 
        return HttpResponse("选择的服务器无效")
    
    sm = StatisticModule('', False)
    
    sm.getServer(server_id, True)
    if 'open' == log_def.key:
        sm.update_open_channel()
    elif 'pay' == log_def.key:
        sm.update_pay_channel()
    else:
        sm.update_channel(log_def.id, server_id)
    
    return HttpResponse("成功")
    
#日志表结构信息
def table_info(request):
    
    usm = UserStateManager(request)
    if not usm.current_userRole_is_root():
        return HttpResponse('权限不足')
    
    log_id = int(request.GET.get('log_id', '0'))
    server_id = int(request.GET.get('server_id', '0'))
    
    if 0 == server_id:
        server_id = int(request.POST.get('server_id', '0'))
    
    log_list = []
    if 0 == server_id:
        log_list = LogDefine.objects.filter(status = ENUM_LOG_STATUS.SAVE_CENTER).all()
    else:
        log_list = LogDefine.objects.filter(status = ENUM_LOG_STATUS.NORMAL).all()
    
    server_list = get_server_list()
    
    parg = {}
    
    if 0 != log_id and -1 != server_id:
        if 0 == LogDefine.objects.filter(id = log_id).count():
            return HttpResponse('请选择日志表')
        
        log_def = None
        for item in log_list:
            if item.id == log_id:
                log_def = item
        
        if None == log_def:
            return HttpResponse('请选择日志表')
        
        query_sql = 'show index from log_%s' %  log_def.key
        conn = conn_switch(server_id)
        cursor = conn.cursor()
        cursor.execute(query_sql) 
        list_data = cursor.fetchall()
        #raise Exception, query_sql
        conn.close()
        
        parg['log_def'] = log_def
        parg['list_data'] = list_data
    
    parg['log_id'] = log_id
    parg['log_list'] = log_list
    parg['server_list'] = server_list
    parg['server_id'] = server_id
    
    return render_to_response('log/table_info.html', parg)


def del_index(request):
    
    usm = UserStateManager(request)
    if not usm.current_userRole_is_root():
        return HttpResponse('权限不足')
    
    log_key = request.GET.get('log_key', '')
    index_name = request.GET.get('index_name', '')
    
    server_id = int(request.GET.get('server_id', '-1'))
    
    if -1 == server_id:
        return HttpResponse('没有选择服务器')
    
    if log_key == '' or index_name == '':
        return HttpResponse('没有选择日志表  或  索引')
    
    if not check_table_is_log(log_key):
        return HttpResponse('非法操作，该表不是日志表')
    
    sql = 'drop index %s on log_%s;' % (index_name, log_key)
    
    conn = conn_switch(server_id)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()
    
    return table_info(request)
    
    

def check_table_is_log(log_key):
    if 0 == LogDefine.objects.filter(key = log_key).count():
        return False
    return True
    
def conn_switch(server_id):
    conn = None
    if 0 != server_id:
        conn = getConn(server_id)
    else:
        conn = connections['write']
    return conn
 
# 删除日志数据   
def log_data_delete(request, log_type):
    
    log_type = int(log_type)
    
    sdate = request.GET.get('sdate','')
    edate = request.GET.get('edate','')
    server_id = int(request.GET.get('server_id','0'))
    
    delete_date = ''
    size = 300
    msg = ''

    if server_id > 0:
        delete_server = " AND `log_server` = %d " % server_id
    else:
        msg = '服务器ID不能为空！'  
            
    if sdate != '' and edate != '':
        delete_date +=  "`log_time` >='%s' AND `log_time` <= '%s' " %(sdate, edate) 
        print delete_date
        
    else:
        msg = '时间不能为空！'     
        
    is_finish = 0
    record = 0
    if log_type > 0 and msg == '':
        print 'yes'
        log_def = LogDefine.objects.get(id=log_type)
        try:
            if server_id > 0:
                try:
                    conn = getConn(server_id)
                except:
                    msg = '数据库链接出错!'
                    print msg
            else:
                conn = connection
            cursor = conn.cursor()
            
            record_sql = "SELECT COUNT(*) FROM `log_%s` WHERE %s %s"%(log_def.key, delete_date, delete_server)
            print record_sql
            cursor.execute(record_sql)
            record = int(cursor.fetchone()[0])
            if record > 0:
                sql = 'DELETE FROM `log_%s` WHERE %s %s LIMIT %d' % (log_def.key, delete_date, delete_server,size)
                is_finish = cursor.execute(sql)
            else:
                is_finish = 0
            cursor.close()
        except Exception, e:
            print('clear data error:%s' % e)    
            msg = '%s'%e
    return HttpResponse('{"is_finish":%d,"msg":"%s","record":"%s"}'%(is_finish,msg, record))
