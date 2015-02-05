from django.conf.urls import include, url
#from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'game_manage.views.home', name='home'),
    url(r'^GameManage/', include('GameManage.urls', namespace = "GameManage")),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}), 
    #url(r'^admin/', include(admin.site.urls)),
]
