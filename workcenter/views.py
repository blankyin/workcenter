# -*- coding: utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from workcenter.models import Foo, Requirement
from workcenter.common.PageHelper import PageHelper
from workcenter.common.ModelHelper import get_labels_for
from workcenter.common import PageUtil
from workcenter.forms import FooForm, RequirementForm
import time


def login(request):
    return render_to_response("admin/login.html")


def add_foo(request):
    if request.method == "POST":
        form = FooForm(request.POST)
        if form.is_valid():
            return HttpResponse("1", mimetype="application/javascript")
        else:
            return HttpResponse("2", mimetype="application/javascript")
    else:
        form = FooForm()
        return render_to_response("admin/add_foo.html", {"form": form}, context_instance=RequestContext(request))


def foo_list(request):
    result = None
    if request.GET:
        rows = None
        pageNo = None
        try:
            rows = int(request.GET[PageUtil.JQGRID_ROWS]) # 详细显示的记录，默认对应jqGrid中配置的rowNum
        except ValueError:
            rows = PageUtil.PAGE_NUM

        try:
            pageNo = int(request.GET[PageUtil.JQGRID_PAGE])
        except ValueError:
            pageNo = PageUtil.PAGE_NO

        sortname = str(request.GET[PageUtil.JQGRID_SORT_NAME]) # 排序字段
        sortorder = str(request.GET[PageUtil.JQGRID_SORT_ORDER])    # 排序方式
        if sortorder and sortorder.upper() == "DESC":
            sortname = "-" + sortname

        foos = Foo.objects.all().order_by(sortname)

        pageHelper = PageHelper(foos, rows, pageNo)
        result = pageHelper.getPaginatorJson()

    return HttpResponse(result, mimetype="application/javascript")


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def requirement_list(request):
    """
    需求列表查询页面:
    GET:进入requirement_list页面
    POST:分页查询数据
    """
    if request.method == "GET":
        return render_to_response("admin/wc/requirement_list.html", context_instance=RequestContext(request))
    else:
        rows = None
        pageNo = None
        try:
            rows = int(request.POST[PageUtil.JQGRID_ROWS]) # 详细显示的记录，默认对应jqGrid中配置的rowNum
        except ValueError:
            rows = PageUtil.PAGE_NUM

        try:
            pageNo = int(request.POST[PageUtil.JQGRID_PAGE])
        except ValueError:
            pageNo = PageUtil.PAGE_NO

        sortname = str(request.POST[PageUtil.JQGRID_SORT_NAME]) # 排序字段
        sortorder = str(request.POST[PageUtil.JQGRID_SORT_ORDER])    # 排序方式
        if sortorder and sortorder.upper() == "DESC":
            sortname = "-" + sortname

        requirements = Requirement.objects.all().order_by(sortname)

        pageHelper = PageHelper(requirements, rows, pageNo)
        result = pageHelper.getPaginatorJson()
        return HttpResponse(result, mimetype="application/javascript")



def add_requirement(request):
    """
    新增需求
    """
    if request.method == "POST":
        form = RequirementForm(request.POST)
        if form.is_valid():
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            form.save_requirement(1, dt, True)
            return HttpResponse("1", mimetype="application/javascript")
        else:
            return HttpResponse("2", mimetype="application/javascript")
    else:
        form = RequirementForm()
        return render_to_response("admin/wc/add_requirement.html", {"form": form, "is_popup":"true"}, context_instance=RequestContext(request))


def requirement_detail(request, requirement_id):
    try:
        requirement_id = int(requirement_id)
    except ValueError:
        #raise Http404()
        pass
    requirement = Requirement.objects.get(id=requirement_id)
    labels = get_labels_for(requirement)

    return render_to_response("admin/wc/requirement_detail.html", {"labels":labels, "requirement": requirement, "is_popup":"true"})





