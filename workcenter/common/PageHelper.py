# -*- coding: utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django.core.paginator import Paginator
from workcenter.common.WJSONEncoder import getJson

class PageHelper(object):
    """

    """

    def __init__(self, objects, rows=20, pageNo=1):
        self.objects = objects
        self.rows = rows
        self.pageNo = pageNo

    def getPaginatorJson(self):
        """
        objects:查询的数据列表
        rows:详细显示的记录，默认对应jqGrid中配置的rowNum
        pageNo:当前页码
        """
        paginator = Paginator(self.objects, self.rows)

        if self.pageNo < 1:
            self.pageNo = 1

        if self.pageNo > paginator.num_pages:
            self.pageNo = paginator.num_pages

        page = paginator.page(self.pageNo)

        # total:总页数, page:当前页数, records:总记录数, rows:实际数据
        result = getJson(total=paginator.num_pages, page=self.pageNo, records=paginator.count, rows=page.object_list)
        return result