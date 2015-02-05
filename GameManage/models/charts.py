# coding=utf-8
from django.db import models

def get_time_str(time): 
    if time == '' or time == None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S')


class ChartsDefine(models.Model):
    title = models.CharField(u'标题',max_length=50)
    charts_type = models.CharField(u'模块类别',max_length=10)
    query_result_id = models.IntegerField(u'统计汇总ID')
    is_show = models.IntegerField(u'是否显示')
    display_type = models.CharField(u'显示类别',max_length=10)
    chart_unit = models.CharField(u'报表单位',max_length=10)
    chart_height = models.IntegerField(u'模块高度')
    expression_cfg = models.CharField(u'公司表达式配置',max_length=100)
    
    def display_type_str(self):
        if self.display_type == "spline_time_chart":
            return u"图表"
        if self.display_type == "situation":
            return u"近日概况"
        if self.display_type == "summary":
            return u"信息摘要"
        if self.display_type == "date_trend":
            return u"时段趋势"
        if self.display_type == "top":
            return u"TOP10"  
        if self.display_type == "top_ratio":
            return u"饼图"                      
        return self.display_type
    
    class Meta:
        db_table = 'def_charts'
        app_label = 'GameManage'
        ordering = ('id',)
        
class ChartsResult(models.Model):
    name = models.CharField(u'查询名称', max_length=100)
    remark = models.CharField(u'查询说明', max_length=200)
    charts = models.ManyToManyField(ChartsDefine)
    
    class Meta: 
        db_table = u'charts_result'
        app_label = 'GameManage'
