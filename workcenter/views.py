# -*- coding: utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django.db.models.fields import DateTimeField, DateField
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db import transaction
from workcenter.models import Foo, Requirement, CodeValue, Department
from workcenter.common.PageHelper import PageHelper
from workcenter.common.ModelHelper import get_labels_for
from workcenter.common import PageUtil
from workcenter.forms import FooForm, RequirementForm
from workcenter.common.WJSONEncoder import getJson
import time
import datetime


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
            rows = int(request.POST.get(PageUtil.JQGRID_ROWS)) # 详细显示的记录，默认对应jqGrid中配置的rowNum
        except:
            rows = PageUtil.PAGE_NUM

        try:
            pageNo = int(request.POST.get(PageUtil.JQGRID_PAGE))
        except:
            pageNo = PageUtil.PAGE_NO

        try:
            sortname = str(request.POST.get(PageUtil.JQGRID_SORT_NAME)) # 排序字段
            sortorder = str(request.POST.get(PageUtil.JQGRID_SORT_ORDER))    # 排序方式
            if sortorder and sortorder.upper() == "DESC":
                sortname = "-" + sortname
        except:
            sortname = None

        # 查询条件
        searchDict = {}
        for field in Requirement._meta.fields:
            if request.POST.get(field.name):
                fieldValue = request.POST.get(field.name)
                if isinstance(field, DateField) or isinstance(field, DateTimeField):
                    fieldValue = datetime.datetime.strptime(fieldValue, "%Y-%m-%d")
                    searchDict[field.name + '__range'] = (
                        datetime.datetime.combine(fieldValue, datetime.time.min),
                        datetime.datetime.combine(fieldValue, datetime.time.max))
                else:
                    searchDict[field.name + '__icontains'] = fieldValue

        if sortname:
            requirements = Requirement.objects.filter(**searchDict).order_by(sortname)
        else:
            requirements = Requirement.objects.filter(**searchDict)

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
        return render_to_response("admin/wc/add_requirement.html", {"form": form, "is_popup": "true"},
                                  context_instance=RequestContext(request))


@csrf_exempt
def update_requirement(request):
    """
    更新需求
    """
    result = False
    try:
        if request.POST.get("id"):
            rid = request.POST.get("id")
            new_requirement_name = request.POST.get("requirement_name")
            new_requirement_type = int(request.POST.get("requirement_type_name"))
            new_requirement_dept = int(request.POST.get("requirement_dept_name"))
            new_requirement_desc = request.POST.get("requirement_desc")
            localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            update = Requirement.objects.filter(id=rid).update(requirement_name=new_requirement_name,
                                                            requirement_type=new_requirement_type,
                                                            requirement_dept=new_requirement_dept,
                                                            requirement_desc=new_requirement_desc,
                                                            modifier_user = request.user.id,
                                                            gmt_modified = localtime)
            if update == 1:
                result = True
    except:
        pass

    result = getJson(status=result)
    return HttpResponse('[' + result + ']', mimetype="application/javascript")


@csrf_exempt
@transaction.commit_manually
def del_requirement(request):
    """
    删除需求
    """
    result = False
    try:
        if request.POST.get("ids"):
            idstr = request.POST.get("ids")
            if idstr:
                ids = idstr.split(",")
                rids = [int(rid) for rid in ids]
                update = Requirement.objects.filter(id__in=rids).update(status=-1)
                if (update == len(ids)):
                    result = True
    except:
        pass

    if result:
        transaction.commit()
    else:
        transaction.rollback()

    result = getJson(status=result)
    return HttpResponse(result, mimetype="application/javascript")


def requirement_detail(request, requirement_id):
    """
    需求详情
    """
    try:
        requirement_id = int(requirement_id)
    except ValueError:
        #raise Http404()
        pass
    requirement = Requirement.objects.get(id=requirement_id)
    labels = get_labels_for(requirement)

    return render_to_response("admin/wc/requirement_detail.html",
                              {"labels": labels, "requirement": requirement, "is_popup": "true"})


def requirement_type_list(request):
    """
    需求类别下拉框公用组件
    """
    try:
        result = CodeValue.objects.valid_types()
    except:
        result = None

    return render_to_response("admin/wc/requirement_type_list.html", {"result": result})


def requirement_dept_list(request):
    """
    需求类别下拉框公用组件
    """
    try:
        result = Department.objects.valid_departments()
    except:
        result = None

    return render_to_response("admin/wc/requirement_dept_list.html", {"result": result})


def user_list(request):
    """
    有效用户下拉框公用组件
    """
    try:
        result = User.objects.filter(is_active=1)
    except:
        result = None

    return render_to_response("admin/wc/user_list.html", {"result": result})




