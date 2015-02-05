# -*- coding: utf-8 -*-
import memcache, datetime, time

class MemcachedUtil(object):
    def __init__(self, memcache_host=['127.0.0.1:11211'], valid_date = 1200):
        self.memcache_host = memcache_host
        self.valid_date = valid_date
        self.mc = memcache.Client(self.memcache_host, debug=1)
    
    def get(self, key, clear_before = lambda *args:True, *args):
        result = self.mc.get(key)
        
        cache_time = self.mc.get('CACHE_TIME')
        now = datetime.datetime.now()
        now = time.mktime(now.timetuple())
        if None != cache_time:
            limit = 60 * 20
            if (now - cache_time) > limit:
                clear = True
                try:
                    clear = clear_before(result, args)
                except Exception, ex:
                    clear = True
                    print ex
                if clear:
                    self.mc.flush_all()
                    print 'flush all cache'
                    self.mc.set('CACHE_TIME', now)
        else:
            print 'start cache ', now
            self.mc.set('CACHE_TIME', now)
        
        return result
    
    def safe_get(self, key):
        return self.mc.get(key)
    
    def clear_all(self):
        self.mc.flush_all()
        
    def set(self, key, value, time = -1):
        if -1 == time:
            time = self.valid_date
        return self.mc.set(key, value, time)


def get_value(key, cache_type, mc_util = None,get_data = lambda args:None, *args):
    
    if None == mc_util:
        mc_util = MemcachedUtil()
    result = mc_util.get(key)
    
    if None == result:
        result = get_data(args)
        mc_util.set(key, result)
        save_cache_key(cache_type, key, mc_util)
        
    return result


class CACHE_TYPE(object):
    CENTER_CACHE = 'CENTER_CACHE_KEYS'
    LOG_CACHE = 'LOG_CACHE_KEYS'
    MENU_CACHE = 'MENU_CACHE_KEYS'
    
    
def clear_cache(cache_type, mc_util = None):
    if None == mc_util:
        mc_util = MemcachedUtil()
    key_list = mc_util.get(cache_type)
    if None == key_list:
        return
    
    for cache_key in key_list:
        mc_util.mc.delete(cache_key)

    
def save_cache_key(cache_type, key, mc_util):
    mc_util.valid_date = 3600 * 24
    keys = mc_util.get(cache_type)
    if None == keys:
        keys = {}
    if '' == keys.get(key, ''):
        keys[key] = key
        mc_util.set(cache_type, value = keys)

