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
# from django.core.urlresolvers import reverse

from spoc import models
from spoc import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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


@api_view(['GET'])
def oei_list(request):
    """
    List all loction of OEI model.
    """
    if request.method == 'GET':
        locations = models.OEI.objects.all()
        serializer = serializers.OEISerializer(locations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def oei_detail(request, pk):
    """
    Retrieve a location from oei table.
    """
    try:
        location = models.OEI.objects.get(pk=pk)
    except models.OEI.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.OEISerializer(location)
        return Response(serializer.data)


@api_view(['GET'])
def wnsattribute_list(request):
    """
    List all wms-attributes.
    """
    if request.method == 'GET':
        wnsattributes = models.WNSAttribute.objects.all()
        serializer = serializers.WNSAttributeSerializer(wnsattributes, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def wnsattribute_detail(request, pk):
    """
    Retrieve a wns-attribute.
    """
    try:
        wnsattribute = models.WNSAttribute.objects.get(pk=pk)
    except models.WNSAttribute.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.WNSAttributeSerializer(wnsattribute)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def location_list(request):
    """
    List all locations, or create a new location.
    """
    if request.method == 'GET':
        locations = models.Location.objects.all()
        serializer = serializers.LocationSerializer(locations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, pk):
    """
    Retrieve, update or delete a location.
    """
    try:
        location = models.Location.objects.get(pk=pk)
    except models.Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.LocationSerializer(location)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.LocationSerializer(location, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        location.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ListLocations(viewsets.ModelViewSet):
    """ List dummy locations. """

    model = models.Location
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class LocationDetails(viewsets.ModelViewSet):
    """ List dummy locations. """

    model = models.Location
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, pk=None):
        location = models.Locations.objects.get(pk=pk)
        return Response(location)

    def post(self, request, pk=None, *args, **kwargs):
        import pdb; pdb.set_trace()
        return Response(models.Location.objects.get(pk=pk))
