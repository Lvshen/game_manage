#! /usr/bin/python
# -*- coding: utf-8 -*-

from GameManage.models.gm import GMDefine
from GameManage.http import http_post
import json, time, datetime, shutil
from django.shortcuts import render_to_response
from django.http import HttpResponse
from GameManage.views.game.base import write_gm_log
from GameManage.views.base import save_log
from GameManage.views.base import UserStateManager
from GameManage.models.center import Server
from GameManage.cache import center_cache
from os.path import getsize
def gm(request, model_id=0):
    model_id = int(model_id)
    form_key = request.GET.get('form_key', '')
    form_type = request.GET.get('form_type', '')
    desc = request.POST.get('gm_desc', request.GET.get('gm_desc', ''))#备注
    from_id = request.GET.get('from_id', '')#提交来自哪个 gm_def 的id
    is_ajax = int(request.GET.get('ajax', request.POST.get('ajax', 0)))#用什么模板渲染，目前只用于ajax 提交 gm_form.html 中的批量服务器保存
    parg = {}
    if 0 == model_id:
        model_id = int(request.GET.get('id'))
     
    err_msg = ''
    gm_def = GMDefine.objects.get(id = model_id)
    plugin_list = []
    
    try:
        plugin_list = json.loads(gm_def.description)
    except Exception, ex:
        pass
    parg["plugin_list"] = plugin_list
    nemu_list = []
    if None != gm_def.flag and '' != gm_def.flag:
        nemu_list = GMDefine.objects.filter(flag=gm_def.flag) 
    
    result_def = json.loads(gm_def.result_define)
    
    code_path = result_def.get('code_path', 'code')
    content_path =  result_def.get('content_path', 'content')
    reason_phrase_path = result_def.get('reason_phrase_path', 'reason_phrase')
    
    def_params = json.loads(gm_def.params)
    
    
    template = 'game/gm_%s.html' % gm_def.result_type
    
    if def_params.get('req_type', '') == '':
        return HttpResponse(u"缺少协议参数req_type")
    
    req_type = def_params.get('req_type').get('value')
    req_params = '&req_type=%s' % req_type
    
    
    #参数处理
    lost_param_list = []
    has_value_param_list = []
    json_param = {}
    postback_param = []
    has_lost_server_id = False
    has_server_id = False
    
    usm = UserStateManager(request)
    is_root = usm.current_userRole_is_root()
    user_server_id_list = []
    if not is_root:
        user_server_list = center_cache.get_user_server_list(usm.get_the_user())
        user_server_id_list = [str(item.id) for item in user_server_list]
    
    group_server_list = []
    for p_name in def_params: 
        
        if p_name == 'req_type':
            continue
        
        input_value = request.GET.get(p_name, '')
        p_info = def_params[p_name]
        if input_value == '':
            input_value = request.POST.get(p_name, '')
        
        if not is_root and p_name == 'server_id' and '' != input_value:
            if input_value not in user_server_id_list:
                return HttpResponse('没有权限')
        
        value_type = p_info.get('type')
        default_value = p_info.get('value', '')
        if '' != input_value:
            try:
                if 'boolean' == value_type:
                    input_value = bool(int(input_value))
                if 'int' == value_type:
                    input_value = int(input_value)
                if 'float' == value_type:
                    input_value = float(input_value) 
                
            except:
                print 'value type error: ', (p_name, value_type, input_value)
                input_value = ''
        
        default_value = p_info.get('value', '')
        try:
            if '' != default_value:
                if 'boolean' == value_type:
                    if 'False' == default_value: 
                        default_value = False
                    if 'True' == default_value:
                        default_value = True
                    default_value = bool(default_value)
                if 'int' == value_type:
                    default_value = int(default_value)
                if 'float' == default_value:
                    default_value = float(default_value)
        except:
            pass
        
        p_info['value'] = default_value 
        required = int(p_info.get('required', 1))
        if input_value == '' and required:
            if p_name == 'server_id':
                has_lost_server_id = True 
                group_server_list = get_group_server_list(is_root)
            else:
                value_map = p_info.get('value_map', '')
                
                value_map_array = ''
                if '' != value_map:
                    value_map = json.loads(value_map)
                    try:
                        if type(value_map) == dict:
                            value_map_array = [{"key":key, "value":value} for key, value in value_map.items()]
                        else:
                            value_map_array = []
                            for item in value_map:
                                item = item.items()
                                value_map_array.append({"key":item[0][0], "value":item[0][1]}) 
                             
                    except Exception, ex:
                        print ex
                        pass
                            
                    
                lost_param_list.append({'key':p_name, 'value':p_info, 'value_map':value_map_array})
        else:
            has_value_param_list.append({'key':p_name, 'value':input_value})
        
        
        if p_name == 'server_id' and required:
            has_server_id = True
            
        if 'get' == p_info.get('method', 'get').lower():
            #组装外部参数
            req_params += '&%s=%s' % (p_name, input_value)
        else:
            param_name = p_info.get('json_name', 'content')
            if '' == param_name:
                param_name = "content"
            param_item = json_param.get(param_name, {})
            param_item[p_name] = input_value
            json_param[param_name] = param_item
        
        #处理回发（重用参数）
        if 1 == int(p_info.get('postback', 0)):
            postback_param.append({'key':p_name, 'value':input_value})
            
    parg['is_root'] = is_root
    #缺少参数则返回页面让用户输入
    if 0 != lost_param_list.__len__() or has_lost_server_id:
        print lost_param_list
        parg['lost_param_list'] = lost_param_list
        parg['has_value_param_list'] = has_value_param_list
        parg['has_lost_server_id'] = has_lost_server_id
        
        if 0 == len(group_server_list):
            group_server_list = get_group_server_list(is_root) 
        
        parg['group_server_list'] = group_server_list
        parg['gm_def'] = gm_def
        parg['system_timestamp'] = int(time.time())
        return render_to_response('game/gm_post.html', parg)
    
    from_gm_def_form_items = None
    if '' != from_id:
        from_id = int(from_id)
        from_gm_def = GMDefine.objects.get(id = from_id)
        from_gm_def_form_items = json.loads(from_gm_def.result_define).get('form_items', {})
    
    if form_type == 'json' and form_key == '':
        form_key = 'content'
    
    if form_key != '': 
        if form_type == 'json':
            post_param = json_param.get(form_key, {})
            for post_item in request.POST:
                if 'server_id' == post_item:
                    continue
                if '' == post_item:
                    continue
                value = request.POST.get(post_item, '')
                if None != from_gm_def_form_items:
                    attr_cfg = from_gm_def_form_items.get(post_item, {})
                    attr_type = attr_cfg.get('type', 'text')
                    if attr_type == 'number':
                        value = float(value)
                    elif attr_type in ['array', 'json']:
                        value = json.loads(value)
                    elif attr_type == 'timestamp':
                        try:
                            value = int(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').timetuple()))
                        except Exception, ex:
                            value = None
                            print ex
                    elif value_type == 'int':
                        try:
                            value = int(value)
                        except:
                            pass
                if None != value:    
                    post_param[post_item] = value 
            json_param[form_key] = post_param
    
    
    
    #如果有server_id 取服务器JSON配置中的 GM协议地址
    if has_server_id:
        
        #以下POST一定要优先GET取， 因为form方式如果批量提交修改到各个服务器表单提交过来的server_id 是用POST 方式
        server_id = int(request.POST.get('server_id', 0))
        if 0 == server_id:
            server_id = int(request.GET.get('server_id', 0))
        parg['server_id'] = server_id
        server_item = Server.objects.get(id = server_id)
        server_cfg = {}
        try:
            server_cfg = json.loads(server_item.json_data)
        except:
            pass
        
        #过滤url 中有 server_id 的。 批量修改post 中的 server_id 要替代  url中的值
        if -1 != req_params.find('server_id'): 
            param_list = req_params.split('&')
            new_url = req_params[0]
            for item in param_list:
                tmp = item.split('=')
                if tmp.__len__() != 2:
                    continue
                name = tmp[0].strip()
                value = tmp[1].strip()
                if 'server_id' == name:
                    value = server_id
                
                new_url = '%s&%s=%s' % (new_url, name, value) 
                
                    
            req_params = new_url
        gm_def.url = server_cfg.get('gm_url', gm_def.url)
    
    
    #组装内部参数(JSON格式参数)
    for key, value in json_param.items():
        req_params += '&%s=%s' % (key, json.dumps(value))
        
    #参数处理完毕
    
    req_params = req_params.encode('utf-8')
    print '***************gm -log*******************'
    print u'request param::::', req_params
    result_json_str = ''
    try:
        #gm_def.url = 'http://203.195.147.115:8082/gm' 
        #req_params = 'req_type=obtainquestionlist&server_id=1&secure_key=le1dou'
        result_json_str = http_post(gm_def.url, req_params, timeout_param=120)
        fb = None
        try:
            now = datetime.datetime.now()
            log_path = '/data/gm.log'
            if getsize(log_path) > 3010632:
                shutil.move(log_path, '/data/gm_%s.log' % (now.strftime('%Y-%m-%d_%H-%M-%S')))
            fb = open('/data/gm.log', 'a')
            fb.write('========================[%s]===========================\n' % now.strftime('%m-%d %H:%M:%S'))
            fb.write('REQUEST:\n')
            fb.write(gm_def.url)
            fb.write('\n')
            fb.write(req_params)
            fb.write('\n')
            fb.write('RESPONSE:\n')
            fb.write(result_json_str)
            fb.write('\n')
            fb.flush()
        except Exception, ex:
            print 'write gm log file error'
            print ex
        finally:
            if None != fb:
                fb.close()
    except Exception, ex:
        print 'http_post error'
        print ex
        err_msg = u'请求GM服务器出错,请检查请求url 或者提交参数是否正确'
    
    
    source_result_json_str = result_json_str
    try:
        result_json_str = result_json_str.decode('utf-8')
    except:
        print '<views.game.gm> warring: result decode utf-8 fail'
        result_json_str = source_result_json_str
    
    
    #print u'result_json::::', result_json_str
    #print '*****************************************'
    
    try:
        #写日志 
        log_req_params = req_params
        log_data_result = result_json_str
        write_gm_log(request,  [req_type, 0, 0, 0,u'协议:%s 返回代码:%s  URL:%s  参数:%s' % (req_type, log_data_result, gm_def.url, log_req_params)])
    except Exception, ex:
        print 'write gm log error'
        print ex
    
    result = ''
    if '' == err_msg and '' != result_json_str:
    #    if True:
        try: 
            result_json = json.loads(result_json_str)
            result_code = result_json
             
            try:
                for path_item in code_path:
                    result_code = result_code[path_item]
            except Exception, ex:
                print ex
                err_msg = u'配置状态码路径错误'
                result_code = '-99' 
            try:
                reason_phrase =  result_json
                for path_item in reason_phrase_path:
                    reason_phrase = reason_phrase[path_item]
            except:
                err_msg = u'reason_phrase 配置路径错误' 
            if result_code != '0' and result_code != 0:
                err_msg = u'出错,服务端返回状态码:%s, 原因:%s' % (result_code, reason_phrase)
            else:
                content_json = result_json 
                try:
                    for path_item in content_path: 
                        content_json = content_json[path_item]
                except Exception, ex:
                    print ex
                    err_msg = u'内容路径填写错误' 
                if '' == err_msg:
                    if reason_phrase == '':
                        reason_phrase = '非法请求'
                    result = get_result(content_json, reason_phrase, gm_def, result_code, usm)
                    try:
                        save_desc(request, req_type, result_def, desc)
                    except Exception, ex:
                        print 'save gm remark error' 
                        print ex
                    
        except Exception, ex:
            print ex
            err_msg = u'错误:%s' % ex
    else:
        err_msg = u'GM工具返回为空'
     
    parg['title'] = gm_def.title
    parg['id'] = gm_def.id
    parg['result'] = result
    parg['err_msg'] = err_msg
    parg['system_timestamp'] = int(time.time())
    parg['postback_param'] = postback_param
    parg['nemu_list'] = nemu_list
    parg['now_time_str'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if is_ajax and 'msg' == gm_def.result_type:
        if result == '' and err_msg != '':
            result = err_msg
        return HttpResponse(result)
    return render_to_response(template, parg)

#保存备注信息
def save_desc(request, req_type, result_def, desc):
    if desc.strip() == '':
        return
    desc_field_map = result_def.get('desc_field_map', None)
    log_server = 0
    log_channel = 0
    log_user = 0
    log_data = 0
    log_result = 0
    f1=''
    f2=''
    f3=''
    f4=''
    f5=''
    if isinstance(desc_field_map, dict):
        log_server_map = desc_field_map.get('log_server', '')
        print 'desc_field_map', desc_field_map
        print 'log_server:', log_server_map
        log_channel_map = desc_field_map.get('log_channel', '')
        log_user_map = desc_field_map.get('log_user', '')
        log_data_map = desc_field_map.get('log_data', '')
        log_result_map = desc_field_map.get('log_result', '')
        f1_map = desc_field_map.get('f1', '')
        f2_map = desc_field_map.get('f2', '')
        f3_map = desc_field_map.get('f3', '')
        f4_map = desc_field_map.get('f4', '')
        f5_map = desc_field_map.get('f5', '')
        try:
            log_server = int(get_argument(request, log_server_map, 0))
            print 'value:', log_server
            log_channel = int(get_argument(request, log_channel_map, 0))
            log_user = int(get_argument(request, log_user_map, 0))
            log_data = int(get_argument(request, log_data_map, 0))
            log_result = int(get_argument(request, log_result_map, 0))
            f1 = get_argument(request, f1_map, '')
            f2 = get_argument(request, f2_map, '')
            f3 = get_argument(request, f3_map, '')
            f4 = get_argument(request, f4_map, '')
            f5 = get_argument(request, f5_map, '')
        except Exception, ex:
            print ex
    
    save_log('gm_desc', req_type, log_server, log_channel, log_user, log_data, log_result, f1 , f2, f3, f4, f5, desc)

def get_argument(request, name, default):
    return request.GET.get(name, request.POST.get(name, default))

def get_group_server_list(is_root):
    group_server_list = []
    group_list = center_cache.get_group_list()
    if is_root:
        for group in group_list:
            server_list = center_cache.get_group_server_list(group.id)
            group_server_list.append({'group':group, 'server_list':server_list})
    else:
        from GameManage.models import Group 
        tmp_group = Group()
        tmp_group.id = 99
        tmp_group.name = '服务器'
        group_server_list.append({'group':tmp_group, 'server_list': center_cache.get_user_server_list(usm.get_the_user())})
        
    return group_server_list

class FormItem(object):
    def __init__(self, key ,is_modify, is_append, value, enum, attr_type):
        self.key = key
        self.name = ''
        self.is_modify = is_modify
        self.is_append = is_append
        self.value = value
        self.enum = enum
        self.attr_type = attr_type
    
    def get_value(self):
        if '' != self.enum and None != self.enum and {} != self.enum:
            return self.enum.get(self.value, self.value) 
        
        value_type = self.attr_type
        if value_type in ['text', 'textarea']:
            return self.value
         
        if value_type in ['json', 'array']:
            result = json.dumps(self.value)
            
            result_type = type(self.value)
            
            if dict != result_type and list != result_type:
                if value_type == 'json':
                    return {}
                else:
                    return []
            return result

        if 'boolean' == value_type:
            if self.value:
                return 'true'
            else:
                return 'false'
        
        if 'timestamp' == value_type:
            return datetime.datetime.fromtimestamp(self.value).strftime('%Y-%m-%d %H:%M:%S')
        
        return self.value
        

def get_result(content_json, reason_phrase, gm_def, result_code, usm):
    result = None  
    result_def = json.loads(gm_def.result_define)
    if gm_def.result_type == 'json_result':
        result = {}
        result['content_json'] = json.dumps(content_json)
    
    elif gm_def.result_type == 'msg':
        result = result_def.get('msg_values',{})
        #print '-==============================='
        #print result
        #print result.get(str(content_json))
        result = result.get(str(content_json), u'错误,错误码:%s' % content_json)
    elif gm_def.result_type == 'form':
        
        list_infos = [] 
        
        form_items = result_def['form_items']
        
        form_items_list = []
        for key, value in form_items.items():
            #print key
            form_items_list.append({'key': key,'json':value})
        form_items = form_items_list
        
        form_items.sort(cmp=lambda x,y:cmp(x['json'].get('order', 0), y['json'].get('order', 0)))
        
        for _item in form_items:
            key = _item.get('key')
            def_item = _item.get('json')
            allow_empty = def_item.get('allow_empty', 0)
            has_value = False
            content_json_type = type(content_json)
            if dict == content_json_type:
                for r_key, value in content_json.items():
                    if key != r_key:
                        continue
                    has_value = True
                    item = FormItem(key, False, False, value, {}, 'text')
                    item.name = def_item.get('name', key) 
                    item.is_modify = def_item.get('is_modify', False)
                    item.is_textarea = def_item.get('is_textarea', False)
                    item.is_append = def_item.get('is_append', False)
                    item.attr_type = def_item.get('type', 'text')
                    item.enum =  def_item.get('enum', {})
    
                    list_infos.append(item)
            elif list == content_json_type:
                item = FormItem(key, False, False, value, {}, 'text')
                item.name = def_item.get('name', key) 
                item.is_modify = def_item.get('is_modify', False)
                item.is_textarea = def_item.get('is_textarea', False)
                item.is_append = def_item.get('is_append', False)
                item.attr_type = def_item.get('type', 'text')
                item.enum =  def_item.get('enum', {})
                item.value = json.dumps(content_json)
                list_infos.append(item)
                
            if not has_value and allow_empty:
                
                 
                item = FormItem(key, False, False, '', {}, 'text')
                item.name = def_item.get('name', key) 
                item.is_modify = def_item.get('is_modify', False)
                item.is_textarea = def_item.get('is_textarea', False)
                item.is_append = def_item.get('is_append', False)
                item.attr_type = def_item.get('type', 'text')
                item.enum =  def_item.get('enum', {})
                
                list_infos.append(item)
        
        result = {}
        result['form_action'] = result_def.get('form_action', '')
        result['form_type'] = result_def.get('form_type', '') 
        result['form_key'] =  result_def.get('form_key', '')
        
        server_list_chkbox = result_def.get('server_list_chkbox', False)
        
        if server_list_chkbox:
            
            group_server_dic = {}
            if usm.current_userRole_is_root():
                group_list = center_cache.get_group_list()
                for item in group_list:
                    group_server_dic[item.name] = center_cache.get_server_list(item.id)
            else:
                group_server_dic['服务器'] = center_cache.get_user_server_list(usm.get_the_user())
            
            result['group_server_dic'] = group_server_dic
            
        result['server_list_chkbox'] = server_list_chkbox
        result['list_infos'] = list_infos
        
    elif gm_def.result_type == 'list':
        list_items_def = result_def.get('list_items', {})
        list_action = result_def.get('action', [])
        
        #排序
        #先转数组 
        
        field_array = []
        for key, value in list_items_def.items():
            
            field_array.append({"key":key, "json":value}) 
        #排序  
        try:
            field_array.sort(cmp=lambda x,y:cmp(x['json'].get('order', 0), y['json'].get('order', 0)))
        except Exception, ex:
            print ex
        list_data  = []
        if list != type(content_json):
            try:
                print content_json
                content_json = json.loads(content_json)
            except Exception, ex:
                print 'get_reult type is list json loads error:'
                print ex
                content_json = []
        try:
            #每一行
            for item in content_json:
                row = {}
                
                field_dic = {}
                cells = []
                #每个字段
                for field_def in field_array:
                    key = field_def.get('key', '')
                    json_item = field_def.get('json', {})
                    value = item.get(key, '')
                    field_dic[key] = value
                    if type(json_item) == dict:
                        value_type = json_item.get('type', 'text')
                        if value_type == 'number':
                            value = float(value)
                        elif value_type in ['array', 'json']:
                            try:
                                value = json.loads(value)
                            except:
                                pass
                        elif value_type == 'timestamp':
                            try:
                                value = int(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').timetuple()))
                            except Exception, ex:
                                print ex
                        elif value_type == 'int':
                            try:
                                value = int(value)
                            except:
                                pass
                    cells.append(value)
                 
                action_url = ''
                links = []
                for action in list_action:
                    action_title = action.get('title', '')
                    action_url = action.get('form_action', '')
                     
                    param_list = action.get('param_list', []) 
                    #print param_list
                    tmp_f = '?' 
                    for param in param_list:
                        param_name = param.get('param_name', '')
                        if '' == param_name:
                            continue
                        value_source = param.get('value_source', '')
                        value = field_dic[value_source]
                        if '' == param_name or '' == value_source:
                            continue
                        #print (action_url, tmp_f, value)
                        action_url = '%s%s%s=%s' % (action_url, tmp_f, param_name ,value)
                        tmp_f = '&'
                         
                    links.append({"title":action_title, 'link':action_url})
                
                row['cells'] = cells
                row['links'] = links
                
                list_data.append(row)
        except Exception, ex:
            print 'append row error:'
            print ex
              
        result = {}
        result['list_data'] = list_data
        result['list_field'] = field_array
    return result
         
        
        
