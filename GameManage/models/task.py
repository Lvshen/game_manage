# coding=utf-8
from django.db import models

def get_time_str(time): 
    if time == '' or time == None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S')

class TaskDefine(models.Model):
    STATE_CHOICES = ((0,'正常'),(1,'暂停'),(2,'任务完成'),)
    type = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=50, null=False)
    remark = models.CharField(max_length=1000)
    source_url = models.CharField(u'最初的url', max_length=200)
    source_cfg = models.CharField(u'执行该任务前的配置', max_length=1000)
    target_cfg = models.CharField(u'执行任务的配置', max_length=1000)
    trigger_date = models.DateTimeField(u'触发时间',null=False)
    end_date = models.DateTimeField(u'任务过期日期',null=False)
    interval = models.IntegerField(u'任务间隔秒数',null=False)
    request_url = models.CharField(u'任务执行的url',null=False)
    state = models.IntegerField(u'任务当前状态', default=0)
    result_msg = models.CharField(u'任务执行完返回的信息')
    counter = models.IntegerField(u'执行失败次数', default=0)
    
    def get_trigger_date(self):
        return get_time_str(self.trigger_date)
    
    def get_end_date(self):
        return get_time_str(self.end_date)
    
    def __unicode__(self):
        return '%s' % self.title
    
    def get_state(self):
        return self.STATE_CHOICES.get(self.state,'未知')

    class Meta: 
        db_table = u'def_task'
        app_label = 'GameManage'
