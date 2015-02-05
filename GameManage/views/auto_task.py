#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse

import random, datetime,time

def run_task(request): 
    now = datetime.datetime.now()
    
    next_time = time.mktime((now + datetime.timedelta(minutes = 2)).timetuple())
    
    params = [['sleep_time#3', 'next_url#http://10.1.1.103:8080/service/autotask'],
              ['sleep_time#5', 'next_url#http://10.1.1.103:8080/service/autotask'],
              ['sleep_time#2', 'next_url#http://10.1.1.103:8080/service/autotask'],
              ['next_time#%s'%next_time],
              ['NEXT_TIME#%s#NEXT_URL#%s'%(next_time, 'http://10.1.1.103:8080/service/autotask?new')]
              ]
    a = 0
    b = 4
    return HttpResponse('#'.join(params[random.randint(a,b)])) 
