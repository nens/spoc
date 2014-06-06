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


@csrf_exempt
def location_detail(request, pk):
    """
    Retrieve, update or delete a location.
    """
    try:
        location = models.Location.objects.get(pk=pk)
    except models.Location.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = serializers.LocationSerializer(location)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = serializers.LocationSerializer(location, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        location.delete()
        return HttpResponse(status=204)


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
