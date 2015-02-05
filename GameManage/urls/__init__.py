# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from game_manage import settings

urlpatterns = patterns('',
    url(r'^index$', 'GameManage.views.index'),
    url(r'^block$', 'GameManage.views.index_block'),

    url(r'^login$', 'GameManage.views.login'),
    url(r'^login/do$', 'GameManage.views.login_do'),
    url(r'^logout$', 'GameManage.views.logout'),
    
    url(r'^menu/script$', 'GameManage.views.system.menu.menu_script'),
    url(r'^menu/list', 'GameManage.views.system.menu.menu_list'),
    url(r'^menu/edit/(\d+)/(\d+)$', 'GameManage.views.system.menu.menu_edit'),
    url(r'^menu/edit/(\d+)$', 'GameManage.views.system.menu.menu_edit'),
    url(r'^menu/edit$', 'GameManage.views.system.menu.menu_edit'),
    url(r'^menu/save/(\d+)/(\d+)$', 'GameManage.views.system.menu.menu_save'),
    url(r'^menu/save/(\d+)$', 'GameManage.views.system.menu.menu_save'),
    url(r'^menu/save$', 'GameManage.views.system.menu.menu_save'),
    url(r'^menu/remove/(\d+)$', 'GameManage.views.system.menu.menu_remove'),
    url(r'^menu/remove$', 'GameManage.views.system.menu.menu_remove'),

    url(r'^role/list', 'GameManage.views.system.role.role_list'),
    url(r'^role/edit/(\d+)$', 'GameManage.views.system.role.role_edit'),
    url(r'^role/edit$', 'GameManage.views.system.role.role_edit'),
    url(r'^role/save/(\d+)$', 'GameManage.views.system.role.role_save'),
    url(r'^role/save$', 'GameManage.views.system.role.role_save'),
    url(r'^role/remove/(\d+)$', 'GameManage.views.system.role.role_remove'),
    url(r'^role/remove$', 'GameManage.views.system.role.role_remove'),


    url(r'^admin_user/list$', 'GameManage.views.system.admin.admin_list'),
    url(r'^admin_user/edit/(\d+)$', 'GameManage.views.system.admin.admin_edit'),
    url(r'^admin_user/edit$', 'GameManage.views.system.admin.admin_edit'),
    url(r'^admin_user/save/(\d+)$', 'GameManage.views.system.admin.admin_save'),
    url(r'^admin_user/save$', 'GameManage.views.system.admin.admin_save'),
    url(r'^admin_user/remove/(\d+)$', 'GameManage.views.system.admin.admin_remove'),
    url(r'^admin_user/remove$', 'GameManage.views.system.admin.admin_remove'),
    url(r'^admin_user/set/(\d+)$', 'GameManage.views.system.admin.admin_set'),
    url(r'^admin_user/change_password/do$', 'GameManage.views.system.admin.change_password_do'),
    url(r'^admin_user/change_password$', 'GameManage.views.system.admin.change_password'), 
    url(r'^admin_user/unlock$', 'GameManage.views.system.admin.unlock'),
    
    url(r'^coc/', include('GameManage.urls.coc')),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}), 
)
