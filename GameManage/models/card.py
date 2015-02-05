#coding=utf-8
from django.db import models
from django.db import connection
from center import Channel, Server
import re

PRIZE_NAME = {1:'武将',2:'装备',3:'银币',4:'金币',5:'军功',6:'军令',7:'威望',8:'魂石',9:'战魂'}
      
class CardBatch(models.Model):
    STATUS_CHOICES = ((0,u'禁用'),(1,u'启用'))
    server = models.CharField(u'服务器',max_length=255)
    channels = models.CharField(u'渠道',max_length=255)
    key = models.CharField(u'标识',max_length=10) #标识
    name = models.CharField(u'批次',max_length=32)
    remark = models.CharField(u'备注',max_length=255,default='')
    total_count = models.IntegerField(u'总数量',default=0)
    used_count = models.IntegerField(u'已使用数量',default=0)
    limit_count = models.IntegerField(u'每用户限制使用次数',default=0)
    prize = models.CharField(u'奖励内容',max_length=255,default='')
    start_time = models.DateTimeField(u'生效时间',blank=True)
    end_time = models.DateTimeField(u'失效时间',blank=True)
    status = models.IntegerField(u'状态',default=1,choices=STATUS_CHOICES)
    
    def __unicode__(self):
        return "id:%d,name:%s" % (self.id,self.name)
    
    def get_status_name(self):
        return self.STATUS_CHOICES[self.status][1]
    
    def get_prize_content(self):
        prize_content = []
        for item in re.findall("\[(\d+,\s*\d+)\]", self.prize):
            if int(item.split(',')[1]) != 0:
                prize_content.append('%s%s'%(int(item.split(',')[1]),PRIZE_NAME[int(item.split(',')[0])]))
        return ', '.join(prize_content)
    
    def get_server_content(self):
        if self.server != '':
            server_list = [int(i) for i in self.server.split(',')]
            server_content = []
            for item in Server.objects.filter(id__in = server_list):
                server_content.append(item.name)
            return ', '.join(server_content)
        else:    
            return '所有服务器'
    
    def get_channel_content(self):
        if self.channels != '':
            channel_list = [i for i in self.channels.split(',')]
            channel_content = []
            for item in Channel.objects.filter(key__in = channel_list):
                channel_content.append(item.name)
            return ', '.join(channel_content)
        else:    
            return '所有渠道'        

    class Meta:
        db_table = u'card_batch'
        app_label = 'GameManage'
        
# Create your models here.              
class Card(models.Model):
    STATUS_CHOICES = ((-1,u'已删除'),(0,u'未使用'),(1,u'已领取'),(2,u'已使用'))
    batch = models.ForeignKey(CardBatch)
    number = models.CharField(u'新手卡号',max_length=32,unique=True,db_index=True) #format：1001 + 5数字 ＋　5字母 + 1校验位
    password = models.CharField(u'新手卡号密码',max_length=32,blank=True,null=True)
    add_time = models.DateTimeField(u'添加时间',blank=True,auto_now_add=True)
    use_time = models.DateTimeField(u'使用时间',blank=True,null=True)
    server_id = models.IntegerField(u'服务器标识',default=0,db_index=True,null=True)
    player_id = models.IntegerField(u'用户标识',default=0,db_index=True,null=True) 
    channel_key = models.CharField(u'渠道key',max_length=20)
    status = models.IntegerField(u'状态',default=0,choices=STATUS_CHOICES)

    def __unicode__(self):
        return 'status:%s'%(self.status)
    
    def get_status_name(self):
        return self.STATUS_CHOICES[self.status+1][1]
    
    def safe_save(self):
        self.lock()
        try:
            self.save()
        except Exception,e:
            print('save error',e)
        self.unlock()
        
    def lock(self):
        cursor = connection.cursor()
        cursor.execute('LOCK TABLES card_card WRITE;')

    def unlock(self):
        cursor = connection.cursor()
        cursor.execute('UNLOCK TABLES;')

    class Meta:
        db_table = u'card_0'  #format: create table card_%s like card_0;
        app_label = 'GameManage'
        
class CardLog(models.Model):
    STATUS_CHOICES = ((0,u'待发奖励'),(1,u'已发奖励'),(2,u'发送中'),(3,u'发送失败'))
    server_id = models.IntegerField(u'服务器标识',default=0,db_index=True,null=True)
    player_id = models.IntegerField(u'用户标识',default=0,db_index=True,null=True) 
    number = models.CharField(u'新手卡号',max_length=32,unique=True,db_index=True)
    channel_key = models.CharField(u'渠道key',max_length=20)
    card_key = models.CharField(u'标识',max_length=10) #标识
    card_name = models.CharField(u'卡类名称',max_length=30,default='')
    prize = models.CharField(u'奖励内容',max_length=255,default='')
    create_time = models.DateTimeField(u'添加时间',blank=True,auto_now_add=True)
    status = models.IntegerField(u'状态',default=0,choices=STATUS_CHOICES)#0待发奖励，1已发奖励

    def get_prize_content(self):
        prize_content = []
        for item in re.findall("\[(\d+,\s*\d+)\]", self.prize):
            if int(item.split(',')[1]) != 0:
                prize_content.append('%s%s'%(int(item.split(',')[1]),PRIZE_NAME[int(item.split(',')[0])]))
        return ', '.join(prize_content)  
    
    def get_status_name(self):
        return self.STATUS_CHOICES[self.status][1]
    
    def create_time_str(self):
        return self.create_time.strftime("%Y-%m-%d %H:%M:%S")
    
    def server_name(self):
        try:
            the_server = Server.objects.get(id = self.server_id)
            return the_server.name
        except:
            return ''
    class Meta:
        db_table = u'card_log'  #
        app_label = 'GameManage'    
