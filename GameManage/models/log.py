# coding=utf-8
'''
Created on 2011-12-19

@author: Administrator
'''
from django.db import models
from django.db import connection
from center import Channel, Server
import datetime, time, json, calendar

def get_time_str(time): 
    if time == '' or time == None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Log(models.Model):
    log_type = models.IntegerField(default=0)
    log_user = models.IntegerField(default=0, db_index=True)
    log_server = models.IntegerField(default=0, db_index=True)
    log_channel = models.IntegerField(default=0, blank=True, db_index=True)
    log_data = models.IntegerField(default=0, db_index=True)
    log_result = models.IntegerField(default=0)
    log_time = models.DateTimeField(auto_now_add=True)
    f1 = models.CharField(max_length=100, null=True, blank=True)
    f2 = models.CharField(max_length=100, null=True, blank=True)
    f3 = models.CharField(max_length=100, null=True, blank=True)
    f4 = models.CharField(max_length=100, null=True, blank=True)
    f5 = models.CharField(max_length=100, null=True, blank=True)
    f6 = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return '%d_%d_%s'(self.log_type, self.log_user, self.log_time.strftime('%Y-%m-%d'))

    def log_time_str(self):
        return get_time_str(self.log_time)

    class Meta: 
        db_table = u'log_0'
        app_label = 'GameManage'
        
class LogDefine(models.Model):
    key = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    remark = models.CharField(max_length=200)
    status = models.IntegerField(default=0)
    #def_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s' % self.key

    class Meta: 
        db_table = u'def_log'
        app_label = 'GameManage'

class FieldDefine(models.Model):
    log_type = models.IntegerField(default=0)
    field_type = models.CharField(max_length=20)
    field_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    field_format = models.CharField(max_length=100) 
    create_index = models.BooleanField(default=0)
    
    def __unicode__(self):
        return '%s' % self.field_name
    class Meta: 
        db_table = u'def_field'
        app_label = 'GameManage'
        
class ValueDefine(models.Model):
    field_id = models.IntegerField()
    value_id = models.IntegerField()
    value = models.CharField(max_length=50)
    def __unicode__(self):
        return '%s' % self.value
    
    class Meta: 
        db_table = u'def_value'
        app_label = 'GameManage'
        
class Query(models.Model):
    log_type = models.IntegerField()
    name = models.CharField(max_length=100)
    select = models.CharField(max_length=100)
    where = models.CharField(max_length=100)
    group = models.CharField(max_length=50)
    order = models.CharField(max_length=20)
    order_type = models.IntegerField(default=0)
    sql = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now_add=True)
    cache_validate = models.IntegerField()
    def __unicode__(self):
        return '%s' % self.name
    
    class Meta: 
        db_table = u'query'
        app_label = 'GameManage'
        
class Statistic(models.Model):
    STATUS_CHOICES = ((0, '结果数量数'), (1, '值求和'), (2, '求平均值'), (3, '求最大值'), (4, '求最小值'),)
     
    log_type = models.IntegerField()
    count_type = models.IntegerField(default=0, choices=STATUS_CHOICES) #统计类型：求和，求差，求平均
    name = models.CharField(max_length=200)
    field_name = models.CharField(max_length=50) #统计字段
    where = models.CharField(max_length=50)
    sql = models.CharField(max_length=2000)
    exec_interval = models.IntegerField(default=0) #执行间隔，单位秒
    last_exec_time = models.DateTimeField(null=True, blank=True)
    is_auto_execute = models.IntegerField(default=0)
    auto_exec_interval = models.IntegerField(default=0) #执行间隔，单位秒
    remark = models.CharField(max_length=100, blank=True)
    result_data = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return '%s' % self.name

    def last_exec_time_str(self):
        return get_time_str(self.last_exec_time)
        
        
    def get_result_json(self):
        if self.result_data != '' and self.result_data != None:
            the_json = json.loads(self.result_data)
            the_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            if the_date == the_json['date']:
                return the_json
        
        #处理,昨天,前天,本周,上月同一天
        today = datetime.date.today()
        last_day = today.day
        
        #当前月份天数
        current_month_days = calendar.monthrange(today.year, today.month)[1]
        if current_month_days < last_day:
            last_day = current_month_days
        
        now_date = datetime.datetime.now()
        
        list_date = [(now_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                     (now_date - datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
                     (now_date - datetime.timedelta(weeks=1)).strftime('%Y-%m-%d'),
                     (now_date - datetime.timedelta(days=current_month_days)).strftime('%Y-%m-%d')]
        
        query_sql = 'select result_time,sum(result) from result where statistic_id=%d and result_time in("%s") group by result_time desc limit 10' % (self.id, '","'.join(list_date))
        cursor = connection.cursor()
        cursor.execute(query_sql) 
        list_record = cursor.fetchall() 
        #cursor.close()
        #list_record = Result.objects.filter(statistic__id=self.id,create_time__in=list_date).order_by('-create_time')
        new_json = {}
        new_json['date'] = list_date[0]
        
        
        the_value = 0.0
       
        for item_record in list_record:
            print item_record
            item_date = item_record[0].strftime('%Y-%m-%d')
            tmp = 0
            if float(item_record[1]) != 0:
                tmp = (the_value / float(item_record[1]) - 1)
                
            if item_date == list_date[0]: 
                the_value = int(item_record[1])
                new_json['default'] = '%d' % the_value
            elif item_date == list_date[1]: 
                new_json['day'] = '%.2f' % (tmp * 100)
            elif item_date == list_date[2]: 
                new_json['week'] = '%.2f' % (tmp * 100)
            elif item_date == list_date[3]: 
                new_json['month'] = '%.2f' % (tmp * 100)
                
        self.result_data = str(new_json).replace('\'', '"')
        self.save(using='write') 
        return new_json

    class Meta: 
        db_table = u'statistic'
        app_label = 'GameManage'
        ordering = ('-last_exec_time',)

class Result(models.Model):
    statistic = models.ForeignKey(Statistic)
    server = models.ForeignKey(Server)
    channel = models.ForeignKey(Channel)
    result = models.FloatField()
    create_time = models.DateTimeField()
    result_time = models.DateTimeField()
    def result_time_int(self):
        return int(time.mktime(self.result_time.timetuple()) * 1000)

    def result_time_str(self):
        return get_time_str(self.result_time)
    
    def __unicode__(self):
        return '%s' % self.statistic.name

    def cmp_time(self,days):
        time_slot = 86400000
        if days >= 8*24:
            time_slot = 30 * 86400000
        elif days >= 4*24:
            time_slot = 14 * 86400000
        elif days >= 2*24:
            time_slot = 7 * 86400000
        elif days >= 24:
            time_slot = 2 * 86400000
        return time_slot

    def get_month(self,sdate,edate):
        month_list = []
        sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d').strftime('%Y-%m')
        edate = datetime.datetime.strptime(edate, '%Y-%m-%d').strftime('%Y-%m')
        month_list.append(sdate)
        print sdate,edate
        diff = (int(datetime.datetime.strptime(edate, '%Y-%m').strftime('%Y')) - int(datetime.datetime.strptime(sdate, '%Y-%m').strftime('%Y'))) *12 + (int(datetime.datetime.strptime(edate, '%Y-%m').strftime('%m')) - int(datetime.datetime.strptime(sdate, '%Y-%m').strftime('%m')))
        print diff
        temp_date = sdate.split("-")
        print temp_date
        for i in range(1,diff):
            month_list.append(self.datetime_offset_by_month(datetime.date(int(temp_date[0]),int(temp_date[1]),1), i))
        month_list.append(edate)
        return month_list
    
    def get_year(self,sdate,edate):
        year_list = []
        sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d').strftime('%Y')
        edate = datetime.datetime.strptime(edate, '%Y-%m-%d').strftime('%Y')
        diff = int(edate) - int(sdate)
        for i in range(1,diff):
            year_list.append(int(sdate)+int(i))
        year_list.append(sdate)
        return year_list

    def datetime_offset_by_month(self,datetime1, n = 1):
        one_day = datetime.timedelta(days = 1)
    
        q,r = divmod(datetime1.month + n, 12)
    
        datetime2 = datetime.datetime(datetime1.year + q, r + 1, 1) - one_day

        if datetime1.month != (datetime1 + one_day).month:
            return datetime2

        if datetime1.day >= datetime2.day:
            return datetime2
        
        return datetime2.replace(day = datetime1.day).strftime("%Y-%m")
          
    class Meta: 
        db_table = u'result'
        ordering = ('-id',)
        app_label = 'GameManage'
    
    
class QueryResult(models.Model):
    name = models.CharField(u'查询名称', max_length=100)
    remark = models.CharField(u'查询说明', max_length=200)
    statistic = models.ManyToManyField(Statistic)
    
    class Meta: 
        db_table = u'query_result'
        app_label = 'GameManage'
    
