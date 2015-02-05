# -*- coding: utf-8 -*-
from GameManage.cache.memcached_util import MemcachedUtil, get_value as cache_get_value, CACHE_TYPE, save_cache_key
from GameManage.models.log import LogDefine, FieldDefine, Query
from GameManage.log_cfg import ENUM_LOG_STATUS

def get_value(key, mc_util, get_data, *args):
    return cache_get_value(key, CACHE_TYPE.LOG_CACHE, mc_util, get_data, *args)

def get_logDefine(model_id, mc_util = None):
    key = 'LOGDEFINE_%s' % model_id
    return get_value(key, mc_util, lambda args:LogDefine.objects.get(id=args[0]), model_id)
    
    
def get_query(model_id, mc_util = None):
    key = 'QUERY_%s' % model_id
    return get_value(key, mc_util, lambda args:Query.objects.get(id=args[0]), model_id)
    
     
def get_query_list_by_logType(log_type, mc_util = None):
    key = 'QUERY_LIST_BY_LOG_TYPE_%s' % log_type
    return get_value(key, mc_util, lambda args:Query.objects.filter(log_type=args[0]), log_type)
    

def get_fielddef_list_by_logType(log_type, mc_util = None):
    key = 'FIELD_DEFINE_LIST_BY_LOG_TYPE_%s' % log_type
    return get_value(key, mc_util, lambda args:FieldDefine.objects.filter(log_type=args[0]), log_type)
    

def get_query_count(sql, query_key, cursor, mc_util = None):
    if None == mc_util:
        mc_util = MemcachedUtil()
     
    result = mc_util.get(query_key)
    if None == result:
        cursor.execute(sql)
        result = int(cursor.fetchone()[0])
        mc_util.set(query_key, result)
        save_cache_key(CACHE_TYPE.LOG_CACHE, query_key, mc_util)
    
    return result

def get_center_log(mc_util = None):
    key = 'CENTER_LOG'
    return get_value(key, mc_util, lambda x:LogDefine.objects.filter(status = ENUM_LOG_STATUS.SAVE_CENTER))



def get_query_data(query_key, cursor, query_sql ,mc_util = None):
    if None == mc_util:
        mc_util = MemcachedUtil()
    result = mc_util.get(query_key)
    if None == result:
        cursor.execute(query_sql)
        result = cursor.fetchall()
        mc_util.set(query_key, result)
        save_cache_key(CACHE_TYPE.LOG_CACHE, query_key, mc_util)
        
    return result

def get_query_display_data(query_key, mc_util, query_display_process, *args):
    key = 'QUERY_DISPLAY_DATA_%s' % query_key
    return get_value(key, mc_util, query_display_process, *args)
    
    


#*******统计相关*************
from GameManage.models.log import Statistic
def get_statistic_list(mc_util = None):
    key = 'STATISTIC_LIST'
    return get_value(key, mc_util, lambda x : Statistic.objects.all())

def get_statistic(model_id, mc_util = None):
    key = 'STATISTIC_%s' % model_id
    return get_value(key, mc_util, lambda args: __fetch_statistic(model_id, args[0]), mc_util)
    

def __fetch_statistic(model_id, mc_util):
    statistic_list = get_statistic_list(mc_util)
    for item in statistic_list:
        if item.id == model_id:
            return item
    
    if 0 == Statistic.objects.filter(id = model_id).count():
        return None
    
    return Statistic.objects.get(id = model_id)


    
    
    
