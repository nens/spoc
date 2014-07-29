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


class HeaderSerializer(serializers.HyperlinkedModelSerializer):
    
    source = SourceSerializer()
    parameter = ParameterSerializer()

    class Meta:
        model = models.Header
        fields = ('url', 'id', 'location', 'parameter', 'source')


class ScadaLocationSerializer(serializers.HyperlinkedModelSerializer):
    
    #headers = serializers.RelatedField(many=True, read_only=True)
    headers = HeaderSerializer()
    class Meta:
        model = models.ScadaLocation
        fields = ('url', 'locationid', 'locationname', 'headers')


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    scada_location = ScadaLocationSerializer()
    oei_location = OEILocationSerializer()
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')

    class Meta:
        model = models.Location
        fields = ('url', 'id', 'oei_location', 'scada_location')


class PaginatedLocationSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = LocationSerializer
