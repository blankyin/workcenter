from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from workcenter import views
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'workcenter.views.home', name='home'),
    # url(r'^workcenter/', include('workcenter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    #url(r'admin/workcenter/requirement/$', views.requirement_list),



    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }),

    url(r'^admin/workcenter/foo_list/', views.foo_list),


    url(r'^login/', views.login),
    url(r'^admin/workcenter/add_foo/', views.add_foo),


    url(r'admin/workcenter/requirement_list/', views.requirement_list),
    url(r'^admin/workcenter/add_requirement/', views.add_requirement),
    url(r'^admin/workcenter/requirement_detail/(\d+)/', views.requirement_detail),


)
