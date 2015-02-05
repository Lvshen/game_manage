#coding=utf-8
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from GameManage.models.card import CardBatch
from django.db import connections
import datetime
from GameManage.views.base import UserStateManager, get_server_list
from GameManage.models.center import  Channel, Group
import re,json
#from GameManage.views.log.exprot_file import QueryExprot
#import json
#import string
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def group_ajax(request):
    group = int(request.POST.get('group', '0'))
    option_str = []
    option_str.append('<option value="0">服务器</option>')
    if 0 != group:
        list_server = Group.objects.get(id = group).server.all()
    else:
        list_server = get_server_list() 
    if len(list_server) != 0:
        for item in list_server:
            option_str.append('<option value="%s">%s</option>'%(item.id, item.name))
    return HttpResponse(''.join(option_str))   
    
def batch_list(request):
    #usm = UserStateManager(request)
    #list_group = []
    
    #if usm.current_userRole_is_root():
    list_group = Group.objects.all()    
    
    query = ['1=1']
    status = int(request.GET.get('status','1'))
    query.append(' and status = %d '% status)
    page_size = 15
    page_num = int(request.GET.get('page_num', '1'))    
    if page_num < 1:
        page_num = 1 
    search_card = int(request.GET.get('search_card','0'))
    search_card_val = request.GET.get('search_card_val','')
  
    server_id = int(request.GET.get('server_id','0'))    
    group = int(request.GET.get('group','0')) 
    if 0 != group:
        try:
            list_server = Group.objects.get(id = group).server.all()
        except:
            list_server = None
            pass
    else:
        list_server = get_server_list() 
    card_batch = None
    if status == 1:
        query.append(" and end_time >= '%s'"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif status == 0:
        query.append(" or end_time < '%s'"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    if search_card != 0 and search_card_val !='':
        if search_card == 1:
            query.append(" and `key` = '%s'"%search_card_val)
        elif search_card == 2:
            query.append(" and `name` like '%s%s%s'"%('%%',search_card_val,'%%'))        
    if server_id != 0:
        query.append(" and `server` REGEXP '^%d$|,%d|%d,' "%(server_id,server_id,server_id))
    elif group != 0:
        query_server_id = []
        for item in list_server:
            query_server_id.append("`server` REGEXP '^%d$|,%d|%d,' "%(item.id,item.id,item.id))
        if len(query_server_id) != 0:
            query.append(" and (%s) "%(' or '.join(query_server_id)))
        else:
            query.append(" and 0 ")
    #return HttpResponse(''.join(query))
    total_record = CardBatch.objects.using('card').extra(where=[''.join(query)]).count() 
    if total_record:   
        card_batch = CardBatch.objects.using('card').extra(where=[''.join(query)])[(page_num - 1) * page_size:page_num * page_size] 
        for item in card_batch:
            item.prize_content = item.get_prize_content()
            item.server_content = item.get_server_content()
            item.channel_content = item.get_channel_content()
            item.expire = 0
            if item.end_time < datetime.datetime.now():
                item.expire = 1
                
            if item.used_count == item.total_count:
                item.rate = 100
            else:
                item.rate = round(float(item.used_count) * 100 / item.total_count,2)
    parg = {}
    parg["page_num"] = page_num
    parg["page_size"] = page_size
    parg["total_record"] = total_record
    parg["batch"] = card_batch
    parg['status'] = status
    parg['list_server'] = list_server
    parg['server_id'] = server_id
    parg['search_card'] = search_card
    parg['search_card_val'] = search_card_val   
    parg['list_group'] = list_group 
    parg['group'] = group
    return render_to_response('card/batch_list.html', parg)

def batch_edit(request):
    tmp_group_id = request.GET.get('group_id', 0)
    model_id = request.GET.get('id', 0)
    group_id = 0
    try:
        group_id =  int(tmp_group_id)
    except:
        pass
    usm = UserStateManager(request)
    the_user = usm.get_the_user()
    
    if usm.current_userRole_is_root():
        list_channel = Channel.objects.using('read').all().order_by("-logins")
    else:
        list_channel = the_user.channel.all().order_by("-logins")
#        
#    for item1 in list_channel:
#        if query_channel.__len__() > 0:
#            if str(item1.id) in query_channel:
#                item1.is_show = 1 
#        else:
#            item1.is_show = 1
    
    
    list_group = []
    
    if usm.current_userRole_is_root():
        list_group = Group.objects.all()
        if 0 != group_id:
            list_server = Group.objects.get(id = group_id).server.all()
        else:
            list_server = get_server_list()
    else:
        list_server = the_user.server.all().order_by("id")
#    query_server = request.GET.getlist('s')#server_id
#    query_channel = request.GET.getlist('c')#server_id
#    
#    for serverItem in list_server:
#        if len(query_server) > 0:
#            if str(serverItem.id) in query_server:
#                serverItem.is_show = 1    
#        else:
#            serverItem.is_show = 1
##            
##    for channelItem in list_channel:
##        if len(query_channel) > 0:
##            if str(channelItem.id) in query_channel:
##                channelItem.is_show = 1    
##        else:
##            channelItem.is_show = 1    
    query_server = []
    query_channel = []
                        
    model_id = int(model_id)
    
    prize = '[[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]'
    the_key = ''
    if model_id > 0:
        model = CardBatch.objects.using('card').get(id=model_id)
        query_server = model.server.split(',')
        query_channel = model.channels.split(',')
        prize = model.prize
    else :
        try:
            conn = connections['card']
            cursor = conn.cursor()
            sql = "SELECT SUBSTR(`table_name`,6) + 1 FROM INFORMATION_SCHEMA.`TABLES` WHERE `table_schema` = 'card' AND `table_name` NOT LIKE 'card_9%%' AND `table_name` REGEXP 'card_[[:digit:]]{4}$' ORDER BY `table_name` DESC LIMIT 1"
            cursor.execute(sql)
            count = cursor.fetchone()
            the_key = int(count[0])
        except:
            pass
        
        now = datetime.datetime.now()
        model = CardBatch()
        model.id = model_id
        model.limit_count = 1
        if not the_key:
            model.key = 1000
        elif the_key < 9999 and the_key > 1000:
            model.key = the_key
        model.start_time = now.strftime("%Y-%m-%d 00:00:00")
        model.end_time = (now + datetime.timedelta(days=90)).strftime("%Y-%m-%d 00:00:00")
        
    prize_help = {}
    for item in re.findall("\[(\d+,\s*\d+)\]", prize):
        prize_help[item.split(',')[0].strip(' ')] = item.split(',')[1].strip(' ')
    for serverItem in list_server:
        if len(query_server) > 0:
            if str(serverItem.id) in query_server:
                serverItem.is_show = 1    
        else:
            serverItem.is_show = 1
            
    for channelItem in list_channel:
        if len(query_channel) > 0:
            if str(channelItem.key) in query_channel:
                channelItem.is_show = 1    
        else:
            channelItem.is_show = 1    
    
    parg = {}
    parg["usm"] = usm    
    parg["model"] = model
    parg["list_server"] = list_server
    parg["list_channel"] = list_channel
    parg["prize"] = prize
    parg["prize_help"] = prize_help
    parg["list_group"] = list_group
    parg["group_id"] = group_id  
    parg["the_key"] = the_key  
    return render_to_response('card/batch_edit.html', parg)  
  
def batch_save(request):
    msg = ''
    server_list = request.POST.getlist('s')
    channel_list = request.POST.getlist('c')
    
    
    model_id = request.GET.get('id','')
    model_id = int(model_id)
    key = request.POST.get('key','')
    name = request.POST.get('name','')
    limit_count = request.POST.get('limit_count','')
    remark = request.POST.get('remark','')
    start_time = request.POST.get('start_time','')
    end_time = request.POST.get('end_time','')
    
    prize = request.POST.get('prize','')
    

    if key == '' or len(key) != 4:
        msg = '标识只能是4位纯数字！'
    elif name == '':
        msg = '名称不能为空！'
    elif limit_count == '':
        msg = '可用次数不能为空！'   
    elif start_time == '' or end_time == '':
        msg = '时间不能为空！'        
    elif start_time > end_time:
        msg = '开始时间不能大于结束时间！'
    elif end_time < datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        msg = '结束时间不能小于服务器时间！'
    
    if model_id > 0:
        model = CardBatch.objects.using('card').get(id = model_id)
    else:
        model = CardBatch() 
        if CardBatch.objects.using('card').filter(key = key).count() > 0:
            msg = '礼包卡类标识已经存在！'
    if prize != '':
        try:
            json.loads(prize)
        except Exception,e:
            print 'json error',e
            msg = '奖励格式有误！请检查！'
    if msg == '' and key != '' and name !='' and limit_count != ''  and start_time != '' and end_time != '':
        try:
   
            if prize != '':
                pass
            else:
                prize = []
                for i in range(1,10):
                    if request.POST.get('prize_%d'%i,'0') != '' and request.POST.get('prize_%d'%i,'0') != '0':
                        prize.append([i,int(request.POST.get('prize_%d'%i,'0').strip(' '))])
            if model_id == 0:    
                model.key = key
            model.name = name
            model.start_time = start_time
            model.end_time = end_time
            model.limit_count = limit_count
            model.prize = '%s'%prize#'{ "msg":["%s",%s]}'%(name,prize)
            model.server = ','.join(server_list)
            #model.channels = ','.join(channel_list)
            model.remark = remark
            model.save(using='card')
            msg = '操作成功！'
            if model.id > 0 and model_id == 0:
                try:
                    sql = "CREATE TABLE IF NOT EXISTS `card_%s` LIKE `card_0`" % key
                    conn = connections['card']
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    cursor.close()
                except Exception,e:
                    print 'create table `card_%s` error' % key
                    msg = '礼包卡类标识已经存在！'%e
        except Exception,e:
            print 'save batch error',e
            msg = '%s'%e
    parg = {} 
    parg['msg'] = msg
    parg['next_url'] = '/card/batch/?status=1'
    print msg
    #return HttpResponseRedirect('/card/batch/?status=1')
    return render_to_response('card/feedback.html', parg)
    
def batch_del(request):
    ids = request.GET.get('ids','0')
    if ids != '':
        try:
            card_batch = CardBatch.objects.using('card').filter(id__in = ids.split(','))
            for item in card_batch:
                item.status = 0 
                item.save(using='card')

#            elif status == -1:             
#                card_batch.status = 0
#                card_batch.save(using='card')
#            elif status == 2:
#                key = card_batch.key
#                Card._meta.db_table = 'card_%s'%key
#                Card.objects.using('card').extra(where=["status = 1"]).delete()                     
        except Exception, e:
            print('del batch error:', e)
    else:
        return HttpResponse("id不能为空！")
    return render_to_response('feedback.html')

def batch_recover(request):
    ids = request.GET.get('ids','0')
    if ids != '':
        try:
            card_batch = CardBatch.objects.using('card').filter(id__in = ids.split(','))
            for item in card_batch:
                item.status = 1 
                item.save(using='card')

#            elif status == -1:             
#                card_batch.status = 0
#                card_batch.save(using='card')
#            elif status == 2:
#                key = card_batch.key
#                Card._meta.db_table = 'card_%s'%key
#                Card.objects.using('card').extra(where=["status = 1"]).delete()                     
        except Exception, e:
            print('recover batch error:', e)
    else:
        return HttpResponse("id不能为空！")
    return render_to_response('feedback.html')
