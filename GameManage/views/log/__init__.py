#! /usr/bin/python
# -*- coding: utf-8 -*-
from GameManage.views.base import GlobalPathCfg, mkdir
from GameManage.log_cfg import ENUM_LOG_STATUS
from GameManage.cache.log_cache import get_center_log, get_statistic
import datetime

def the_log_in_center(log_def):
    '''@log_def 支持int 也可以是一个 log_define '''
    if type(log_def) == int or type(log_def) == long:
        center_log_list = get_center_log()
        if None != center_log_list:
            for item in center_log_list:
                if item.id == log_def:
                    return True
    else:
        if log_def.status == ENUM_LOG_STATUS.SAVE_CENTER:
            return True
    return False

def the_statistic_in_center(statistic):
    '''@statistic 支持int 也可以是一个 statistic对象 '''
    if type(statistic) == int or type(statistic) == long:
        statistic = get_statistic(statistic)
    return the_log_in_center(statistic.log_type)

field_types = [u'字符串', u'时间', u'日期', u'小时', u'整数', u'小数', u'百分数']

def format_value(field_def, value):
    field_type = field_def.field_type
    if field_type == u'时间':
        try:
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        except:
            value = float(value)
            value = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
        
        
    elif field_type == u'日期':
        value = value.strftime('%Y-%m-%d')
    elif field_type == u'小时':
        value = value.strftime('%Y-%m-%d %H')
    elif field_type == u'整数':
        value = int(value)
    elif field_type == u'小数':
        value = float(value)
    elif field_type == u'百分数':
        value = '%s%%' % (value * 100)
    return value


class ExportCfg(object):
    def __init__(self, query_save_folder_name = ''):
        self.path_cfg = GlobalPathCfg()
        self.static_path = self.path_cfg.get_static_folder_path()
        
        self.root_folder_name = 'export'
        self.temp_folder_name = 'tmp'

        self.export_root_path = self.static_path + r'/' + self.root_folder_name
        
        #创建保存导出根目录
        mkdir(self.export_root_path)
        if query_save_folder_name:
            mkdir(self.export_root_path + r'/feiyin')
            self.query_save_folder_name = query_save_folder_name
        else:
            self.query_save_folder_name = 'query'        
        self.query_export_path = self.export_root_path + r'/' + self.query_save_folder_name
        
        #创建查询导出目录
        mkdir(self.query_export_path)
        
        self.query_tmp_path = self.query_export_path + r'/' + self.temp_folder_name
        
        #创建查询导出临时目录
        mkdir(self.query_tmp_path)
        
        self.export_root_path = self.export_root_path + r'/'
        self.query_export_path = self.query_export_path + r'/'
        self.query_tmp_path = self.query_tmp_path + r'/'
        
        self.query_export_url = '/%s/%s/%s/' % (self.path_cfg.static_folder_name, self.root_folder_name, self.query_save_folder_name)
        
        
        
        
        
        
    
    
