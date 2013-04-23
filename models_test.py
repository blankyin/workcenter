# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AdminToolsDashboardPreferences(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser')
    data = models.TextField()
    dashboard_id = models.CharField(max_length=100L)
    class Meta:
        db_table = 'admin_tools_dashboard_preferences'

class AdminToolsMenuBookmark(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser')
    url = models.CharField(max_length=255L)
    title = models.CharField(max_length=255L)
    class Meta:
        db_table = 'admin_tools_menu_bookmark'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100L)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128L)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=30L, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200L)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class WcCodeValue(models.Model):
    id = models.BigIntegerField(primary_key=True)
    code_type = models.CharField(max_length=20L)
    code = models.CharField(max_length=10L, blank=True)
    value = models.CharField(max_length=20L)
    sort = models.IntegerField()
    status = models.IntegerField()
    creator_user = models.IntegerField()
    gmt_create = models.DateTimeField()
    modifier_user = models.IntegerField(null=True, blank=True)
    gmt_modified = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'wc_code_value'

class WcDepartment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40L)
    descrption = models.CharField(max_length=100L, blank=True)
    status = models.IntegerField()
    parent_id = models.BigIntegerField(null=True, blank=True)
    sort = models.IntegerField()
    creator_user = models.IntegerField()
    gmt_create = models.DateTimeField()
    modifier_user = models.IntegerField(null=True, blank=True)
    gmt_modified = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'wc_department'

class WcRequirement(models.Model):
    id = models.BigIntegerField(primary_key=True)
    requirement_code = models.CharField(max_length=30L, blank=True)
    requirement_name = models.CharField(max_length=100L)
    requirement_type = models.IntegerField()
    requirement_dept = models.IntegerField()
    requirement_desc = models.CharField(max_length=500L)
    gmt_hope_finished = models.DateTimeField()
    status = models.IntegerField()
    submitter_user = models.IntegerField()
    gmt_submit = models.DateTimeField()
    modifier_user = models.IntegerField(null=True, blank=True)
    gmt_modified = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'wc_requirement'

