# -*- coding:utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django.forms.widgets import DateInput


class My97DateInput(DateInput):
    """
    自定义My97日期控件widgets
    """
    def __init__(self, attrs={}):
        super(My97DateInput, self).__init__(attrs)
        self.attrs['onclick'] = 'WdatePicker({readOnly:true})'
        self.attrs['class'] = 'Wdate'