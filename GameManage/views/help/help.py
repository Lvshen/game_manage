#coding=utf-8
# Create your views here.
from django.db.models import Q
import re, os
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, Template
from GameManage.models.help import Help, HelpCategory
from GameManage.views.base import mkdir
from GameManage.settings import TEMPLATE_DIRS, MEDIA_ROOT, STATIC_ROOT

################# 删除 #####################
def help_del(request, model_id=0):
    model_id = int(model_id)
    p = Help.objects.get(id=model_id)
    p.delete()
    return HttpResponseRedirect('/help/list/')

################ 修改 ################
def edit(request, model_id=0):
    #修改信息
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    if model_id > 0:
        model = Help.objects.get(id=model_id)
    else:
        model = Help()
        model.id = model_id
        model.order = 0
        
    cgname = HelpCategory.objects.all()
    return render_to_response('help/edit.html', {'model':model, 'cgname':cgname})

def save(request, model_id=0):
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    if model_id > 0:
        model = Help.objects.get(id=model_id)
    else:
        model = Help()
    order = request.POST.get('order', 0)
    parent_id = request.POST.get('parent_id', 0)
    erro_msg = ''
    try:
        order = int(order)
        parent_id = int(parent_id)
    except:
        erro_msg = u'输入的排序格式错误'
    if erro_msg == '':
        model.title = request.POST.get('title', '')
        model.order = order
        model.filename = request.POST.get('filename', '')
        model.parent_id = parent_id
        model.content = request.POST.get('content', '')
        model.save()
    cgname = HelpCategory.objects.all()
    return render_to_response('feedback.html', {'cgname':cgname, 'err_msg':erro_msg})

################ 修改 ################ 
def category_save(request, model_id=0):
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    if model_id > 0:
        model = HelpCategory.objects.get(id=model_id)
    else:
        model = HelpCategory()
    
    res = HelpCategory.objects.all()
    err_msg = ''
    try:
        order = int(request.POST.get('order', '0'))
    except:
        err_msg = u'排序输入格式错误'
        
    if '' == err_msg:
        model.order = order
        model.name = request.POST.get('name', '')
        model.save()
    
    return render_to_response('help/category_list.html', {'cg':res, 'err_msg':err_msg})

#
#def help_add(request): 
#    raise Exception, 123
#    if request.method == 'POST':
#        title = request.POST.get('title','')
#        filename = request.POST.get('filename','')
#        parent_id = request.POST.get('parent_id',0)
#        content = request.POST.get('content','')
#        p = Help(title=title,filename=filename,parent_id=parent_id,content=content)
#        p.save()
#        return HttpResponseRedirect('/add/')
#    else:
#        category_list = HelpCategory.objects.all()
#        return render_to_response('help/add.html',{'cgname':category_list}) 
    
    
########   分类 管理列表    ##########
def category_list(request):
#    if request.method == 'POST':
#        name = request.POST.get('name','')
#        content = HelpCategory(name=name)
#        content.save()
#        return HttpResponseRedirect('/help/category/categorylist/')
#    else:
    if True:
        title = '分类列表'
        res = HelpCategory.objects.all()
        return render_to_response('help/category_list.html', {'cg':res, 'title':title})



def category_del (request, model_id=0):
    model_id = int(model_id)
    if 0 == model_id:
        model_id = int(request.GET.get('id', 0))
    p = HelpCategory.objects.get(id=model_id)
    p.delete()
    return HttpResponseRedirect('/help/category/list/')
    

def view(request, file_name=''):
    if file_name == '':
        file_name = request.GET.get('filename', '')
    if file_name=='' or file_name=='index.html':
        data_list = []
        cg = HelpCategory.objects.all()
        for item in cg:
            category = {}
            helps = Help.objects.filter(parent_id=item.id)
            category['name'] = item.name
            category['helps'] = helps
            data_list.append(category)
        return render_to_response('help/index.html', {'data_list':data_list})
    else:
        file_name = file_name[:-5]
        result = Help.objects.get(filename=file_name) 
    
        result.content = filter_content(result.content)
        return render_to_response('help/content.html', {'title':result.title, 'content':result.content})



def help_list(request):

    search_con = request.POST.get('title', '')
    parent_id = int(request.POST.get('parent_id', 0))
    if search_con == '' and parent_id == 0:
        res = Help.objects.all().order_by('parent_id','order')
    else:
        query = Q()
        if search_con != '':
            query = query & (Q(title__contains=search_con) | Q(content__contains=search_con))
            
        if 0 != parent_id :
            query = query & Q(parent_id=parent_id)
        res = Help.objects.filter(query)
        
    cgname = HelpCategory.objects.all()
    return render_to_response('help/list.html', {'res':res, 'cgname':cgname, 'search_con':search_con, 'parent_id':parent_id})

############# 生成静态页面  ###############
def file_create(request, help_id=0):

    help_id = int(help_id)
    
    if 0 == help_id:
        help_id = int(request.GET.get('id', 0))
    
    if help_id > 0:
        res = Help.objects.filter(id=help_id)
    else:
        res = Help.objects.all()
    
    file_tpl = open(r'%s/help/content.html' % TEMPLATE_DIRS[0], 'r')
    tpl_content = file_tpl.read()
    file_tpl.close()
    t = Template(tpl_content)
    
    save_path = r'%s/help' % MEDIA_ROOT
    
    mkdir(save_path)
    for item in res:
        sign = '%s' % item.filename
        title = item.title
        content = filter_content(item.content) 
        static_file_path = r'%s/%s.html' % (save_path, sign)
        delete_file(static_file_path)
        fileHandle = open (static_file_path, 'w')
        c = Context({"title":title, "content": content}) 
        c = t.render(c)
        fileHandle.write(c.encode('utf-8'))
        fileHandle.close()
    cgname = HelpCategory.objects.all()
    
    if help_id == 0:
        file_tpl = open(r'%s/help/index.html' % TEMPLATE_DIRS[0], 'r')
        tpl_content = file_tpl.read()
        file_tpl.close()
        t = Template(tpl_content)
        data_list = []
        cg = HelpCategory.objects.all()
        for item in cg:
            category = {}
            helps = Help.objects.filter(parent_id=item.id)
            category['name'] = item.name
            category['helps'] = helps
            data_list.append(category)
         
        
        index_html_path = r'%s/index.html' % (MEDIA_ROOT + '/help') 
        delete_file(index_html_path) 
        fileHandle = open (index_html_path, 'w')
        c = Context({"data_list":data_list})
        c = t.render(c)
        fileHandle.write((c).encode('utf-8'))
        fileHandle.close()
        
    return render_to_response('help/list.html', {'res':res, 'cgname':cgname})

def filter_content(html): 
    html = re.sub('\s{2,}', '\n', html) 
    html = '<li>%s</li>' % ('</li><li>'.join(html.split('\n')))
    html = html.replace('<li></li>', '')
    return html

def delete_file(file_path): 
    if os.path.isfile(file_path):
        #print 'delete:', file_path
        os.remove(file_path)


def import_html_data(request): 
    clear_db()
    fileHandle = open (r'%s/help/index.html' % (STATIC_ROOT), 'r')
    index_content = fileHandle.read()
    fileHandle.close()
    
    regex = ur"<li>([\s\S]+?)</li>"
    regex_span = ur"<span><b>\+</b>([\S\s]+?)</span>"
    regex_href = ur"href=\"(.*)\" target=\"right\""
    regex_title = ur"target=\"right\">([\S\s]+?)</a>"
    regex_body = ur"<body>([\s\S]+?)</body>"
    
    
    filter_regex = ur"<[\s\S]+?>"
    
    match = re.findall(regex, index_content)
    if match:
        index = 1
        
        for result in match:
            
            mark_span = re.findall(regex_span, result)
            
            category = HelpCategory()
            category.id = index 
            category.order = index
            category.name = mark_span[0].replace(" ", "")
            
            category.save()
            
            
            mark_href = re.findall(regex_href, result)
            href_title = re.findall(regex_title, result)
            #for i in range(mark_href.__len__()):
            #   print mark_href[i]
            h_index = 0
            for href in mark_href:
                fileHandle_href = open (r'%s/help/%s' % (STATIC_ROOT, href), 'r')
                fileHandle_href_content = fileHandle_href.read()
                fileHandle_href.close()
                
                model = Help()
                model.parent_id = index
                model.order = h_index
                model.filename = href[:-5]
                model.title = href_title[h_index]
                
                content = re.findall(regex_body, fileHandle_href_content)[0] 
                content = re.sub(r'</\S+>', '\n', content)
                content = re.sub(filter_regex, '', content)
                #print content
                model.content = content
                model.save()
                h_index = h_index + 1
            index = index + 1
        return render_to_response('feedback.html')
    else :
        return render_to_response('help/help_list.html')
    
    

def clear_db():
    HelpCategory.objects.all().delete()
    Help.objects.all().delete()
    
    
    
    
    
