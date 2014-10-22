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
        fields = ('url', 'locationid', 'locationname', 'sort',
                  'gpgin', 'gpginzp', 'gpginwp', 'gpguit', 'gpguitzp', 'gpguitwp' )


class SourceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Source
        fields = ('source_type',)


class DiverSerializer(serializers.HyperlinkedModelSerializer):
    header = serializers.PrimaryKeyRelatedField()
    dstop = serializers.DateField(required=False)
    dstart = serializers.DateField(required=False)
    ref_h = serializers.FloatField(required=False)
    baro = serializers.CharField(required=False)

    class Meta:
        model = models.Diver
        fields = ('url', 'dstart', 'dstop', 'ref_h', 'baro', 'header')

class DiverDetailsSerializer(DiverSerializer):

    header = serializers.PrimaryKeyRelatedField(write_only=True, required=False)


class ParameterSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = models.Parameter
        fields = ('id', 'name', 'formula_allowed')


class ValidationSerializer(serializers.HyperlinkedModelSerializer):
    
    field = serializers.CharField(source='field', read_only=True)

    class Meta:
        model = models.Validation
        fields = ('url', 'field', 'value')


class HeaderFormulaSerializer(serializers.HyperlinkedModelSerializer):
    header = serializers.PrimaryKeyRelatedField()
    dstop = serializers.DateField(required=False)
    dstart = serializers.DateField(required=False)
    formula_type = serializers.PrimaryKeyRelatedField(required=False, source='formula_type')
    #formula_type = serializers.CharField(required=False)

    class Meta:
        model = models.HeaderFormula
        fields = ('url', 'header', 'dstart', 'dstop', 'formula_type', 
                  'coef01','coef02', 'coef03', 'coef04', 'coef05',
                  'coef06', 'coef07', 'coef08', 'coef09', 'coef10',
                  'coef11', 'coef12')


class HeaderSerializer(serializers.HyperlinkedModelSerializer):
    
    parameter = ParameterSerializer(read_only=True)
    validations = ValidationSerializer(read_only=True)
    formulas = HeaderFormulaSerializer(source="headerformula_set")
    location = serializers.PrimaryKeyRelatedField(read_only=True)
    divers = DiverSerializer(source="diver_set")

    class Meta:
        model = models.Header
        fields = ('url', 'location', 'parameter', 'validations', 'formulas', 'divers')


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
        fields = ('id', 'url', 'fews', 'forward', 'visible', 'created', 'oei_location', 'scada_location')


class PaginatedLocationSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = LocationSerializer


class FormulaTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.FormulaType
        fields = ('code',)
