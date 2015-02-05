#! /usr/bin/python
# -*- coding: utf-8 -*-
#from django.db.models import Q
#from GameManage.models.log import Log
#def gm_desc_list(request):
#    req_type = request.GET.get('req_type', '')
#    log_user = request.GET.get('log_user', '')
#    log_server = request.GET.get('log_server', '')
#    log_data = request.GET.get('log_data', '')
#    log_result = request.GET.get('log_result')
#    
#    page_size = 50
#    page_num = request.GET.get('page_num')
#    
#    q = Q()
#    try:
#        if req_type != '':
#            q = q & Q(log_type = int(req_type))
#        if log_user != '':
#            q = q & Q(log_user = int(log_user))
#        if log_server != '':
#            q = q & Q(log_server = int(log_server))
#        if log_data != '':
#            q = q & Q(log_data = int(log_data))
#        if log_result != '':
#            q = q & Q(log_result = int(log_result))
#        
#    except Exception, ex:
#        print ex
#        
#    
#    Log._meta.db_table = 'log_gm_desc'
#    offset = page_size * page_num 
#    data_list = Log.objects.filter(q)[offset : offset + page_size]
#    
#    
