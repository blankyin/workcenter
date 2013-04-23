# -*- coding: utf-8 -*-
__author__ = 'yinchangjiang.ht'

from django import forms
from django.contrib.auth.models import User
from workcenter.widgets import My97DateInput
from workcenter.models import Requirement, Department, CodeValue

PLEASE_SELECT = "---请选择---"

# 有效需求类别下拉框
REQUIREMENT_TYPE_DICT = {'': PLEASE_SELECT}
REQUIREMENT_TYPE_DICT.update(
    dict(((codevalue.code, codevalue.value) for codevalue in CodeValue.objects.valid_types())))

# 有效部门下拉框
REQUIREMENT_DEPT_DICT = {'': PLEASE_SELECT}
REQUIREMENT_DEPT_DICT.update(dict(((dept.id, dept.name) for dept in Department.objects.valid_departments())))

# 有效用户下拉框
ACTIVE_USERS_DICT = {'': PLEASE_SELECT}
ACTIVE_USERS_DICT.update(dict(((user.id, user.username) for user in User.objects.filter(is_active=1))))


class FooForm(forms.Form):
    name = forms.CharField(max_length=50)


class RequirementForm(forms.ModelForm):
    requirement_code = forms.CharField(required=False)
    requirement_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), max_length=100, label="需求名称")
    requirement_type = forms.ChoiceField(choices=REQUIREMENT_TYPE_DICT.items(), label="需求类别")
    requirement_dept = forms.ChoiceField(choices=REQUIREMENT_DEPT_DICT.items(), label="需求部门")
    requirement_desc = forms.CharField(widget=forms.Textarea, label="需求描述")
    gmt_hope_finished = forms.DateTimeField(widget=My97DateInput, label="期望完成日期")
    submitter_user = forms.ChoiceField(choices=ACTIVE_USERS_DICT.items(), label="需求提出人")
    status = forms.IntegerField(required=False)
    gmt_submit = forms.DateTimeField(required=False)
    modifier_user = forms.IntegerField(required=False)
    gmt_modified = forms.DateTimeField(required=False)

    class Meta:
        model = Requirement

    def save_requirement(self, status, gmt_submit, commit=True):
        requirement = super(RequirementForm, self).save(commit=False)
        requirement.set_status(status)
        requirement.set_gmt_submit(gmt_submit)
        if commit:
            requirement.save()
        return requirement