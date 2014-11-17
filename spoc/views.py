# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect

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


def string_to_bool(bool_string):
    if bool_string == 'true':
        return True
    elif bool_string == 'false':
        return False
    else:
        return None


def get_filtered_locationset(queryset, request):
    
    visible = string_to_bool(request.QUERY_PARAMS.get('visible', None))
    fews = string_to_bool(request.QUERY_PARAMS.get('fews', None))
    forward = string_to_bool(request.QUERY_PARAMS.get('forward', None))
    oei_location = request.QUERY_PARAMS.get('oei_location', None)
    scada_location = request.QUERY_PARAMS.get('scada_location', None)
    source = request.QUERY_PARAMS.get('source', None)
    
    if type(visible).__name__ == 'bool':
        queryset = queryset.filter(visible=visible)
    else:
        queryset = queryset.filter(visible=True)

    if type(fews).__name__ == 'bool':
        queryset = queryset.filter(fews=fews)

    if type(forward).__name__ == 'bool':
        queryset = queryset.filter(forward=forward)

    if type(oei_location).__name__ in ['str', 'unicode']:
        queryset = queryset.filter(oei_location__locationid__icontains=oei_location)
    
    if type(scada_location).__name__ in ['str', 'unicode']:
        queryset = queryset.filter(scada_location__locationid__icontains=scada_location)
    
    #if type(oei_location_name).__name__ in ['str', 'unicode']:
    #    queryset = queryset.filter(oei_location__locationname__icontains=oei_location_name)
    
    #if type(scada_location_name).__name__ in ['str', 'unicode']:
    #    queryset = queryset.filter(scada_location__locationname__icontains=scada_location_name)
    
    if type(source).__name__ in ['str', 'unicode']:
        queryset = queryset.filter(scada_location__source__source_type__iexact=source)

    return queryset


def sort_locationset(queryset, request):
    fieldname = request.QUERY_PARAMS.get('sort', None)
    fieldorder = request.QUERY_PARAMS.get('order', None)
    order = ''
    
    if fieldname in [None, '']:
        return queryset

    if fieldorder == 'desc':
        order = '-'
    else:
        order = ''

    queryset = queryset.order_by('{0}{1}__{2}'.format(order, fieldname, 'locationid')

    return queryset
        
        
@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'locations': reverse('location-list', request=request, format=format),
        'formulatypes': reverse('formulatypes-list', request=request, format=format),
        'headerformulas': reverse('headerformula-list', request=request, format=format)
    })


@api_view(['GET'])
def formulatypes_list(request):
    """
    List formula types.
    """

    if request.method == 'GET':

        formula_types = models.FormulaType.objects.all()

        serializer = serializers.FormulaTypeSerializer(
            formula_types, context={'request': request})
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def location_list(request):
    """
    List all locations.
    """
    ITEMS_PER_PAGE = 20

    if request.method == 'GET':
                
        page = request.QUERY_PARAMS.get('page')
        items = request.QUERY_PARAMS.get('items_per_page', None) 

        queryset = get_filtered_locationset(
            models.Location.objects.all(), request)
        queryset = sort_locationset(queryset, request)

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
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT'])
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
    elif request.method == 'PUT':
        serializer = serializers.LocationSerializer(location, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT'])
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
    elif request.method == 'PUT':
        serializer = serializers.HeaderSerializer(header, request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT'])
def validation_detail(request, pk):
    """
    Retrieve a validation details from Header table.
    """
    try:
        validation = models.Validation.objects.get(pk=pk)
    except models.Validation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ValidationSerializer(
            validation, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.ValidationSerializer(validation, request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def headerformula_list(request):
    
    if request.method == 'POST':
        formula = models.HeaderFormula()
        serializer = serializers.HeaderFormulaSerializer(formula, request.DATA)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect( reverse('headerformula-detail', args=[formula.id]))
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT'])
def headerformula_detail(request, pk):
    """
    Retrieve a formula details from HeaderFormul table.
    """
    try:
        formula = models.HeaderFormula.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = serializers.HeaderFormulaSerializer(
                formula, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.HeaderFormulaSerializer(formula, request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except models.HeaderFormula.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def diver_list(request):
    
    if request.method == 'POST':
        diver = models.Diver()
        serializer = serializers.DiverSerializer(diver, request.DATA)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect( reverse('diver-detail', args=[diver.id]))
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT'])
def diver_detail(request, pk):
    """
    Retrieve a diver details.
    """
    try:
        diver = models.Diver.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = serializers.DiverSerializer(
                diver, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.DiverDetailsSerializer(diver, request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except models.Diver.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
