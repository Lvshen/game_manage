#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.views.log import ExportCfg
import os, shutil, json
from django.http import HttpResponse
import sys
import codecs
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
class QueryExprot(object):
    
    def get_gene_file_name(self, query_id ,query_key):
        return "%s_%s" % (query_id, query_key)
        
    def gene_file(self, list_data, fields, file_name, page_num, page_size, total_record, file_type, close_export, clear_export_old_file, work_id, exprot_file_key = '', join_old_file = False):
        is_finish = False
        de = total_record / page_size
        
        if total_record % page_size >= 1:
            total_page =  de + 1 
        else:
            total_page =  de

        if page_num+1 > total_page:
            is_finish = True
     
          
        suffix = '.xls'
        #exportCfg = ExportCfg()
        if 2 == file_type:
            suffix = '.csv'
        if file_type == 3:
            suffix = '.txt'
            if str(fields).find('feiyin') != -1:
                import datetime
                if len(fields) > 6:
                    query_save_folder_name = fields
                else:
                    query_save_folder_name = 'feiyin/%s'%(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
                exportCfg = ExportCfg(query_save_folder_name)
            else:
                exportCfg = ExportCfg()
        else:
            exportCfg = ExportCfg()
        
        
        final_name = file_name + suffix
        url = exportCfg.query_export_url + final_name
        
        if os.path.isfile('%s%s%s'%(exportCfg.query_export_path , file_name , suffix)) and not clear_export_old_file:
            is_finish = True
        else:
            #如果创建的是第一页的数据
#            if page_num == 1:
#                #临时文件删除
#                tmp_file_path = '%s%s%s%s' % (exportCfg.query_tmp_path , file_name, work_id  , suffix)
#                if os.path.isfile(tmp_file_path):
#                    os.remove(tmp_file_path)
            #写文件
            self.write_file(exportCfg, file_name, suffix, file_type, list_data, fields, is_finish, close_export,  work_id, join_old_file)
        
        page_num = page_num + 1
        
        result = json.dumps({"page_num":page_num, "is_finish": is_finish, "total_page": total_page, "url":url, "exprot_file_key":exprot_file_key})
        
        return HttpResponse(result)
    
    def write_file(self, exportCfg, file_name, suffix, file_type, list_data, fields, is_finish, close_export,  work_id, join_old_file = False):
       
        final_name = file_name + suffix
        
        file_path = '%s%s%s%s' % (exportCfg.query_tmp_path , file_name, work_id  , suffix)
        
        is_create = True 
        fp = None
        
        if close_export:
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        if not os.path.isfile(file_path):
            fp = codecs.open(file_path, 'w','utf-8')
        else:
            is_create = False 
            fp = codecs.open(file_path, 'a','utf-8')
        
        if 2 == file_type:
            file_str = self.csv_convert(is_create, list_data, fields, is_finish)
        elif 3 == file_type:
            file_str = self.txt_convert(is_create, list_data, fields, is_finish)           
        else:
            file_str = self.excel_convert(is_create, list_data, fields, is_finish)
        
        fp.write(file_str)
        fp.flush()
        fp.close()
        if is_finish:
            if join_old_file and  os.path.isfile(exportCfg.query_export_path + final_name):#
                fp = None
                nfp = None
                try:
                    fp = codecs.open(exportCfg.query_export_path + final_name, 'a','utf-8')
                    nfp = codecs.open(file_path, 'r', 'utf-8')
                    file_str = nfp.read()
                    fp.write(file_str)
                    fp.flush()
                except Exception, ex:
                    print ex
                finally:
                    if fp != None:
                        fp.close()
                    if nfp != None:
                        nfp.close()
            else:    
                shutil.copy(file_path, exportCfg.query_export_path + final_name)
            os.remove(file_path)
    
    def csv_convert(self, is_create, list_data, fields, is_finish):
        file_str = '%s%s'
        
        head_str = ''
        if is_create: 
            field_index = 0
            for field in fields:
                field_index = field_index + 1 
                if field_index != fields.__len__():
                    head_str += '%s,'%field
                else:
                    head_str += '%s'%field
            head_str = '%s\n'%head_str
         
        row_str = ''
        for items in list_data:
            item_str = ''
            item_index = 0
            for item in items:
                item_index = item_index + 1
                if item_index != items.__len__():
                    item_str += '%s,' % item
                else:
                    item_str += '%s' % item
                    
            row_str += '%s\n'%item_str
        
        file_str = file_str % (head_str, row_str)
        
        return file_str
    
    def excel_convert(self, is_create, list_data, fields, is_finish):
        file_str = '%s%s'
        
        head_str = ''
        if is_create: 
            for field in fields: 
                head_str += '<td>%s</td>'%field
            head_str = '<table><tr>%s<\/tr>\n'%head_str
         
        row_str = ''
        for items in list_data:
            item_str = ''
            for item in items:
                item_str += '<td>%s</td>'%item
        
            row_str += '<tr>%s</tr>\n'%item_str
        
        file_str = file_str % (head_str, row_str)
     
        if is_finish:
            file_str += u'<\/table>' 
        
        return file_str
    
    def txt_convert(self, is_create, list_data, fields, is_finish):  
        head_str = ''
        row_str = ''
        if fields != '' and is_create and str(fields).find('feiyin') != 0:
            for field in fields: 
                head_str += '%s\t'%field
            head_str = head_str[0:len(head_str)-1]
            head_str = '%s\n'%head_str 
                       
        for items in list_data:
            item_str = ''
            for item in items:
                item_str += '%s\t'%item
            item_str = item_str[0:len(item_str)-1]
            row_str += '%s\n'%item_str
        
        file_str = '%s%s' % (head_str, row_str)

        return file_str        
