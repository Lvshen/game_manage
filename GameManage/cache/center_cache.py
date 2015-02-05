# -*- coding: utf-8 -*-
from GameManage.cache.memcached_util import get_value as cache_get_value, CACHE_TYPE
from GameManage.models.center import Server, Group, Channel
from GameManage.enum import ENUM_SERVER_STATUS
from django.db.models import Q

def get_value(key, mc_util, get_data, *args):
    return cache_get_value(key, CACHE_TYPE.CENTER_CACHE, mc_util, get_data, *args)
    
def get_server_list(group_id = 0, mc_util = None):
    key = 'SERVER_LIST_%s' % group_id
    expre = lambda args:Server.objects.using('read').filter(~Q(status = ENUM_SERVER_STATUS.DELETED)).order_by('-status')
    if group_id > 0 :
        if 0 < get_server_count():  
            expre = lambda args:get_group(group_id, mc_util).server.all()
        else:
            expre = lambda args:None
    return get_value(key, mc_util, expre, group_id)

def get_server_by_id(server_id, mc_util = None):
    key = 'SERVER_ID_%s' % server_id
    return get_value(key, mc_util, lambda args: _get_server(server_id, mc_util))

import json
def get_server_config(server_id, key, default, mc_util = None):
    server = get_server_by_id(server_id, mc_util)
    result = default
    if None == server:
        return default
    try:
        if server.json_data != '':
            server.json_data = '{%s}' % server.json_data
            cfg = json.loads(server.json_data)
            result = cfg.get(key, default)
        else:
            return default
    except Exception, ex:
        print '<<center_cache get_server_config >>:', ex
        return default 
    return result
    
    
def _get_server(server_id, mc_util = None):
    server_list = get_server_list(0, mc_util)
    result = None
    for item in server_list:
        if item.id == server_id:
            result = item
            break
    
    if None == result:
        result = Server.objects.filter(id = server_id)
    
    return result
            
def get_cache_server_list_group_by(mc_util = None):
    key = 'SERVER_LIST_GROUP_BY'
    return get_value(key, mc_util, lambda args: _get_server_list_group_by(args[0]), mc_util)
        
def _get_server_list_group_by(mc_util):
    group_list = get_group_list(mc_util)
    result = []
    server_dic = {}
    for group in group_list:
        server_list = []
        group_server_list = get_group_server_list(group.id, mc_util)
        if 0 != group_server_list:
            for server in group_server_list:
                if -1 == server_dic.get(server.id, -1):
                    server_dic[server.id] = server
                    server_list.append(server)
            result.append(server_list)
            
    return result

def get_user_server_list(the_user, mc_util = None):
    key = 'USER_%s_SERVER_LIST' % the_user.id
    return get_value(key, mc_util, lambda args:args[0].server.all().order_by('create_time'), the_user)

def get_server_count(mc_util=None):
    key = 'SERVER_COUNT'
    return get_value(key, mc_util, lambda args:Server.objects.all().count())


def get_group(group_id=0, mc_util=None):
    key = 'GROUP_%s' % group_id
    return get_value(key, mc_util, lambda args:Group.objects.get(id=args[0]), group_id)

def get_group_list(mc_util = None):
    key = 'GROUP_LIST'
    return get_value(key, mc_util, lambda args:Group.objects.all())


def get_group_server_list(group_id, mc_util = None):
    group = get_group(group_id)
    key = 'GROUP_%s_SERVER' % group_id
    return get_value(key, mc_util, lambda args:args[0].server.all(), group)

def get_channel_list(mc_util = None):
    key = 'CHANNEL_LIST'
    return get_value(key, mc_util, lambda args:Channel.objects.all().order_by('name'))

def get_channel_by_id(channel_id, mc_util = None):
    key = 'CHANNEL_ID_%s' % channel_id
    return get_value(key, mc_util, lambda args:_get_channel(channel_id, mc_util))

def _get_channel(channel_id, mc_util):
    channel_list = get_channel_list(mc_util)
    result = None
    for item in channel_list:
        if channel_id == item.id:
            result = item
            break
    if result == None:
        result = Channel.objects.get(id= channel_id)
    return result
        
def get_user_channel_list(the_user, mc_util = None):
    key = 'USER_%s_CHANNEL_LIST' % the_user.id
    return get_value(key, mc_util, lambda args:args[0].channel.all().order_by('name'), the_user)
