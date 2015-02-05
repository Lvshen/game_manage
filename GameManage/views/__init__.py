#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from GameManage.models.admin import Admin, Role
from GameManage.views.system.admin_status import admin_status 
from django.http import HttpResponseRedirect
import datetime, time
 

def index(request):
    the_user_id = int(request.session.get('userid', '0'))
    if the_user_id == 0:
        return HttpResponseRedirect("login")
    the_user = Admin.objects.using('read').get(id=the_user_id)  
    
    return render_to_response('index.html', locals())

def index_block(request):
    
    return render_to_response('block.html', locals())


def login(request):
    username = request.COOKIES.get('username', '')
    return render_to_response('login.html', {'model':{'username':username}})

def login_do(request):
    tmp_admin = Admin()
    tmp_admin.username = request.POST.get('username', '')
    tmp_admin.password = request.POST.get('password', '')
    template_name = 'login.html'
    err_msg = ''
    
    now = datetime.datetime.now() 
    if tmp_admin.username != "" and tmp_admin.password != "":
        list_admin = Admin.objects.filter(username=tmp_admin.username, status=admin_status.NORMAL)
        the_admin = None
        if list_admin.__len__() == 0:
            if tmp_admin.username != 'root':
                err_msg = u'账号不存在! %s ' % tmp_admin.username
                return render_to_response(template_name, {'model':tmp_admin, 'err_msg':err_msg})
            else:    
                if 0 == Admin.objects.count():
                    if 0 == Role.objects.count():
                        role = Role()
                        role.name = 'root'
                        tmp_admin.role = role
                    else:
                        tmp_admin.role = Role.objects.all()[0]
                    
                    tmp_admin.password = tmp_admin.md5_password()
                    tmp_admin.last_time = now
                    tmp_admin.lock_time = now
                    tmp_admin.status = 0
                    tmp_admin.login_count = 0
                    tmp_admin.save()
                    the_admin = tmp_admin
        else:
            the_admin = list_admin[0]
        
        the_admin.last_time = now
        
        if the_admin.lock_time != None and the_admin.lock_time > now:
            err_msg = u'账号已被锁定至: %s 解锁' % the_admin.lock_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            if the_admin.password == tmp_admin.md5_password():
                request.session["userid"] = the_admin.id
                request.COOKIES["username"] = the_admin.username
                request.session["key"] = tmp_admin.md5_password()
                the_admin.login_count = 0
                the_admin.save()
                return HttpResponseRedirect("/index")
            else:
                err_msg = u'账号或密码错误! %s | %s' % (the_admin.password, tmp_admin.md5_password())
                #累加login_count
                login_count = the_admin.login_count
                if login_count == None:
                    login_count = 0
                login_count = login_count + 1
                the_admin.login_count = login_count
                
                max_count = 5
                if login_count < max_count and login_count >= 3:
                    err_msg = '密码错误,还有%d次登陆机会后账号锁定。' % (max_count - login_count)
                 
                #错误登陆超过5次
                if login_count >= max_count: 
                    date = now + datetime.timedelta(minutes=30) 
                    the_admin.lock_time = date
                    err_msg = u'账号已被锁定至: %s 解锁' % the_admin.lock_time.strftime('%Y-%m-%d %H:%M:%S')
                    #清空累计
                    the_admin.login_count = 0
            
                the_admin.save()
                 
                
    else:
        err_msg = u'账号或密码不能为空!'

    return render_to_response(template_name, {'model':tmp_admin, 'err_msg':err_msg})


def logout(request):
    request.session.clear()
    return HttpResponseRedirect("/login")
