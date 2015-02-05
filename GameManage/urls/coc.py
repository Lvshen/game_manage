# -*- coding: utf-8 -*-
from  django.conf.urls import patterns, url 

urlpatterns = patterns('',
    url(r'^queryplayer/', 'GameManage.views.coc.gm.queryPlayer'),
    url(r'^queryplayerans/', 'GameManage.views.coc.gm.queryPlayerDataQeq'),
    url(r'^modified_player/','GameManage.views.coc.gm.modified_player'),
    url(r'^banplayer/','GameManage.views.coc.gm.banPlayer'),
    url(r'^banplayerans/', 'GameManage.views.coc.gm.banPlayerAns'),
    url(r'^unbanplayer/', 'GameManage.views.coc.gm.unbanPlayer'),
    url(r'^unbanplayerans/','GameManage.views.coc.gm.unbanPlayerAns'),
    #url(r'^sendmail/', 'GameManage.views.coc.gm.sendmail'),
    #url(r'^sendmailans/', 'GameManage.views.coc.gm.sendmailans'),
    #url(r'^resetserverstatus/','GameManage.views.coc.gm.resetserverstatus'),
    #url(r'^resetserverstatusans/','GameManage.views.coc.gm.resetserverstatusAns'),
    #url(r'^refreshfriend/','GameManage.views.coc.gm.refreshfriend'),
    #url(r'^refreshfriendans/','GameManage.views.coc.gm.refreshfriendAns'),
)
