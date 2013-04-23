# -*- coding: utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django.db import models
from django.contrib.auth.models import User
import workcenter.settings as settings


class Foo(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

        # class Meta:
        #     verbose_name = "FOO"
        #     db_table = "wc_foo"


class DepartmentManager(models.Manager):
    def valid_departments(self):
        """
        有效部门数据
        """
        return self.filter(status=1)


class Department(models.Model):
    """
    部门
    """
    name = models.CharField(max_length=40L, verbose_name="部门名称")
    descrption = models.CharField(max_length=100L, blank=True, verbose_name="部门描述")
    status = models.IntegerField(verbose_name="状态")
    parent_id = models.BigIntegerField(null=True, blank=True, verbose_name="上级部门ID")
    sort = models.IntegerField(verbose_name="排序")
    creator_user = models.IntegerField(verbose_name="创建人")
    gmt_create = models.DateTimeField(verbose_name="创建时间")
    modifier_user = models.IntegerField(null=True, blank=True, verbose_name="修改人")
    gmt_modified = models.DateTimeField(null=True, blank=True, verbose_name="修改时间")

    # 有效部门数据
    objects = DepartmentManager()

    class Meta:
        verbose_name = verbose_name_plural = "部门"
        db_table = 'wc_department'


class RequirementTypeManager(models.Manager):
    def valid_types(self):
        """
        有效项目需求类型
        """
        return self.filter(code_type="requirement_type", status=1)


class CodeValue(models.Model):
    """
    基础字典
    """
    code_type = models.CharField(max_length=20L, verbose_name="字典类型")
    code = models.CharField(max_length=10L, blank=True, verbose_name="字典编码")
    value = models.CharField(max_length=20L, verbose_name="字典内容")
    sort = models.IntegerField(verbose_name="字典排序")
    status = models.IntegerField(verbose_name="字典状态")
    creator_user = models.IntegerField(verbose_name="创建人")
    gmt_create = models.DateTimeField(verbose_name="创建时间")
    modifier_user = models.IntegerField(null=True, blank=True, verbose_name="修改人")
    gmt_modified = models.DateTimeField(null=True, blank=True, verbose_name="修改时间s")

    # 有效项目需求类型
    objects = RequirementTypeManager()

    class Meta:
        verbose_name = verbose_name_plural = "基础字典"
        db_table = 'wc_code_value'


class Requirement(models.Model):
    """
    项目需求
    """
    requirement_code = models.CharField(max_length=30L, blank=True, verbose_name="需求单号")
    requirement_name = models.CharField(max_length=100L, verbose_name="需求名称")
    requirement_type = models.IntegerField(verbose_name="需求类别")
    requirement_dept = models.IntegerField(verbose_name="需求部门")
    requirement_desc = models.CharField(max_length=500L, verbose_name="需求描述")
    gmt_hope_finished = models.DateTimeField(verbose_name="期望完成日期")
    status = models.IntegerField(verbose_name="需求状态")
    submitter_user = models.IntegerField(verbose_name="需求提出人")
    #submitter_user = models.ForeignKey(User, db_column="submitter_user")
    gmt_submit = models.DateTimeField(verbose_name="需求提出时间")
    modifier_user = models.IntegerField(null=True, blank=True, verbose_name="修改人")
    gmt_modified = models.DateTimeField(null=True, blank=True, verbose_name="修改时间")

    class Meta:
        ordering = ['-gmt_submit']
        verbose_name = verbose_name_plural = "项目需求"
        db_table = 'wc_requirement'

    def set_status(self, status):
        self.status = status

    def set_gmt_submit(self, gmt_submit):
        self.gmt_submit = gmt_submit

    def set_modifier_user(self, modifier_user):
        self.modifier_user = modifier_user

    def set_gmt_modified(self, gmt_modified):
        self.gmt_modified = gmt_modified

    def set_submitter_user(self, submitter_user):
        self.submitter_user = submitter_user

    def _get_requirement_type_name(self):
        """
        获取需求类型描述
        """
        try:
            type = CodeValue.objects.get(code_type="requirement_type", code=self.requirement_type)
        except:
            return settings.TEMPLATE_STRING_IF_INVALID
        return type.value

    def _get_submitter_user_name(self):
        """
        获取提交人姓名
        """
        try:
            user = User.objects.get(id=self.submitter_user)
        except:
            return settings.TEMPLATE_STRING_IF_INVALID
        return user.username

    def _get_requirement_dept_name(self):
        """
        获取部门名称
        """
        try:
            dept = Department.objects.get(id=self.requirement_dept)
        except:
            return settings.TEMPLATE_STRING_IF_INVALID
        return dept.name

    requirement_type_name = property(_get_requirement_type_name)
    submitter_user_name = property(_get_submitter_user_name)
    requirement_dept_name = property(_get_requirement_dept_name)
