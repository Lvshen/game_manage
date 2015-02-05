# coding=utf-8
'''
Created on 2011-12-19

'''
from django.db import models
import hashlib
from center import Channel, Server
  
class Menu(models.Model):
    parent_id = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100,null=True,blank=True,default='')
    icon = models.CharField(max_length=100,null=True,blank=True,default='')
    css = models.CharField(max_length=100,null=True,blank=True,default='')
    order = models.IntegerField(default=0)
    is_show = models.IntegerField(default=1)
    is_log = models.IntegerField(default=0)
    
    def __unicode__(self):
        return '%s'%self.name

    class Meta:
        db_table = u'menu'
        ordering = ('order',)
        app_label = 'GameManage'
        
class Role(models.Model):
    TYPE_CHOICES = ((0,'普通账号'),(1,'系统管理员'),(2,'专区账号'),(3,'客服账号'),)
    name = models.CharField(max_length=50)
    menu = models.ManyToManyField(Menu)
    #type = models.IntegerField(default = 0, choices=TYPE_CHOICES)
    
    def __unicode__(self):
        return '%s'%self.name
    
    class Meta:
        db_table = u'role'
        app_label = 'GameManage'
        
class Admin(models.Model):
    role = models.ForeignKey(Role)
    channel = models.ManyToManyField(Channel)
    server = models.ManyToManyField(Server)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    #create_time = models.DateTimeField(auto_now_add=True)
#    last_ip = models.CharField(max_length=20)
    last_time = models.DateTimeField(auto_now_add=True)
#    logins = models.IntegerField(default=0)
    lock_time = models.DateTimeField(null=True,blank=True)
    login_count = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    
    def __unicode__(self):
        return '%s'%self.username

    def md5_password(self):
        #return hashlib.new('md5', self.password + 'game.sanguo').hexdigest()
		return self.password
    
    class Meta:
        db_table = u'admins'
        app_label = 'GameManage'
        

    
