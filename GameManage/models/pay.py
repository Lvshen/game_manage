# coding=utf-8
'''
Created on 2011-12-19

'''
from django.db import models
from django.db import connections
import datetime,time,uuid,json

def get_time_str(time): 
    if time == '' or time == None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S')


class PayChannel(models.Model):
    STATUS_CHOICES = ((-1,'隐藏'),(0,'正常'),(1,'推荐'),)
    server_id = models.IntegerField(u'专属服务器',default=0,db_index=True)#大于0则表示该支付通道只在某服务器可用
    channel_key = models.CharField(u'渠道限制',max_length=200)
    name = models.CharField(u'通道名称',max_length=20)
    link_id = models.CharField(u'关联第三方标识',max_length=50,db_index=True)
    icon = models.CharField(u'充值通道图标',max_length=20,default='')
    func_name =  models.CharField(u'使用支付函数',max_length=20,default='downjoy')
    pay_type = models.IntegerField(u'支付类型',default=1)
    post_url =  models.CharField(u'通道请求地址',max_length=100)
    notice_url = models.CharField(u'通知我们支付接口成功的地址',max_length=100)
    pay_config = models.CharField(u'支付接口的参数配置',max_length=1000)
    remark =  models.CharField(u'通道描述',max_length=200)
    exchange_rate = models.FloatField(u'兑换汇率',default=0.00)
    status = models.IntegerField(u'通道状态',default=0,choices=STATUS_CHOICES)
    order = models.IntegerField(default=0)
    unit = models.CharField(u'单元',max_length=10,default='元')
    
    def __unicode__(self):
        return '%s_%s'%(self.func_name,self.name)
    
    
    def get_gold(self,pay_amount):
        return self.exchange_rate * float(pay_amount)
    
    
    def is_extra(self):
        extra_list = self.get_config_value('extra', [])
        if extra_list.__len__() > 0:
            return True
        else:
            return False
        
    # 获取返利额
    def get_extra(self, pay_gold,server_id=0):

        result = 0
        try:
            extra_list = self.get_config_value('extra', '')
            if extra_list == '':
                return 0
            if extra_list.__len__() == 0:
                return 0
            
            server_list = self.get_config_value('server_list', [])
            if server_id > 0 and server_list.__len__() > 0:
                if not server_list in server_list:
                    return 0
            
            for extra in extra_list:
                conditions = extra.get('conditions', '')
                if conditions.__len__() >= 2:
                    if pay_gold >= float(conditions[0]) and pay_gold <= float(conditions[1]):
                        result = float(extra.get('amount', '0'))
                        if result < 1:
                            result = result * pay_gold
        except Exception,e:
            print('extra has error',e)
        return result
    
    __cache_pay_config = None
    def get_config_value(self,key_name,default_value):
        if self.pay_config.__len__() == 0:
            return default_value;
        if self.__cache_pay_config == None:
            self.__cache_pay_config = json.loads(self.pay_config)
        return self.__cache_pay_config.get(key_name, default_value)
    
    class Meta: 
        db_table = u'pay_channel'
        ordering = ('order',)
        app_label = 'GameManage'
        
class PayAction(models.Model):
    STATUS_CHOICES = ((0,'已提交,未支付'),(1,'已转发,未回复'),(2,'已支付,金币发放中'),(3,'金币发放中'),(4,'充值成功,金币已发放'),)
    query_id = models.CharField(u'查询编号',max_length=40,default='')
    order_id = models.CharField(u'订单编号',max_length=60,db_index=True,blank=True,null=True)
    channel_key = models.CharField(u'客户端渠道KEY',max_length=20)
    channel_id = models.IntegerField(u'渠道ID',default=0)
    server_id = models.IntegerField(u'服务器ID',default=1,db_index=True)
    pay_type = models.IntegerField(u'支付类型',default=1,db_index=True)
    pay_user = models.IntegerField(u'支付账号',db_index=True)
    pay_ip = models.CharField(u'支付IP',max_length=20)
    pay_status = models.IntegerField(u'支付状态',default=0,choices=STATUS_CHOICES) 
    card_no = models.CharField(u'支付账号',max_length=50)
    card_pwd = models.CharField(u'支付账号',max_length=50)
    post_time = models.DateTimeField(u'提交时间',auto_now_add=True)
    last_time = models.DateTimeField(u'支付时间',blank=True,null=True)
    post_amount = models.FloatField(u'提交金额',default=0.00)
    pay_amount = models.FloatField(u'实际支付金额',default=0.00)
    pay_gold = models.IntegerField(u'支付金额兑换的金币数量',default=0)
    extra = models.FloatField(u'赠送金币', default=0.00)
    remark = models.CharField(u'备注',blank=True,null=True,max_length=200)
    
    def __unicode__(self):
        return '%d_%s'%(self.pay_user,self.query_id)
    
    def pay_type_name(self):
        return ''

    def total_gold(self):
        return self.pay_gold + self.extra
    
    def pay_status_name(self):
        if self.pay_status<0:
            return u'失败:%s'%self.remark
        else:
            return u'%s'%self.get_pay_status_display()
        
    def post_time_str(self):
        return get_time_str(self.post_time)

    def post_time_int(self):
        return int(time.mktime(self.post_time.timetuple()))
    
    def last_time_str(self):
        return get_time_str(self.last_time)
    
    def last_time_int(self):
        return int(time.mktime(self.last_time.timetuple()))
    
    def get_query_id(self):
        return datetime.datetime.now().strftime('%y%m%d%H%M%S%f')+str(uuid.uuid4()).split('-')[1].upper()

    def set_query_id(self):
        self.query_id = self.get_query_id()
    
    def safe_save(self,has_order_id=False):
        try:
            PayAction.lock()
            if has_order_id ==False or (has_order_id and PayAction.objects.using('write').filter(pay_type=self.pay_type, order_id=self.order_id).count() == 0):
                self.save(using='write')
        except Exception,e:
            print('save error',e)
        finally:
            PayAction.unlock()
            
    @staticmethod
    def lock():
        cursor = connections['write'].cursor()
        cursor.execute('LOCK TABLES pay_action WRITE;')
        row = cursor.fetchone()
        #cursor.close()
        return row
    
    @staticmethod
    def unlock():
        cursor = connections['write'].cursor()
        cursor.execute('UNLOCK TABLES;')
        row = cursor.fetchone()
        #cursor.close()
        return row      
     
    class Meta: 
        db_table = u'pay_action'
        ordering = ('-id',)
        app_label = 'GameManage'
