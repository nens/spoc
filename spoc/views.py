# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext as _

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.reverse import reverse
# from django.core.urlresolvers import reverse

from spoc import models
from spoc import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view


# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'locations': reverse('location-header-list', request=request, format=format),
        #'parameters': reverse('wnsattribute-list', request=request, format=format)
    })



@api_view(['GET'])
def location_list(request):
    """
    List all locations.
    """
    ITEMS_PER_PAGE = 20

    if request.method == 'GET':
        queryset = models.Location.objects.all()
        
        page = request.QUERY_PARAMS.get('page')
        items = request.QUERY_PARAMS.get('items_per_page', None)
        try:
            items = int(items)
        except:
            items = ITEMS_PER_PAGE

        paginator = Paginator(queryset, items)
        try:
            locations = paginator.page(page)
        except PageNotAnInteger:
            locations = paginator.page(1)
        except EmptyPage:
            locations = paginator.page(paginator.num_pages)

        serializer = serializers.PaginatedLocationSerializer(
            locations, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def location_detail(request, pk):
    """
    Retrieve a location from LocatonHeader table.
    """
    try:
        location = models.Location.objects.get(pk=pk)
    except models.Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.LocationSerializer(
            location, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.LocationSerializer(location, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def oeilocation_detail(request, pk):
    """
    Retrieve a oei-location from OEILocation table.
    """
    try:
        location = models.OEILocation.objects.get(pk=pk)
    except models.OEILocation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.OEILocationSerializer(
            location, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def scadalocation_detail(request, pk):
    """
    Retrieve a scada-location from ScadaLocation table.
    """
    try:
        location = models.ScadaLocation.objects.get(pk=pk)
    except models.ScadaLocation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ScadaLocationSerializer(
            location, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def header_detail(request, pk):
    """
    Retrieve a header details from Header table.
    """
    try:
        header = models.Header.objects.get(pk=pk)
    except models.Header.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.HeaderSerializer(
            header, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.HeaderSerializer(header, request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
