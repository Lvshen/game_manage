# coding=utf-8
'''

'''
from django.db import models
import time
  
class AdConfig(models.Model):
    channel_key = models.CharField(u'渠道限制', max_length=200, db_index=True)
    url = models.CharField(u'跳转URL', max_length=300, default='')
    hits = models.IntegerField(u'点击数', default=0)
    max_actives = models.IntegerField(u'限制激活数', default=0)
    remark = models.CharField(u'备注说明', max_length = 255)
    
    def __unicode__(self):
        return '%s,%s' % (self.channel_key, self.url)

    class Meta:
        db_table = u'ad_config'
        app_label = 'Adapply'
        
class AdIP(models.Model):
    channel_key = models.CharField(u'渠道限制', max_length=200, db_index=True)
    ip = models.CharField(u'IP', max_length=32, db_index=True)
    last_time = models.IntegerField(u'最后更新时间', default=int(time.time()))
    cid = models.IntegerField(u'配置ID',db_index=True)
    
    def __unicode__(self):
        return '%s,%s' % (self.channel_key, self.ip)

    def last_time_str(self):
        try:
            t = time.localtime(self.last_time)
            return time.strftime('%Y-%m-%d %H:%M:%S',t)   
        except:
            return self.last_time
        
    class Meta:
        db_table = u'ad_ip'
        app_label = 'Adapply'        
        
class AdLog(models.Model):
    channel_key = models.CharField(u'渠道限制', max_length=200, db_index=True)
    ip = models.CharField(u'IP', max_length=32, db_index=True)
    create_time = models.IntegerField(u'激活时间', default=int(time.time()))
    cid = models.IntegerField(u'配置ID',db_index=True)
    
    def __unicode__(self):
        return '%s,%s' % (self.channel_key, self.ip)

    def create_time_str(self):
        try:
            t = time.localtime(self.create_time)
            return time.strftime('%Y-%m-%d %H:%M:%S',t)   
        except:
            return self.create_time
        
    class Meta:
        db_table = u'ad_log'
        app_label = 'Adapply'        
        
