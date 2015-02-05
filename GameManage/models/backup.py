# coding=utf-8

from django.db import models
def get_time_str(time): 
    if time == '' or time == None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Backup(models.Model):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    field_name = models.CharField(max_length=255) #统计字段
    sql = models.CharField(max_length=3000)
    auto_exec_interval = models.IntegerField(default=0) #执行间隔，单位秒
    remark = models.CharField(max_length=100, blank=True)
    backup_format = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    server_list = models.CharField(max_length=1000)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    
    def __unicode__(self):
        return '%s' % self.name


    def start_date_str(self):
        if self.start_date != '' and self.start_date != None and self.start_date != 'None':
            return self.start_date.strftime('%Y-%m-%d')
        else:
            return ''

    def end_date_str(self):
        if self.end_date != '' and self.end_date != None and self.end_date != 'None':
            return self.end_date.strftime('%Y-%m-%d')
        else:
            return ''
            
    def get_server_id(self,server_id, list_server):
        #list_server = get_server_list()
        server_list = []
        sign = False
        for item in list_server:
            server_list.append(int(item.id))
        total = len(server_list)
        target_server = server_list.index(int(server_id))+1
        if target_server < total:
            sign = True
            return server_list[target_server]
        if sign == False:
            return False
          
    class Meta: 
        db_table = u'backup'
        app_label = 'GameManage'
