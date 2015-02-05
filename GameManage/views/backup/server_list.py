#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.db import connections
from GameManage.models.center import Server
from GameManage.views.base import md5
from django.http import HttpResponse
#import time
import json
import re
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
'''
    服务器内部错误                      Server Error
    限制IP            Forbidden
    没有通过身份验证                   Signature Invalid
    请求方法不存在                      Not Found
    参数错误                                 Parameter Error
    数据为空                                Not Modified
返回值：
1.    返回本游戏所有运营中的服务器列表
2.    数据格式：JSON
3.    返回数据格式及说明
[
    { 
‘unit_agent_name’: [统一平台名称],    // 与agent_name一致
‘agent_name’: [平台名称],    // 服所属运营平台名称
        ‘server_name’: [单服标识],    // 单服标识(如：S1 S2)
        ‘chinese_server_name’: [单服中文标识],    // 单服中文标识(如：人剑合一)，没有可以设置与单服标识一样
        ‘api_url’: [单服网址],    // 单服网址
        ‘open_time’: [开服时间]    // 具体到分钟，格式：2011-10-10 02:30
        ‘close_time’: [关服时间]    // 具体到分钟，格式：2012-05-10 02:30
},
    … // 更多服
]

身份验证加密方式
key 游戏提供
sign = md5(key + unixtime + method)


key    :    L9cnKuDxGJRPVeUIZQHNA40eozVAZqX7
'''
# /backup/server_list/?method=server_list&unixtime=1363750494&sign=b2d4c4deeca72a05934c24d318f15805
ALLOWED_IP = []
KEY = 'L9cnKuDxGJRPVeUIZQHNA40eozVAZqX7'

def server_list(request):
    if len(ALLOWED_IP) != 0:
        request_ip = request.META['REMOTE_ADDR']
        if request_ip not in ALLOWED_IP:
            return HttpResponse('Forbidden')

    unixtime = request.GET.get('unixtime','')
    method = request.GET.get('method','')
    sign = request.GET.get('sign','')
        
    if unixtime != '' and method != '' and sign != '':
        if method != 'server_list':
            return HttpResponse('Not Found')
                
        if not re.match('^\d+$', str(unixtime)) or len(sign) != 32 or method != 'server_list':
            return HttpResponse('Parameter Error')
        
#        current_unixtime = int(time.time())
#        # 10分钟超时
#        if (current_unixtime - int(unixtime)) >= 600:
#            print 'Time Out'
#            return HttpResponse('Signature Invalid')
        
        validate_sign = md5(u'%s%s%s' % (KEY, unixtime, method))
        print validate_sign,sign
        
        if validate_sign == sign:    
            # 去掉已删除服务器
            count_sql = "SELECT COUNT(*) FROM `servers` WHERE `status` not in (-1,0) AND `log_db_config` NOT REGEXP '\"fy\"'" 
            # 去掉已删除服务器
            query_sql = "SELECT `name`,`game_addr` AS `api_url`,DATE_FORMAT(`create_time`, '%%Y-%%m-%%d %%H:%%i') AS `open_time`, `log_db_config` FROM `servers` WHERE `status` not in (-1,0) AND `log_db_config` NOT REGEXP '\"fy\"'"
            try:
                conn = connections['read']
                cursor = conn.cursor()
                cursor.execute(count_sql)
                total_record = int(cursor.fetchone()[0])
                if total_record == 0:
                    return HttpResponse('Not Modified')
                cursor.execute(query_sql)
                list_data = cursor.fetchall()
                server = []
                server_name = ''
                agent_name = ''
                close_time = ''
                for item in list_data:
                    the_config = json.loads(item[3])
                    if 'server_name' in the_config.keys():
                        server_name = the_config['server_name']
                    else:
                        server_name = ''
                        
                    if 'agent_name' in the_config.keys():
                        agent_name = the_config['agent_name']
                    else:
                        agent_name = ''
                        
                    if 'unit_agent_name' in the_config.keys():
                        unit_agent_name = the_config['unit_agent_name']
                    else:
                        unit_agent_name = agent_name
                            
                    if 'close_time' in the_config.keys():
                        close_time = the_config['close_time']
                    else:
                        close_time = ''
                                              
                    server.append(({'unit_agent_name':unit_agent_name,'agent_name':agent_name,'server_name':server_name,'chinese_server_name':item[0],'api_url':item[1],'open_time':item[2],'close_time':close_time}))
                server = json.dumps(server)
                return HttpResponse(server)
            except Exception, e:
                print('get server_list error:', e)   
                return HttpResponse('Server Error')
        else:
            return HttpResponse('Signature Invalid')
    else:
        return HttpResponse('Parameter Error')
