# -*- coding: utf-8 -*-
from GameManage.cache.memcached_util import MemcachedUtil, get_value as cache_get_value, CACHE_TYPE
from GameManage.models import Menu

def get_value(key, mc_util, get_data, *args):
    return cache_get_value(key, CACHE_TYPE.MENU_CACHE, mc_util, get_data, *args)

def get_menu_list(usm, mc_util = None):
    the_user = usm.get_the_user() 
    key = 'MENU_LIST_%s' % (the_user.id)
    expre = lambda args:args[0].role.menu.filter(is_show=1)
    
    if usm.is_Administrator():
        expre = lambda args:Menu.objects.filter(is_show=1)
        print('~~~~~~~~~~~~~~value :', get_value(key, mc_util, expre, the_user))
    return  get_value(key, mc_util, expre, the_user)
