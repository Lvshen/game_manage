#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.cache import center_cache, memcached_util
from django.http import HttpResponse
from django.db import connections

import datetime



def check_role(request, server_id, usm):
    the_user = usm.get_the_user()
    if not usm.current_userRole_is_root():
        user_server_list = center_cache.get_user_server_list(the_user)
        if not user_server_list.__contains__(server_id):
            return False
    return True

def get_today_data(server_id, statistic, usm, base_date = None):
    if None == base_date:
        base_date =  datetime.datetime.now()
    
    begin_date = base_date.strftime('%Y-%m-%d 00:00:00')
    end_date = (base_date + datetime.timedelta(days = 1)).strftime('%Y-%m-%d 00:00:00')
    
    return get_date(server_id, statistic.id, begin_date, end_date, usm)
        
def get_yesterday_date(server_id, statistic, usm, base_date = None):
    if None == base_date:
        base_date =  datetime.datetime.now()
        
    begin_date = (base_date - datetime.timedelta(days = 1)).strftime('%Y-%m-%d 00:00:00')
    end_date = base_date.strftime('%Y-%m-%d 00:00:00')
    
    return get_date(server_id, statistic.id, begin_date, end_date, usm)

def get_week_data(server_id, statistic, usm, base_date = None):
    if None == base_date:
        base_date =  datetime.datetime.now()
        
    begin_date = (base_date - datetime.timedelta(days = 7)).strftime('%Y-%m-%d 00:00:00')
    end_date = (base_date - datetime.timedelta(days = 6)).strftime('%Y-%m-%d 00:00:00')
    
    return get_date(server_id, statistic.id, begin_date, end_date, usm)

def get_month_data(server_id, statistic, usm, base_date = None):
    if None == base_date:
        base_date =  datetime.datetime.now()
    
    begin_date = (base_date - datetime.timedelta(days = 30)).strftime('%Y-%m-%d 00:00:00')
    end_date = (base_date - datetime.timedelta(days = 29)).strftime('%Y-%m-%d 00:00:00')
    
    return get_date(server_id, statistic.id, begin_date, end_date, usm)
    
def get_date(server_id, statistic_id, begin_date, end_date, usm):
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
    
    server_conditions = ''
    if 0 != server_id:
        server_conditions = ' AND server_id=%s ' % server_id
    
    sql = "SELECT SUM(`result`) FROM `result` WHERE statistic_id=%s AND create_time BETWEEN '%s' AND '%s' AND channel_id IN (%s) %s " % (statistic_id ,begin_date, end_date, ','.join(channel_id_list), server_conditions)
    
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    if result == None:
        return 0
    
    return float(result)
    
    
