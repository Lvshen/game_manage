# coding=utf-8

from django.db import models

class GMDefine(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=50)
    params = models.CharField(max_length=6000)
    result_type = models.CharField(max_length=20)
    result_define = models.CharField(max_length=6000)
    flag = models.CharField(max_length=100)
    
    class Meta:
        db_table = u'def_gm'
        app_label = 'GameManage'
