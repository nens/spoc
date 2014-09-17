# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from spoc import views

admin.autodiscover()

from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = patterns(
    'spoc.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'api_root'),
    url(r'^locations/$', 'location_list', name='location-list'),
    url(r'^locations/(?P<pk>[0-9]+)/$', 'location_detail', name='location-detail'),
    url(r'^scadalocations/(?P<pk>[a-zA-Z0-9_.-]+)/$',
        'scadalocation_detail', name='scadalocation-detail'),
    url(r'^oeilocations/(?P<pk>[a-zA-Z0-9_.-]+)/$',
        'oeilocation_detail', name='oeilocation-detail'),
    url(r'^scadalocations/headers/(?P<pk>[a-zA-Z0-9_.-]+)/$',
        'header_detail', name='header-detail'),
    url(r'^validations/(?P<pk>[a-zA-Z0-9_.-]+)/$',
        'validation_detail', name='validation-detail'),
    url(r'^headerformulas/$',
        'headerformula_list', name='headerformula-list'),
    url(r'^headerformulas/(?P<pk>[a-zA-Z0-9_.-]+)/$',
        'headerformula_detail', name='headerformula-detail'),
    url(r'^formulatypes/$', 'formulatypes_list', name='formulatypes-list'),
    
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^something/',
    #     views.some_method,
    #     name="name_it"),
    # url(r'^something_else/$',
    #     views.SomeClassBasedView.as_view(),
    #     name='name_it_too'),
    )
