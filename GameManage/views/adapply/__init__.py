#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connections
from GameManage.models.adapply import AdConfig, AdIP, AdLog
import time, datetime
from django.db import connections
import os
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    
def _list(respond, model, search = {}, order = ['id'], page_size = 10):
    print 'http://cp.206m.tj.twsapp.com' + respond.META['PATH_INFO'] + '?' + respond.META['QUERY_STRING']
    try:
        print 'order',order
        page_num = int(respond.GET.get('page_num', '1'))
        total_record = 0
        total_page = 0
        model_list = {}
        if page_size != '':
            page_size = page_size
        else:
            page_size = int(respond.GET.get('page_size', '5'))
        if page_size not in [1,5,6,10,12,15,20,50]:
            page_size = 10
        if len(search) != 0:
            model_list = model.objects.using('adapply').filter(**search).order_by(*order)
        else:
            model_list = model.objects.using('adapply').order_by(*order)
        if model_list:
            total_record = model_list.count()
            total_page = total_record / page_size
            if total_record % page_size >= 1:
                total_page = total_page + 1
            if page_num > total_page:
                page_num = 1
                
            model_list = model_list[page_size * (page_num -1):page_size * page_num]
        
        params = {
                  "model_list"  :   model_list,
                  "page_num"    :   page_num,
                  "page_size"   :   page_size,
                  "total_record":   total_record,
                  "total_page"  :   total_page
        }
        print 'search',search
        print params
        return params
    except Exception,e:
        print 'error',e
        params = {
                  "model_list"  :   {},
                  "page_num"    :   1,
                  "page_size"   :   0,
                  "total_record":   0,
                  "total_page"  :   0
        }
        return params        

def _del(model, model_id):
    print 'del',model,model_id
    try:
        msg = ''
        model_id = int(model_id)
        if model_id:
            model.objects.using('adapply').get(id = model_id).delete()
            msg = '操作成功！'
        else:
            msg = '操作失败！'
    except Exception,e:
        print 'del error',e
        msg = '%s'%e
    params = {}
    params['err_msg'] = msg
    return render_to_response('feedback.html', params) 


def index(request):
    search = {}
    params = _list(request,AdConfig, search)
    return render_to_response('adapply/index.html', params)

'''
跳转URL:     
http://10.1.1.243:8888/service/adapply/cid/1
返回参数URL:  
http://10.1.1.243:8888/service/adapply/ip/10.1.1.243
'''

# /adapply/cid/(\d+)$
def jump_url(request, cid = 0):
    print 'jump_url'
    print 'cid',cid
    try:
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
            ip =  request.META['HTTP_X_FORWARDED_FOR']  
        else:  
            ip = request.META['REMOTE_ADDR']         
        cid = int(cid)
        the_ad_config = AdConfig.objects.using('adapply').get(id = cid)
        print 'the_ad_config',the_ad_config
        if the_ad_config:
            the_ad_config.hits = the_ad_config.hits + 1
            the_ad_config.save(using = 'adapply')
            
            if AdIP.objects.using('adapply').filter(ip = ip).count() > 0:
                the_ad_ip = AdIP.objects.using('adapply').filter(ip = ip)[0]
                the_ad_ip.channel_key = the_ad_config.channel_key
                the_ad_ip.cid = cid
                the_ad_ip.last_time = int(time.time())
                the_ad_ip.save(using = 'adapply')
            else:
                the_ad_ip = AdIP()
                the_ad_ip.channel_key = the_ad_config.channel_key
                the_ad_ip.ip = ip
                the_ad_ip.cid = cid
                the_ad_ip.save(using = 'adapply')
            return HttpResponseRedirect(the_ad_config.url)
    except Exception,e:
        print 'jump_url error',e
    return HttpResponse(404)    

# /adapply/ip/(\S+)        
def callback_url(request, ip = ''):
    try:
        if ip != '':
            ip = ip
        else:
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
                ip =  request.META['HTTP_X_FORWARDED_FOR']  
            else:  
                ip = request.META['REMOTE_ADDR']   
        print "AdIP.objects.using('adapply').filter(ip = ip).count()",AdIP.objects.using('adapply').filter(ip = ip).count()
        if AdIP.objects.using('adapply').filter(ip = ip).count() > 0:
            the_ad_ip = AdIP.objects.using('adapply').filter(ip = ip)[0]
            
            th_ad_config = AdConfig.objects.using('adapply').filter(channel_key = the_ad_ip.channel_key)[0]
            if th_ad_config.max_actives <= AdLog.objects.using('adapply').filter(channel_key = the_ad_ip.channel_key, ip = ip).count():
                return HttpResponse(0)
            else:
                the_ad_log = AdLog()
                the_ad_log.ip = ip
                the_ad_log.cid = th_ad_config.id
                the_ad_log.channel_key = the_ad_ip.channel_key
                the_ad_log.save(using = 'adapply')
                return HttpResponse('%s'%the_ad_ip.channel_key)    
    except Exception,e:
        print 'callback_url error',e   
    return HttpResponse(0)     
           
        
# 配置列表
def config(request):
    channel_key = request.GET.get('channel_key','')
    model_id = request.GET.get('id','')
    search = {}
    if channel_key != '':
        search['channel_key'] = channel_key
    if model_id != '':
        search['id'] = model_id
    params = _list(request, AdConfig, search)
    params['channel_key'] = channel_key
    params['model_id'] = model_id
    print 'params',params
    
    return render_to_response('adapply/list.html', params)

def config_edit(request, model_id = 0):
    try:
        model_id = int(model_id)
        if model_id > 0:
            model = AdConfig.objects.using('adapply').get(id = model_id)
        else:
            model = AdConfig()
            model.id = 0
        params = {
                  'model'   :   model
        }
        return render_to_response('adapply/edit.html', params)
    except Exception, e:
        print 'config_edit error',e
    
def config_save(request, model_id = 0):
    try:
        model_id = int(model_id)
        channel_key = request.POST.get('channel_key','')
        url = request.POST.get('url','')
        hits = request.POST.get('hits','')
        max_actives = request.POST.get('max_actives','')
        remark = request.POST.get('remark','')
        if channel_key != '' and url != '' and hits != '' and max_actives != '':
            if model_id > 0:
                model = AdConfig.objects.using('adapply').get(id = model_id)
            else:
                model = AdConfig()
                model.id = 0
            model.channel_key = channel_key
            model.url = url
            model.hits = hits
            model.max_actives = max_actives
            model.remark = remark
            model.save(using = 'adapply')
            return HttpResponseRedirect('/adapply/list')
        else:
            return HttpResponse('必填项不能为空！')
    except Exception, e:
        print 'config_edit error',e
        return HttpResponse(e)
 
def config_del(request, model_id = 0):   
    try:
        msg = ''
        model_id = int(model_id)
        if model_id:
            AdConfig.objects.using('adapply').get(id = model_id).delete()
            msg = '删除成功！'
        else:
            msg = '删除失败！'
    except Exception,e:
        print 'del error',e
        msg = '%s'%e
    params = {}
    params['msg'] = msg
    return render_to_response('adapply/feedback.html', params)  
        
# IP队列表
def ip(request):
    channel_key = request.GET.get('channel_key','')
    ip = request.GET.get('ip','')
    search = {}
    if channel_key != '':
        search['channel_key'] = channel_key
    if ip != '':
        search['ip'] = ip        
    params = _list(request, AdIP, search)
    params['channel_key'] = channel_key
    params['ip'] = ip
    return render_to_response('adapply/ip_list.html', params)

def ip_edit(request, model_id = 0):
    try:
        model_id = int(model_id)
        if model_id > 0:
            model = AdIP.objects.using('adapply').get(id = model_id)
        else:
            model = AdIP()
            model.id = 0
        params = {
                  'model'   :   model
        }
        return render_to_response('adapply/ip_edit.html', params)
    except Exception, e:
        print 'ip_edit error',e
        return HttpResponse(e)
    
def ip_save(request, model_id = 0):
    try:
        model_id = int(model_id)
        channel_key = request.POST.get('channel_key','')
        ip = request.POST.get('ip','')
        
        if channel_key != '' and ip != '':
            if model_id > 0:
                model = AdIP.objects.using('adapply').get(id = model_id)
            else:
                model = AdIP()
                model.id = 0
            model.channel_key = channel_key
            model.ip = ip
            model.last_time = int(time.time())
            model.save(using = 'adapply')
            return HttpResponseRedirect('/adapply/ip/list')
        else:
            return HttpResponse('必填项不能为空！')
    except Exception, e:
        print 'ip_save error',e
        return HttpResponse(e)
    
# 流水表
def log(request):
    channel_key = request.GET.get('channel_key','')
    ip = request.GET.get('ip','')
    search = {}
    if channel_key != '':
        search['channel_key'] = channel_key
    if ip != '':
        search['ip'] = ip   
    params = _list(request, AdLog, search, ['id'], 20)
    params['channel_key'] = channel_key
    params['ip'] = ip    
    return render_to_response('adapply/log_list.html', params)

def log_edit(request, model_id = 0):
    try:
        model_id = int(model_id)
        if model_id > 0:
            model = AdLog.objects.using('adapply').get(id = model_id)
        else:
            model = AdLog()
            model.id = 0
        params = {
                  'model'   :   model
        }
        return render_to_response('adapply/log_edit.html', params)
    except Exception, e:
        print 'log_edit error',e
        return HttpResponse(e)
    
def log_save(request, model_id = 0):
    try:
        model_id = int(model_id)
        channel_key = request.POST.get('channel_key','')
        ip = request.POST.get('ip','')
        if channel_key != '' and ip != '':
            if model_id > 0:
                model = AdLog.objects.using('adapply').get(id = model_id)
            else:
                model = AdLog()
                model.id = 0
            model.channel_key = channel_key
            model.ip = ip
            model.save(using = 'adapply')
            return HttpResponseRedirect('/adapply/log/list')
        else:
            return HttpResponse('必填项不能为空！')        
    except Exception, e:
        print 'log_save error',e
        return HttpResponse(e)    

def log_statistics(request):
    channel_key = request.GET.get('channel_key','')
    
    the_date = datetime.datetime.now()
    sdate = request.GET.get('sdate', the_date.strftime('%Y-%m-01 00:00:00'))
    edate = request.GET.get('edate', (the_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'))
    page_size = 20
    page_num = int(request.GET.get('page_num', '1'))
    if page_num < 1:
        page_num = 1
    spos = (page_num - 1) * page_size   
     
    date_format = '%%Y-%%m-%%d %%H:%%M:%%S'
    query_condition = " AND FROM_UNIXTIME(`create_time`,'%s') BETWEEN '%s' AND '%s'"%(date_format, sdate, edate)
    if channel_key != '':
        query_condition = ' AND `channel_key` = "%s" %s'%(channel_key, query_condition)
    query_sql = "SELECT `channel_key`,COUNT(DISTINCT `ip`) AS `total_ip`, COUNT(*) AS `total_actives` FROM `ad_log` WHERE 1 %s GROUP BY `channel_key`"%(query_condition)
    count_sql = "SELECT COUNT(*) AS `result` FROM (%s) a"%query_sql
    conn = connections['adapply']
    cursor = conn.cursor()
    cursor.execute(count_sql)
    total_record = int(cursor.fetchone()[0])
    model_list = []
    if total_record > 0:
        query_sql = "%s LIMIT %s, %s"%(query_sql, spos, page_size)
        print query_sql
        cursor.execute(query_sql)
        model_list = cursor.fetchall()
    params = {
              "model_list"  :   model_list,
              "page_num"    :   page_num,
              "page_size"   :   page_size,
              "total_record":   total_record,
              "sdate"       :   sdate,
              "edate"       :   edate,
              "channel_key" :   channel_key
    }        
    return render_to_response('adapply/log_statistics_list.html', params)
