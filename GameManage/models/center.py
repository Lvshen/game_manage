# coding=utf-8
'''
Created on 2011-12-19

'''
from django.db import models
import datetime

def get_time_str(time): 
    if time == '' or time == None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Channel(models.Model):
#    server = models.ManyToManyField(Server)
    key = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    login_key = models.CharField(max_length=32)
    create_time = models.DateTimeField(blank=True,auto_now_add=True)
    last_ip = models.CharField(max_length=20)
    last_time = models.DateTimeField(blank=True,null=True)
    last_ip = models.CharField(max_length=20)
    logins = models.IntegerField(default=0)
    
    def __unicode__(self):
        return 'channel_%s'%self.name
    
    class Meta: 
        db_table = u'channel'
        app_label = 'GameManage'
        ordering = ('id',)

class UserType(models.Model):
    name = models.CharField(u'类型名称',max_length=32)
    type_id = models.IntegerField(u'玩家类型',default=0)
    func_name = models.CharField(u'登录方法',max_length=20)
    func_ver = models.IntegerField(u'登录方法版本',default=0)
    login_config = models.CharField(u'登录设置',max_length=100)
    remark = models.CharField(u'备注',max_length=200)
    
    class Meta: 
        db_table = u'user_type'
        app_label = 'GameManage'
        ordering = ('id',)


class Auth(models.Model):
    TYPE_CHOICES = ((0,'Facebook'),(1,'QQ空间'),(2,'新浪微博'),(3,'人人网'),)
    auth_type = models.IntegerField(u'授权类型',default=0,choices=TYPE_CHOICES)
    user_type = models.IntegerField(u'账号类型',default=0,choices=TYPE_CHOICES)
    link_key = models.CharField(u'关联第三方的登录标识',max_length=50)
    access_token = models.CharField(u'授权码',max_length=100)
    class Meta: 
        db_table = u'auth'
        app_label = 'GameManage'
        ordering = ('id',)
        
        
class User(models.Model):
    STATUS_CHOICES = ((-2,'删号'),(-1,'封号'),(0,'正常'),(1,'游客'),(2,'VIP'),)
    TYPE_CHOICES = ((0,'自营'),(1,'当乐'),(2,'UC'),(3,'91'),(4,'云游'),(5,'飞流'),(6,'乐逗'),(8,'小虎'),)
    username = models.CharField(u'用户名',max_length=32)
    password = models.CharField(u'密码',max_length=32)
    user_type = models.IntegerField(u'账号类型',default=0,choices=TYPE_CHOICES)
    link_key = models.CharField(u'关联第三方登录的KEY',max_length=50)
    create_time = models.DateTimeField(u'最后登录时间',auto_now_add=True)
    last_time =  models.DateTimeField(u'最后登录时间',auto_now_add=True)
    last_ip =  models.CharField(u'最后登录IP',max_length=32)
    last_key = models.CharField(u'最后一次验证参数',max_length=50,blank=True,null=True)
    last_server = models.CharField(u'最后登录的服务器',max_length=50,blank=True,null=True)
    login_num =  models.IntegerField(u'登录次数',default=1)
    lock_time = models.DateTimeField(u'账号锁定时间', null=True,blank=True)
    login_count = models.IntegerField(u'尝试登陆次数', default=0)
    
    status = models.IntegerField(u'账号状态',default=0,choices=STATUS_CHOICES)
    
    channel_key = models.CharField(u'渠道关键字',max_length=20)
    mobile_key = models.CharField(u'手机串号',max_length=50)
    
    other = models.CharField(u'其它信息',max_length=500,blank=True,null=True)
    
    def __unicode__(self):
        return '%d_%s'%(self.user_type,self.username)
    
    
    def user_type_name(self):
        return self.TYPE_CHOICES.get(self.user_type,'未知')
    
    def create_time_str(self):
        return get_time_str(self.create_time)
    
    def last_time_str(self):
        return get_time_str(self.last_time)
    
    def is_lock(self):
        if self.status < 0:
            return True
        else:
            return False
    class Meta: 
        db_table = u'users'
        app_label = 'GameManage'
        ordering = ('-id',)

class Player(models.Model):
    STATUS_CHOICES = ((-2,'删号'),(-1,'封号'),(0,'正常'),(1,'游客'),(2,'VIP'),)
    TYPE_CHOICES = ((0,'自营'),(1,'当乐'),(2,'UC'),(3,'91'),(4,'云游'),(5,'飞流'),(6,'乐逗'),(8,'小虎'),(9,'4399'),(10,'facebook'),(11,'qq'))
    player_id = models.IntegerField(u'玩家标识',default=0,db_index=True)
    player_name = models.CharField(u'玩家名称',max_length=50,db_index=True)
    user_type = models.IntegerField(u'账号类型',default=0,db_index=True,choices=TYPE_CHOICES)
    link_key = models.CharField(u'关联第三方登录的KEY',db_index=True,max_length=50)
    create_time = models.DateTimeField(u'最后登录时间',auto_now_add=True)
    last_time =  models.DateTimeField(u'最后登录时间',auto_now_add=True)
    last_ip =  models.CharField(u'最后登录IP',max_length=32)
    last_key = models.CharField(u'最后一次验证参数',max_length=50,blank=True,null=True)
    login_num =  models.IntegerField(u'登录次数',default=1)
#    token = models.CharField(u'令牌',max_length=100,blank=True,null=True)
    
    status = models.IntegerField(u'账号状态',default=0,choices=STATUS_CHOICES)
    channel_id = models.CharField(u'渠道編號',db_index=True,max_length=20)
    mobile_key = models.CharField(u'手机串号',max_length=50,blank=True,null=True)
    
    other = models.CharField(u'其它信息',max_length=500,blank=True,null=True)
    
    def __unicode__(self):
        return '%d_%s'%(self.user_type,self.username)
    
    
    def user_type_name(self):
        return self.TYPE_CHOICES.get(self.user_type,'未知')
    
    def create_time_str(self):
        return get_time_str(self.create_time)
    
    def last_time_str(self):
        return get_time_str(self.last_time)
    
    def is_lock(self):
        if self.status < 0:
            return True
        else:
            return False
    class Meta: 
        db_table = u'player_0'
        app_label = 'GameManage'
        ordering = ('-id',)

    
class SafeQuestion(models.Model):
    user = models.ForeignKey(User)
    question = models.CharField(u'安全问题',max_length=100)
    answer = models.CharField(u'安全答案',max_length=100)
    create_time = models.DateTimeField(u'设置时间',default = datetime.datetime.now)
    class Meta: 
        db_table = u'safe_question'
        app_label = 'GameManage'
        
class Server(models.Model):
    STATUS_CHOICES = ((-1, '已删除'),(0,'停机'),(1,'维护'),(2,'良好'),(3,'繁忙'),(4,'爆满'),(5, '火爆'))
    COMMEND_CHOICES = ((0,'无'),(1,'推荐'),(2,'新服'),(3,'热门'),)
    channel = models.ManyToManyField(Channel)
#    custom_url = models.CharField(u'客服系统地址',max_length=100)
#    pay_url = models.CharField(u'支付接口地址',max_length=100)
    client_ver = models.CharField(u'针对客户端版本',max_length=500,default='')
    name = models.CharField(u'服务器名称',max_length=20)
    game_addr = models.CharField(u'服务器地址',max_length=100)
    game_port = models.IntegerField(u'服务器端口',default=0)
    log_db_config = models.CharField(u'日志数据库',max_length=100)
    report_url = models.CharField(u'战报地址',max_length=100)
    status =  models.IntegerField(u'服务器状态',default=0,choices=STATUS_CHOICES)
    create_time = models.DateTimeField(u'开服时间',auto_now_add=True)
    require_ver =  models.IntegerField(u'需要客户端最低版本',default=0)
    remark = models.CharField(u'备注',max_length=200)
    json_data = models.CharField(u'附加JSON数据',default='',max_length=1000)
    order = models.IntegerField(u'排序',default=0)
    commend = models.IntegerField(u'推荐',default=0,choices=COMMEND_CHOICES)
    
    def __unicode__(self):
        return '%s_%s'%(self.name,self.game_addr)
    
    def create_time_str(self):
        return get_time_str(self.create_time) 
    
    class Meta: 
        db_table = u'servers'
        ordering = ('order',)
        app_label = 'GameManage'

class Group(models.Model):
    key = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    server = models.ManyToManyField(Server)
    custom_url = models.CharField(u'客服系统地址',max_length=100)
    pay_url = models.CharField(u'支付接口地址',max_length=100)
    notice_url = models.CharField(u'支付接口地址',max_length=100)
    upgrade_url = models.CharField(u'更新包地址',max_length=100)
    notice_select = models.IntegerField(u'分区公告',default=0)
    remark = models.CharField(u'备注',max_length=200)
    
    class Meta: 
        db_table = u'groups'
        app_label = 'GameManage'
        
class Notice(models.Model):
    STATUS_CHOICES = ((0,'隐藏'),(1,'显示'),)
    TYPE_CHOICES = ((3,'分区公告'),(1,'游戏滚动公告'),(2,'游戏公告'),(4,'推送消息'),)
    channel = models.ManyToManyField(Channel)
    server=models.ManyToManyField(Server)
    group = models.ManyToManyField(Group)
    client_ver = models.CharField(u'针对客户端版本',max_length=50,default='')
    title = models.CharField(u'消息标题', max_length=200)
    content = models.TextField(u'消息内容')
    link_url = models.CharField(u'消息链接',max_length=100,blank=True)
    begin_time= models.DateTimeField(u'公告开始时间',default = datetime.datetime.now)
    end_time = models.DateTimeField(u'公告过期时间',default = datetime.datetime.now)
    status = models.IntegerField(u'状态',default=1,choices=STATUS_CHOICES)
    pub_ip = models.CharField(u'操作人IP地址',max_length=20)
    pub_user = models.IntegerField(u'操作人ID')
    notice_type = models.IntegerField(u'类型',default=0,choices=TYPE_CHOICES)
    intervalSecond = models.IntegerField(u'间隔时间',default=0)
    size = models.CharField(u'显示的size', max_length=20,default='0.9,0.9')
    
    def begin_time_str(self): 
        return get_time_str(self.begin_time)
    
    def end_time_str(self):
        return get_time_str(self.end_time)
  
    class Meta: 
        db_table = u'notice'
        app_label = 'GameManage'
        ordering = ('notice_type',)
        
class Upgrade(models.Model):
    ver_num = models.IntegerField(u'新版本号',default=0)
    ver_name = models.CharField(u'新版本名称',max_length=20)
    filesize = models.CharField(u'文件包大小',max_length=10)
    channel = models.ManyToManyField(Channel)
    group = models.ManyToManyField(Group)
    client_ver = models.CharField(u'针对客户端版本',max_length=50,default='')
    download_url = models.CharField(u'下载包路径',max_length=500)
    page_url = models.CharField(u'下载页面URL',max_length=500)
    remark = models.CharField(u'更新备注',max_length=500)
    create_time = models.DateTimeField(u'发布时间',auto_now_add=True)
    pub_ip = models.CharField(u'操作人IP地址',max_length=20)
    pub_user = models.IntegerField(u'操作人ID')
    
    def create_time_str(self): 
        return get_time_str(self.create_time) 

        
    class Meta: 
        db_table = u'upgrade'
        app_label = 'GameManage'
        ordering = ('-ver_num',)
class richmanhelp(models.Model):
    TYPE_CHOICES = ((1,'开始游戏'),(2,'选择模式'),(3,'进行游戏'),(4,'商城'),(5,'各城市特征'))
    channel = models.ManyToManyField(Channel)
    title = models.CharField(u'消息标题', max_length=200)
    content = models.TextField(u'消息内容')
    notice_type = models.IntegerField(u'类型',default=0,choices=TYPE_CHOICES)
    ctime = models.DateTimeField(u'创建时间',auto_now_add=True)

    def ctime_time_str(self):
        return get_time_str(self.ctime)
                                      
    class Meta: 
        db_table = u'richmanhelp'
        app_label = 'GameManage'
        ordering = ('notice_type',)


class richman(models.Model):
    ver_num = models.CharField(u'版本号',max_length = 50) 
    channel = models.ManyToManyField(Channel) 
    baglist = models.CharField(u'更新包详细列表',max_length = 5000)
    idlist = models.CharField(u'资源包id列表',max_length = 5000)
    ctime = models.DateTimeField(u'创建时间',auto_now_add=True)

    def ctime_time_str(self):
        return get_time_str(self.ctime)

    class Meta:
        db_table = u'richman'
        ordering = ('-ver_num',)
        app_label = 'GameManage'

class source(models.Model):
    ver_num = models.CharField(u'新版本号',max_length = 50)
    name = models.CharField(u'资源名称',max_length = 50)
    slist = models.CharField(u'包含的列表',max_length = 5000)
    md5 = models.CharField(u'资源名称',max_length = 50)
    channel = models.ManyToManyField(Channel)
    ctime = models.DateTimeField(u'创建时间',auto_now_add=True)

    def ctime_time_str(self):
        return get_time_str(self.ctime)

    class Meta:
        db_table = u'source'
        ordering = ('-ver_num',)
        app_label = 'GameManage'

class Question(models.Model):
    server_id = models.IntegerField()
    channel_id = models.IntegerField(default=0)
    question_type = models.IntegerField()
    status = models.IntegerField(default=0)
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=400)
    post_time = models.DateTimeField(auto_now_add=True)
    reply_time=models.DateTimeField(blank=True,null=True)
    post_user=models.IntegerField(default=0)
    post_user_id=models.IntegerField(default=0)
    #post_user=models.ForeignKey(User)
    score = models.IntegerField(default=-1)
    reply_user=models.CharField(max_length=20)
    def __unicode__(self):
        return '%d_%s'%(self.post_user__id,self.post_time.strftime('%Y-%m-%d'))
    
    def post_time_str(self):
        return get_time_str(self.post_time)
    
    def reply_time_str(self):
        s = ''
        if self.reply_time!=None and self.reply_time != '':
            s = self.reply_time.strftime('%m-%d %H:%M:%S')
        
        return s
    
    class Meta: 
        db_table = u'question'
        ordering = ('-id',)
        app_label = 'GameManage'

class BlockUser(models.Model):
    user = models.ForeignKey(User)
    server = models.ForeignKey(Server)
    
    class Meta: 
        db_table = u'block_user'
        ordering = ('-id',)
        app_label = 'GameManage'
