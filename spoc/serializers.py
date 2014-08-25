from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination
from spoc import models


class LocationSortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LocationSort
        filds = ('sort',)


class OEILocationSerializer(serializers.HyperlinkedModelSerializer):
    
    sort = LocationSortSerializer()
    
    class Meta:
        model = models.OEILocation
        fields = ('url', 'locationid', 'locationname', 'sort', 'gpgzmrpl', 'gpgwntpl')


class SourceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Source
        fields = ('source_type',)


class ParameterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Parameter
        fields = ('id', 'name')


class ValidationSerializer(serializers.HyperlinkedModelSerializer):
    
    field = serializers.CharField(source='field', read_only=True)

    class Meta:
        model = models.Validation
        fields = ('url', 'field', 'value')


class HeaderSerializer(serializers.HyperlinkedModelSerializer):
    
    parameter = ParameterSerializer(read_only=True)
    validations = ValidationSerializer(read_only=True)
    location = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Header
        fields = ('url', 'location', 'parameter', 'validations')


class ScadaLocationSerializer(serializers.HyperlinkedModelSerializer):
    
    source = SourceSerializer(read_only=True)
    headers = HeaderSerializer()

    class Meta:
        model = models.ScadaLocation
        fields = ('url', 'locationid', 'locationname', 'source', 'headers')


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    scada_location = ScadaLocationSerializer(read_only=True)
    oei_location = OEILocationSerializer(read_only=True)
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')

    class Meta:
        model = models.Location
        fields = ('url', 'fews', 'forward', 'visible', 'created', 'oei_location', 'scada_location')


class PaginatedLocationSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = LocationSerializer
