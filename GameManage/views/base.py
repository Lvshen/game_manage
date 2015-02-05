#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.db.models import Q
from GameManage.models.admin import Admin
from GameManage.models.center import Channel
from GameManage.models.log import Log
from GameManage.models.center import Server
from GameManage.enum import ENUM_SERVER_STATUS, ROLE_TYPE
from game_manage.settings import TEMPLATE_DIRS
import hashlib, datetime, json, MySQLdb, urllib, os

def check_author(user_name, password):
    tmp_admin = Admin();
    tmp_admin.username = user_name
    tmp_admin.password = password
    
    if tmp_admin.username == '' or tmp_admin.password == '':
        return None
    
    if Admin.objects.filter(username=tmp_admin.username).count() == 0:
        return None
    
    admin = Admin.objects.filter(username=tmp_admin.username).all()[0]
    if admin.password != tmp_admin.md5_password():
        return None
    
    return admin

class UserStateManager(object):
    __the_user = None
    __the_channel = None
    __user_server_count = None
    __user_channel_count = None
    __request = None
    __allow_exprot = None
    
    def __init__(self, request):
        self.__request = request
        self.get_the_user()
        self.get_the_channel()
      
    #获取当前登陆的管理员账号,  没有则返回   None
    def get_the_user(self):
        if self.__the_user != None:
            return self.__the_user
        
        the_user_id = self.get_the_user_id(self.__request) 
        print('~~~~~~~~~~~~~~the_user_id :', the_user_id)
        if the_user_id > 0:
            self.__the_user = Admin.objects.using('read').get(id=the_user_id)
        return self.__the_user
    
    def set_the_user(self, the_user):
        self.__the_user = the_user
    
    @staticmethod
    def get_the_user_id(request):
        return int(request.session.get('userid', '0'))
    
    #获取当前登陆的channel,  没有则返回   None
    def get_the_channel(self):
        if self.__the_channel != None:
            return self.__the_channel
        
        channel_id = int(self.__request.GET.get('channelId', '0')); 
        if channel_id > 0: 
            self.__the_channel = Channel.objects.get(id = channel_id)
        return self.__the_channel
    
    #当前登陆的账号是否管理员权限
    def current_userRole_is_root(self): 
        return self.userRole_is_root(self.get_the_user())
    
    
    def allow_export(self):
        if None != self.__allow_exprot:
            return self.__allow_exprot
        
        if self.current_userRole_is_root():
            self.__allow_exprot = True
            
        else:
            if -1 != self.get_user_role(self.get_the_user()).name.find(u'导出'):
                self.__allow_exprot = True
        
        return self.__allow_exprot
        
    
    #判断账号是否管理员权限
    def userRole_is_root(self, the_user):

        if self.is_Administrator(the_user):
            return True 
        
        if self.user_server_count() == 0 and self.user_channel_count() == 0:
            return True
        
        return False
    
    __role = None
    def get_user_role(self, the_user):
        if None != self.__role:
            return self.__role
        
        self.__role = the_user.role
        return self.__role
    
    #此为不需要权限判断的
    def is_Administrator(self, the_user=None):
        if the_user == None:
            the_user = self.__the_user
        if the_user.id == 1:
            return True
        
        if -1 != self.get_user_role(the_user).name.find(u'管理'):
            return True
        
        return False
    
    def user_server_count(self):
        if self.__user_server_count != None:
            return self.__user_server_count
        
        if self.get_the_user() == None:
            return 0
        
        self.__user_server_count = self.get_the_user().server.count()
        
        return self.__user_server_count
    
    def user_channel_count(self):
        if self.__user_channel_count != None:
            return self.__user_channel_count 
        if self.get_the_user() == None:
            return 0
        
        self.__user_channel_count = self.get_the_user().channel.count() 
        return self.__user_channel_count
    
    def check_user_login(self):
        if self.__the_user == None:
            return False 
          
        if self.__the_user.password != self.__request.session.get("key", ''):
            return False
        
        return True
        
        


class OperateLogManager(object):
    @staticmethod
    def save_operate_log(admin_id, msg, url, ipaddress, log_data = 0):
        tmp = msg
        try:
            tmp = tmp.decode('utf-8')
            msg = tmp
        except:
            pass
        msg2 = u''
        msg3 = u''
        msg4 = u''
        
        msg_len = msg.__len__()
        
        msg1 = msg
        
        
        if msg_len >= 99:
            msg1 = msg[:99]
            msg2 = msg[99:99+99]
        if msg_len >= 99*2:
            msg3 = msg[99*2:99*3]
        if msg_len >= 99*3:
            msg4 = msg[99*3:99*4]
        if msg_len >= 99*4:
            msg5 = msg[99*4:99*5]
        if msg_len >= 99*5:
            msg6 = msg[99*5:99*6]
             
        #写登录日志
        save_log('operate', 29, 0, 0, admin_id, log_data, 0, msg1, url, ipaddress, msg2, msg3, msg4)
            
    @staticmethod
    def get_request_ipAddress(request):
        return request.META['REMOTE_ADDR']

def quick_save_log(log_name, log_type, log_server, log_channel, log_user, log_data, log_result, msg):
    
    msg_len = msg.__len__()
    f1 = msg
    f2=''
    f3=''
    f4=''
    f5=''
    f6=''
    if msg_len >= 100:
        f1 = msg[:100]
    if msg_len >= 100:
        f2 = msg[100:200]
    if msg_len >= 200:
        f3 = msg[200:300]
    if msg_len >= 300:
        f4 = msg[300:400]
    if msg_len >= 400:
        f5 = msg[400:500]
    if msg_len >= 500:
        f6 = msg[500:600]
    
    save_log(log_name, log_type, log_server, log_channel, log_user, log_data, log_result, f1, f2, f3, f4, f5, f6)
    

def save_log(log_name, log_type, log_server, log_channel, log_user, log_data, log_result, f1,f2,f3,f4,f5,f6):
    code = 1
    try:
        Log._meta.db_table = 'log_%s' % log_name
        log = Log()
        log.log_type = log_type
        log.log_server = log_server
        log.log_channel = log_channel 
        log.log_user = log_user
        log.log_data =  log_data
        log.log_result = log_result
        log.f1 = f1
        log.f2 = f2
        log.f3 = f3
        log.f4 = f4
        log.f5 = f5
        log.f6 = f6
        log.log_time = datetime.datetime.now()
        log.save(using='write')
        code = 0
    except Exception, ex:
        code = -1
        print ex
    
    return code
    
def md5(s):
    signStr = hashlib.md5() 
    signStr.update(s.encode('utf-8'))
    return signStr.hexdigest()


def getConn(server_id=0):
    
    the_conn = None
    try:
        the_server = Server.objects.using('read').get(id=server_id)
        the_conn_str = json.loads(the_server.log_db_config)
            
        the_conn = MySQLdb.connect(host=the_conn_str['host'], user=the_conn_str['user'], passwd=the_conn_str['password'], port=the_conn_str.get('port',3306),db=the_conn_str['db'], charset='utf8')
        the_conn.autocommit(1)    
    except Exception, e:
        print('mysql has error0:%d,%s' % (server_id, e))
        raise Exception, e

    return the_conn

def url_encode(url):
    params = url.split('&')
    data = {}
    for item in params:
        tmp = item.split('=')
        name = tmp[0]
        value = tmp[1]
        data[name] = value
    return urllib.urlencode(data)

def get_server_list():
    return Server.objects.using('read').filter(~Q(status = ENUM_SERVER_STATUS.DELETED)).order_by('-status')

def filter_inject_sql(keyword):
    keyword = keyword.lower()
    keyword = keyword.replace('update', '')
    keyword = keyword.replace('delete', '')
    keyword = keyword.replace('*', '')
    keyword = keyword.replace('%%', '')
    keyword = keyword.replace('drop', '')
    keyword = keyword.replace('modify', '')
    keyword = keyword.replace('column', '')
    keyword = keyword.replace('contains', '')
    keyword = keyword.replace('\'', '')
    return keyword
    
def filter_sql(sql):
    #sql = sql.lower()
    #sql = sql.replace('update', '')
    #sql = sql.replace('delete', '')
    #sql = sql.replace('modify', '')
    #sql = sql.replace('column', '')
    #sql = sql.replace('lock', '') 
    #sql = sql.replace('drop', '')
    #sql = sql.replace('table', '')
    import re
    p = re.compile( '(update|delete|modify|column|lock|drop|table)', re.I)
    sql = p.sub( '', sql)
    return sql

def get_abs_path(expression):
    root_path = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(root_path, expression))
    return folder_path
            
def get_abs_path_and_mkdir(expression):
    folder_path = get_abs_path(expression)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path
    
def del_files(folder_path):
    for file_item in os.listdir(folder_path):
        try:
            itemsrc = os.path.join(folder_path, file_item)
            if os.path.isfile(itemsrc):
                os.remove(itemsrc)
        except:
            pass


    
class GlobalPathCfg(object):
    
    def __init__(self):
        self.static_folder_name = 'static'
    
    def get_static_folder_path(self):
        path = get_abs_path(r'../../%s' % self.static_folder_name)
        return path
    
    def get_current_url(self,request):
        current_url = '%s%s' % (request.get_host(), request.get_full_path())
        return current_url
    
    
    #**********图表数据模板相关*******
    def get_spline_time_charts_template_path(self):
        return '%s/charts/data_spline_time_charts.html' % get_abs_path(TEMPLATE_DIRS[0])
    
    
    #**********图表数据模板相关 END*******
    
    #**********活动定时配置文件********
    def get_server_active_cfg_save_path(self):
        static_path = self.get_static_folder_path()
        path = static_path + '/active_cfg'
        mkdir(path)
        path = path+'/' + 'server_active.json'
        return path
    
    
    #**********定时任务相关***********
    
    def get_task_cfg_save_path(self,file_name):
        static_path = self.get_static_folder_path()
        path = static_path + '/task'
        mkdir(path)
        path = path + '/' + file_name
        return path
    
    
    #**********定时任务相关  END ******
    
    #****************创建索引SQL保存文件路径**********
    def get_create_index_save_path(self, file_name):
        static_path = self.get_static_folder_path()
        path = static_path + '/sql'
        mkdir(path)
        path = path + '/' + file_name
        return path
    
    #**********公告相关*************
    def get_notice_html_template_path(self):
        return '%s/server/notice_template.html' % get_abs_path(TEMPLATE_DIRS[0])
    
    #获取公告html访问url
    def get_notice_html_url(self, request ,file_name):
        return 'http://%s/%s/notice/html/%s' % (request.get_host() ,self.static_folder_name, file_name)
    
    #获取公告html保存路径
    def get_notice_html_save_path(self, file_name):
        static_path = self.get_static_folder_path()
        path = static_path + '/notice/html'
        mkdir(path)
        path = path + '/' + file_name
        return path
    #**********公告相关  END **********
    
#w     以写方式打开，
#a     以追加模式打开 (从 EOF 开始, 必要时创建新文件)
#r+     以读写模式打开
#w+     以读写模式打开 (参见 w )
#a+     以读写模式打开 (参见 a )
#rb     以二进制读模式打开
#wb     以二进制写模式打开 (参见 w )
#ab     以二进制追加模式打开 (参见 a )
#rb+    以二进制读写模式打开 (参见 r+ )
#wb+    以二进制读写模式打开 (参见 w+ )
#ab+    以二进制读写模式打开 (参见 a+ )
