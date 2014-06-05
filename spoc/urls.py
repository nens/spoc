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

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
from rest_framework.views import APIView

# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     model = User

# class GroupViewSet(viewsets.ModelViewSet):
#     model = Group


router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'groups', GroupViewSet)
router.register(r'locations', views.ListLocations)
urlpatterns = patterns(
    '',
    #url(r'^$', HomepageView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^something/',
    #     views.some_method,
    #     name="name_it"),
    # url(r'^something_else/$',
    #     views.SomeClassBasedView.as_view(),
    #     name='name_it_too'),
    )
