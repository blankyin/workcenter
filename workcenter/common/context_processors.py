# -*- coding: utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django.utils.encoding import smart_text


def requirement_type_dict(request):
    result = {1:"中午",2:2, 3:3}
   # print smart_str(result)
    return {"requirement_type_dict": result}