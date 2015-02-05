#coding=utf-8
# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from GameManage.models.card import Card,CardBatch,CardLog
from GameManage.models.center import Server,Group
import datetime,time
import random
from GameManage.views.base import UserStateManager
from GameManage.views.log.exprot_file import QueryExprot
from django.db import connections
import re
from GameManage.views.base import get_server_list
from GameManage.views.card.batch import group_ajax
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    
#新手卡列表
def card_list(request):
    msg = ''
    batch_id = int(request.GET.get('batch_id', '0'))
    page_num = int(request.GET.get('page_num', '1'))    
    if page_num < 1:
        page_num = 1 
    page_num = int(request.GET.get('page_num', '1'))
    page_size = 15   
    list_data = []    
    search_type = int(request.GET.get('search_type','0'))
    status = request.GET.get('status','')
    
    sdate = request.GET.get('start_date','')
    edate = request.GET.get('end_date','')
    
    search_val = request.GET.get('search_val','')
    query = ['1=1']
    total_record = 0
    card_batch = None
    list_server = get_server_list()
    server_id = int(request.GET.get('server_id','0'))
    if batch_id > 0:
        query.append(" and batch_id = '%s'"%batch_id)
        try:
            card_batch = CardBatch.objects.using('card').get(id = batch_id)
            key = card_batch.key
            Card._meta.db_table = 'card_%s'%key
            if search_type != 0 and search_val !='':
                if search_type == 1:
                    query.append(" and number = '%s'"%search_val)
                elif search_type == 2:
                    query.append(" and player_id = '%s'"%search_val)
#                elif search_type == 3:
#                    query.append(" and password = '%s'"%search_val)                    
            if server_id != 0:
                query.append(" and server_id = %d "%server_id)
            if status != '':
                try:
                    status = int(status)
                    query.append(" and status = %d "%status)
                except:
                    pass
            if sdate != '' and edate != '':
                query.append(" AND DATE(`use_time`) >= '%s' AND DATE(`use_time`) <= '%s'"%(sdate,edate))
            total_record = Card.objects.using('card').extra(where=[''.join(query)]).count()
            if total_record > 0:
                list_data = Card.objects.using('card').extra(where=[''.join(query)]).order_by('-id')[(page_num - 1) * page_size:page_num * page_size]
                for item in list_data:
                    item.server = ''
                    if item.server_id:
                        the_server = Server.objects.get(id = item.server_id)
                        if the_server:
                            item.server = the_server.name
        except Exception, e:
            print('create card number error:', e)   
            msg = '%s'%e        
    usm = UserStateManager(request)
    parg = {} 
    parg["usm"] = usm
    parg['page_num'] = page_num
    parg['page_size'] = page_size
    parg['total_record'] = total_record
    parg['msg']  = msg 
    parg['list_data'] = list_data
    parg['card_batch'] = card_batch
    parg['search_type'] = search_type
    parg['search_val'] = search_val
    parg['batch_id'] = batch_id
    parg['list_server'] = list_server
    parg['server_id'] = server_id
    parg['status'] = status
    parg['sdate'] = sdate
    parg['edate'] = edate
    return render_to_response('card/card_list.html', parg)

#礼包卡列表
def card_log_list(request):
    exprot = int(request.GET.get('exprot', '0'))
    close_export = int(request.GET.get('close_export', '0'))
    clear_export_old_file = int(request.GET.get('clear_export_old_file', '0'))
        
    msg = ''
    batch_id = int(request.GET.get('batch_id', '0'))
    page_num = int(request.GET.get('page_num', '1'))    
    if page_num < 1:
        page_num = 1 
    page_size = 15  
    if exprot > 0:
        page_size = 500     
    list_data = []    
    search_type = int(request.GET.get('search_type','0'))
    search_val = request.GET.get('search_val','')
    status = request.GET.get('status','')
    now = datetime.datetime.now()
    sdate = request.GET.get('start_date',now.strftime("%Y-%m-01 00:00:00"))
    edate = request.GET.get('end_date',now.strftime("%Y-%m-%d %H:%M:%S"))    
    query = ['1=1']
    total_record = 0
    group = int(request.GET.get('group','0')) 
    list_group = Group.objects.all()
    if 0 != group:
        try:
            list_server = Group.objects.get(id = group).server.all()
        except:
            list_server = None
            pass
    else:
        list_server = get_server_list() 
    server_id = int(request.GET.get('server_id','0'))
    if batch_id > 0:
        query.append(" and card_key = '%s'"%batch_id)
    try:
        if search_type != 0 and search_val !='':
            if search_type == 1:
                query.append(" and `number` = '%s'"%search_val)
            elif search_type == 2:
                query.append(" and `player_id` = '%s'"%search_val)
            elif search_type == 3:
                query.append(" and `card_key` = '%s'"%search_val)
            elif search_type == 4:
                query.append(" and `id` = %d "% int(search_val)) 
            elif search_type == 5:
                query.append(" and `card_name` like '%s%s%s'"%('%%',search_val,'%%'))
#                elif search_type == 3:
#                    query.append(" and password = '%s'"%search_val) 
        if status != '':
            query.append(" and `status` = %d " % int(status))

        if sdate != '' and edate != '':
            query.append(" AND `create_time` >= '%s' AND `create_time` <= '%s'"%(sdate,edate))
                        
        if server_id != 0:
            query.append(" and server_id = %d "%server_id)
        elif group != 0:
            query_server_id = []
            for server_item in list_server:
                query_server_id.append(int(server_item.id))
            if len(query_server_id) != 0:
                query_server_id = tuple(query_server_id)
                query.append(" and `server_id` in %s "%str(query_server_id))
            else:
                query.append(" and 0 ")  
        total_record = CardLog.objects.using('card').extra(where=[''.join(query)]).count()
        if total_record > 0:
            list_data = CardLog.objects.using('card').extra(where=[''.join(query)]).order_by('-id')[(page_num - 1) * page_size:page_num * page_size]
            
            for item in list_data:
                item.server = ''
                if item.server_id:
                    the_server = Server.objects.get(id = item.server_id)
                    if the_server:
                        item.server = the_server.name
        #处理 导出文件
        if 0< exprot: 
            export_data = []
            fields = [u'礼包ID',u'礼包卡名',u'礼包卡号',u'礼包卡标识',u'使用时间',u'奖励内容',u'角色ID',u'服务器',u'奖励状态']
            try:
                for item in list_data:
                    export_data.append([item.id,item.card_name, item.number, item.card_key, item.create_time_str(), item.get_prize_content(), item.player_id, item.server_name(), item.get_status_name()])
            except Exception,e:
                print 'error',e
            query_exprot = QueryExprot()
            #session ID 
            session_id = request.COOKIES.get('sessionid')
            pre_file_name = ''   
            if search_val != '':
                pre_file_name = '%s%s_'%(pre_file_name,search_val)
            if group != 0:
                try:
                    pre_file_name = '%s%s_'%(pre_file_name,Group.objects.get(id = group).name)
                except:
                    pass
            if server_id != 0:
                try:
                    pre_file_name = '%s%s_'%(pre_file_name,Server.objects.get(id = server_id).name)
                except:
                    pass                
            file_name = '%s%s_%s___%s'%(pre_file_name, sdate.replace("-","").replace(":","").replace(" ",""), edate.replace("-","").replace(":","").replace(" ",""), session_id)
            return query_exprot.gene_file(export_data, fields, file_name, page_num, page_size, total_record, exprot, close_export, clear_export_old_file, session_id)
                         
    except Exception, e:
        print('search CardLog error:', e)   
        msg = '%s'%e        
    usm = UserStateManager(request)
    parg = {} 
    parg["usm"] = usm
    parg['page_num'] = page_num
    parg['page_size'] = page_size
    parg['total_record'] = total_record
    parg['msg']  = msg 
    parg['list_data'] = list_data
    parg['search_type'] = search_type
    parg['search_val'] = search_val
    parg['batch_id'] = batch_id
    parg['list_server'] = list_server
    parg['server_id'] = server_id
    parg['status'] = status
    parg['list_group'] = list_group
    parg['group'] = group
    parg['sdate'] = sdate
    parg['edate'] = edate    
    return render_to_response('card/card_log_list.html', parg)

def check_card(card_no):
    if get_verifCode(card_no[:-1]) == card_no[-1]:
        return True
    else:
        return False
'''
0    卡号验证成功
-1    未知错误
1    卡号验证失败
2    卡已被使用
3    卡已超过有效期
4    该卡不能在此运营商使用
5    该卡不能在这个服务器使用
6    该类卡你已经不能再用 禁用
7    该类卡你已经不能再用 次数
'''
def card(request):
    code = 1
    card_no = request.POST.get('card_no','')
    server_id = request.POST.get('server_id','')
    channel_id = request.POST.get('channel_id','')
    player_id = request.POST.get('player_id','')
#    
#    card_no = request.GET.get('card_no','')
#    server_id = request.GET.get('server_id','')
#    channel_id = request.GET.get('channel_id','')
#    player_id = request.GET.get('player_id','')
        
    validate_card = ''  
    print 'card_no',card_no
    print 'server_id',server_id
    print 'player_id',player_id
    print 'channel_id',channel_id
    try:
        if server_id != '' and card_no != '' and player_id != '' and re.match('^\d+$', str(server_id)) and len(card_no) == 15:
            key = card_no[0:4]
            validate_card = check_card(card_no)
            print 'validate_card',validate_card
            if validate_card:
                Card._meta.db_table = 'card_%s'%key
                the_card = Card.objects.using('card').extra(where=["number = '%s' and status = 0"%card_no])
                if the_card:
                    the_card = the_card[0]
                    batch_id = the_card.batch.id
                    card_batch = CardBatch.objects.using('card').get(id = batch_id)
                    if card_batch.status == 0:
                        code = 6
                    else:
                        if card_batch.server != '':
                            server = card_batch.server.split(',')
                        else:
                            server = []
                            
                        if card_batch.channels != '':
                            channels = card_batch.channels.split(',')
                        else:
                            channels = []
                        current_unixtime = int(time.time())
                        start_time = int(time.mktime(card_batch.start_time.timetuple()))
                        end_time = int(time.mktime(card_batch.end_time.timetuple()))
                        limit_count = card_batch.limit_count
                        
                        if current_unixtime < start_time or current_unixtime > end_time:
                            code = 3                        
                        elif server.__len__() > 0 and server_id not in server:
                            code = 5
                        elif channels.__len__() > 0 and channel_id not in channels:
                            code = 4
                        elif limit_count > 0:
                            validate_limit_count = CardLog.objects.using('card').filter(player_id = player_id, server_id = server_id, card_key = key).count()
                            if limit_count <= validate_limit_count:
                                code = 7                              
                        if code == 1:
                            code = 0
                            the_card.status = 2
                            the_card.use_time = datetime.datetime.now()
                            the_card.server_id = server_id
                            the_card.channel_key = channel_id
                            the_card.player_id = player_id
                            the_card.save(using='card')
                            
                            card_batch.used_count = card_batch.used_count + 1
                            card_batch.save(using='card')
                            
                            card_log = CardLog()
                            card_log.card_key = key
                            card_log.channel_key = channel_id
                            card_log.server_id = server_id
                            card_log.player_id = player_id
                            card_log.card_name = card_batch.name
                            card_log.number = card_no
                            card_log.prize = card_batch.prize
                            card_log.save(using='card')
                else:
                    code = 2
            else:
                code = 1
    except Exception,e:
        print 'check card error',e
        code = -1
    print code
    return HttpResponse(code)        


def get_verifCode(card_part):
    sum_value = 0
    for i in range(card_part.__len__()):
        if (i+1) % 2 == 0:
            if i < 9:
                sum_value += int(card_part[i]) * 2 % 10
            else:
                sum_value += ord(card_part[i]) * 2 % 23
        else:
            if i < 9:
                sum_value += int(card_part[i])
            else:
                sum_value += ord(card_part[i]) % 23
    chars = 'abcdefghjkmnpqrstuvwxyz'
    result_char = chars[sum_value % 23]
    return result_char

# 生成新手卡号
letter = 'abcdefghjkmnpqrstuvwxyz'
digit = '23456789' 
char = '%s%s'%(letter,digit)

def card_create(request):
    msg = ''
    card_count = int(request.GET.get('card_count','0'))
    batch_id = int(request.GET.get('batch_id','0'))
    record = int(request.GET.get('record','0'))
    #is_pwd = int(request.GET.get('is_pwd','0'))
    card_size = 2000
    
    if card_count < card_size:
        card_size = card_count
        
    if card_count - record < card_size:
        card_size = card_count - record
    
    is_finish = 0
    
    if card_count == record:
        is_finish = 1    
   
    if batch_id > 0 and card_count > 0 and card_size > 0 and is_finish == 0:
        try:
            card_batch = CardBatch.objects.using('card').get(id = batch_id)
            key = card_batch.key
            #card = Card()
            Card._meta.db_table = 'card_%s'%key
            card = Card()      
            card.batch_id = batch_id     
            
            conn = connections['card']
            cursor = conn.cursor()              
            if card_batch:
                insert_sql = []
                for i in range(0,card_size):
                    pre_number = '%s%s%s'%(key,''.join(random.sample(digit,5)),''.join(random.sample(letter,5)))
                    number = '%s%s'%(pre_number,get_verifCode(pre_number))
                    count_sql = "SELECT COUNT(*) FROM `card_%s` c WHERE c.`number` = '%s' "%(key,number)
                    cursor.execute(count_sql)
                    count = cursor.fetchone()
                    repeat_count = int(count[0])   
                    if repeat_count == 0:          
                        insert_sql.append("('%s','%s','%s')"%(batch_id,number,datetime.datetime.now()))
                        i = i + 1
                cursor.execute('INSERT INTO `card_%s`(`batch_id`,`number`,`add_time`) VALUES  %s'%(key, ','.join(insert_sql)))
                cursor.close()
                card_batch.total_count = card_batch.total_count + i
                card_batch.save(using='card')
                record = record + i
        except Exception, e:
            print('create card number error:', e)
            msg = '%s'%e
            
    return HttpResponse('{"is_finish":%d,"msg":"%s","record":"%s"}'%(is_finish,msg, record))             


def export_card(request): 
    page_size = 500
    clear_export_old_file = int(request.GET.get('clear_export_old_file', '0'))
    page_num = int(request.GET.get('page_num', '1'))    
    batch_id = int(request.GET.get('batch_id','0'))
    card_status = int(request.GET.get('card_status','0'))
    start_date = request.GET.get('start_date','')
    end_date = request.GET.get('end_date','')
    export = int(request.GET.get('export','2'))
    if page_num < 1:
        page_num = 1  
    fields = ''    
    #处理 导出文件
    if batch_id > 0 and export > 0: 
        try:
            select_sql = ''
            where_sql = ''
            card_data = []
            card_batch = CardBatch.objects.using('card').get(id = batch_id)
            key = card_batch.key     
            card_table = 'card_%s'%key  
            conn = connections['card']
            cursor = conn.cursor()
            fields = [u'卡号',u'使用状态']
            if card_status == 3:
                select_sql = ",IF(c.`status`=0,'未使用',IF(c.`status`=1,'已领取',IF(c.`status` = 2,'已使用','删除')))"
                where_sql = ''
            elif card_status == 0:
                where_sql = ' AND c.`status` = 0'
                select_sql = ",'未使用' "                    
            elif card_status == 1:
                where_sql = ' AND c.`status` = 1'
                select_sql = ",'已领取' "
            elif card_status == 2:
                where_sql = ' AND c.`status` = 2'
                select_sql = ",'已使用', c.`use_time`,c.`player_id`, c.`server_id` "
                fields = [u'卡号','使用状态',u'使用时间', u'角色ID', u'服务器']
                
            if start_date != '' and end_date != '':
                if card_status == 2:
                    where_sql += " AND c.`use_time` >= '%s' AND DATE(c.`use_time`) <= '%s'"%(start_date,end_date)
                else:
                    where_sql += " AND c.`add_time` >= '%s' AND DATE(c.`add_time`) <= '%s'"%(start_date,end_date)
                
            sql = "SELECT c.`number` %s FROM `%s` c WHERE 1=1 %s"%(select_sql,card_table,where_sql)
            count_sql = "SELECT COUNT(*) FROM (%s) a"%sql
            cursor.execute(count_sql)
            count = cursor.fetchone()
            total_record = int(count[0])       
            sql = "%s LIMIT %s,%s"%(sql,(page_num - 1) * page_size,page_size)    
            cursor.execute(sql)
            card_data = cursor.fetchall()
            if card_status == 2:
                new_data = []
                for item in card_data:
                    item = list(item)
                    if item[4]:
                        the_server = Server.objects.get(id = int(item[4]))
                        if the_server:
                            item[4] = the_server.name
                    new_data.append(item)
                card_data = new_data
            session_id = request.COOKIES.get('sessionid')                        
            query_exprot = QueryExprot()
            file_name = []
            if start_date == '' and end_date == '': 
                file_name.append(u'%s___%s___%s___%s%s'%(card_batch.name.strip(), card_batch.key, datetime.datetime.now().strftime("%Y%m%d"),card_batch.id,session_id))
            else:
                file_name.append(u'%s___%s___%s___%s_%s%s'%(card_batch.name.strip(), card_batch.key, start_date.replace("-","").replace("/",""),end_date.replace("-","").replace("/",""),card_batch.id,session_id))
            file_name = ''.join(file_name)
        except Exception,e:
            print 'export card error',e
        #session ID 
        return query_exprot.gene_file(card_data, fields, file_name, page_num, page_size, total_record, export, 0, clear_export_old_file, session_id)              
    return HttpResponse('导出出错！请重试！')    

def export_card_log(request): 
    page_size = 500
    clear_export_old_file = int(request.GET.get('clear_export_old_file', '0'))
    page_num = int(request.GET.get('page_num', '1'))    
    batch_id = int(request.GET.get('batch_id','0'))
    card_status = int(request.GET.get('card_status','0'))
    start_date = request.GET.get('start_date','')
    end_date = request.GET.get('end_date','')
    export = int(request.GET.get('export','2'))
    if page_num < 1:
        page_num = 1  
    fields = ''    
    #处理 导出文件
    if batch_id > 0 and export > 0: 
        try:
            select_sql = ''
            where_sql = ''
            card_data = []
            card_batch = CardBatch.objects.using('card').get(id = batch_id)
            key = card_batch.key     
            card_table = 'card_%s'%key  
            conn = connections['card']
            cursor = conn.cursor()
            fields = [u'卡号',u'使用状态']
            if card_status == 3:
                select_sql = ",IF(c.`status`=0,'未使用',IF(c.`status`=1,'已领取',IF(c.`status` = 2,'已使用','删除')))"
                where_sql = ''
            elif card_status == 0:
                where_sql = ' AND c.`status` = 0'
                select_sql = ",'未使用' "                    
            elif card_status == 1:
                where_sql = ' AND c.`status` = 1'
                select_sql = ",'已领取' "
            elif card_status == 2:
                where_sql = ' AND c.`status` = 2'
                select_sql = ",'已使用', c.`use_time`,c.`player_id`, c.`server_id` "
                fields = [u'卡号','使用状态',u'使用时间', u'角色ID', u'服务器']
                
            if start_date != '' and end_date != '':
                if card_status == 2:
                    where_sql += " AND c.`use_time` >= '%s' AND DATE(c.`use_time`) <= '%s'"%(start_date,end_date)
                else:
                    where_sql += " AND c.`add_time` >= '%s' AND DATE(c.`add_time`) <= '%s'"%(start_date,end_date)
                
            sql = "SELECT c.`number` %s FROM `%s` c WHERE 1=1 %s"%(select_sql,card_table,where_sql)
            count_sql = "SELECT COUNT(*) FROM (%s) a"%sql
            cursor.execute(count_sql)
            count = cursor.fetchone()
            total_record = int(count[0])       
            sql = "%s LIMIT %s,%s"%(sql,(page_num - 1) * page_size,page_size)    
            cursor.execute(sql)
            card_data = cursor.fetchall()
            if card_status == 2:
                new_data = []
                for item in card_data:
                    item = list(item)
                    if item[4]:
                        the_server = Server.objects.get(id = int(item[4]))
                        if the_server:
                            item[4] = the_server.name
                    new_data.append(item)
                card_data = new_data
            session_id = request.COOKIES.get('sessionid')                        
            query_exprot = QueryExprot()
            file_name = []
            if start_date == '' and end_date == '': 
                file_name.append(u'%s___%s___%s___%s%s'%(card_batch.name.strip(), card_batch.key, datetime.datetime.now().strftime("%Y%m%d"),card_batch.id,session_id))
            else:
                file_name.append(u'%s___%s___%s___%s_%s%s'%(card_batch.name.strip(), card_batch.key, start_date.replace("-","").replace("/",""),end_date.replace("-","").replace("/",""),card_batch.id,session_id))
            file_name = ''.join(file_name)
        except Exception,e:
            print 'export card error',e
        #session ID 
        return query_exprot.gene_file(card_data, fields, file_name, page_num, page_size, total_record, export, 0, clear_export_old_file, session_id)              
    return HttpResponse('导出出错！请重试！') 

# 删除新手卡号
def card_del(request):
    model_id = int(request.GET.get('id','0'))
    batch_id = int(request.GET.get('batch_id','0'))
    if model_id > 0 and batch_id > 0:
        try:
            card_batch = CardBatch.objects.using('card').get(id = batch_id)
            key = card_batch.key
            Card._meta.db_table = 'card_%s'%key 
            the_card = Card.objects.using('card').get(id=model_id)
            the_card.status = -1
            the_card.save(using='card')
            
        except Exception, e:
            print('update error:', e)
    else:
        return HttpResponse("操作有误！<a href='javascript:history.back();'>点击返回</a>")
    return render_to_response('feedback.html')

# 领取新手卡号
def card_get(request,batch='0',server_id=0):
    server_id = int(server_id)
    batch = int(batch)
    model_id = request.POST.get('id','')
    number = 0
    count = 0
    if batch == 0 and server_id == 0:
        server = Server.objects.filter(status__gt=1)
        return render_to_response('card/card_obtain.html',{'server':server})    
    elif 'id' in request.POST and request.POST['id']:
        model_id = int(model_id)
        card =Card.objects.filter(status=0,is_use=1,server_id=int(model_id),batch_id=batch)
        count = len(card)     
    elif batch == 0 and server_id > 0:
        card =Card.objects.filter(status=0,is_use=1,server_id=server_id)
        count = len(card)
    elif batch != 0:
        server = Card.objects.filter(batch_id=batch,is_use=1)
        server.query.group_by = ['server_id']
        server = server
        return render_to_response('card/card_get.html',{'server':server,'batch':batch})       
    if count:
        try:
            cid = card[0].id
            number = card[0].number
            c = Card.objects.get(id=int(cid))
            c.status = 1
            c.get_time = datetime.datetime.now()
            c.safe_save()
            return render_to_response('feedback.html')
        except Exception, e:
            print('update error:', e)        
            return HttpResponse("领取失败！<a href='javascript:history.back();'>返回</a>")
    else:
        return HttpResponse("卡号不足，领取失败！<a href='javascript:history.back();'>点击返回</a>")
    return HttpResponseRedirect('/card/list/?number=%s'%number)
    
# 使用新手卡号
def card_use(request):
    number = request.POST.get('number','')
    password = request.POST.get('password','')
    if number != '':
        #query = Card.objects.filter(number=number,password=password,status=1)
        query = Card.objects.filter(number=number,status=1,is_use=1)
        if query:
            c = Card.objects.get(number=number)
            if c.password != '' and c.password != password:
                return render_to_response('card/card_use.html',{'msg':'卡号或密码错误！'})
            c.status = 2
            c.use_time = datetime.datetime.now()
            c.safe_save()
            return render_to_response('feedback.html')
        else:
            return render_to_response('card/card_use.html',{'msg':'卡号有误'})
    else:
        return render_to_response('card/card_use.html')
