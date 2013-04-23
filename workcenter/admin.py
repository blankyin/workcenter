__author__ = 'yinchangjiang.ht'

from django.contrib import admin
from workcenter.models import Foo, CodeValue, Requirement

admin.site.register(Foo)
admin.site.register(CodeValue)
admin.site.register(Requirement)