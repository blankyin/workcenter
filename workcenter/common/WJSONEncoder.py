# -*- coding: utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django.core.serializers import deserialize
import simplejson
from django.db.models.query import QuerySet
from django.db import models


class WJSONEncoder(simplejson.JSONEncoder):
    def getObjFields(self, instance):
        """
        获取Model的字段与值
        """
        fields = self.get_fields_and_properties(type(instance), instance)

        data = {}
        for attr in fields:
            data[attr] = getattr(instance, attr)

        return data

    def default(self, obj):
        if isinstance(obj, QuerySet):
            result = []
            for item in obj:
                result.append(self.getObjFields(item))
            return result
        if isinstance(obj, models.Model):
            result = self.getObjFields(obj)
            return result
        if hasattr(obj, 'isoformat'):
            return obj.isoformat(' ')   # 使用空格代替T
        return simplejson.JSONEncoder.default(self, obj)

    def get_fields_and_properties(self, model, instance):
        """
        获取model实例的所有field和property属性
        """
        field_names = [f.name for f in model._meta.fields]
        property_names = [name for name in dir(model) if isinstance(getattr(model, name), property)]
        return dict((name, getattr(instance, name)) for name in field_names + property_names)


def jsonBack(json):
    """
    还原Json数据
    """
    if json[0] == '[':
        return deserialize('json', json)
    else:
        return deserialize('json', '[' + json + ']')


def getJson(**args):
    """
    可以自定义Json规则
    """
    result = dict(args)
    return simplejson.dumps(result, cls=WJSONEncoder)

