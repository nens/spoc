from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination
from spoc import models


class LocationSortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LocationSort
        filds = ('sort',)


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    # pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    # locationId = serializers.CharField(required=False,
    #                                    max_length=255)
    # name = serializers.CharField(widget=widgets.Textarea,
    #                              max_length=255)
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES,
    #                                    default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES,
    #                                 default='friendly')

    # def restore_object(self, attrs, instance=None):
    #     """
    #     Create or update a new location instance, given a dictionary
    #     of deserialized field values.

    #     Note that if we don't define this method, then deserializing
    #     data will simply return a dictionary of items.
    #     """
    #     if instance:
    #         # Update existing instance
    #         instance.locationId = attrs.get('locationId', instance.locationId)
    #         instance.name = attrs.get('name', instance.name)
    #         instance.linenos = attrs.get('linenos', instance.linenos)
    #         instance.language = attrs.get('language', instance.language)
    #         instance.style = attrs.get('style', instance.style)
    #         return instance

    #     # Create new instance
    #     return Location(**attrs)
    sort = LocationSortSerializer()
    
    class Meta:
        model = models.Location
        fields = ('url', 'locationid', 'locationname', 'sort', 'gpgzmrpl', 'gpgwntpl')


class OEISerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.OEI
        fields = ('url', 'objectid', 'mpnident', 'mpnomschr', 'mpndatin')


class WNSAttributeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.WNSAttribute
        fields = ('url', 'wnsid', 'wnsname', 'wnshmax', 'wnshmin', 'wnssmax', 'wnssmin')


class LocationWNSSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LocationWNS
        fields = ('id', 'objectid', 'wnsid')


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
        fields = ('url', 'id', 'locationid', 'locationname', 'source', 'parameter')


class LocationHeaderSerializer(serializers.HyperlinkedModelSerializer):
#class LocationHeaderSerializer(serializers.ModelSerializer):
    header = HeaderSerializer()
    oei_location = LocationSerializer()
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')

    class Meta:
        model = models.LocationHeader
        fields = ('url', 'id', 'oei_location', 'header')
        #fields = ('id',)


class PaginatedLocationHeaderSerializer(pagination.PaginationSerializer):

    class Meta:
        object_serializer_class = LocationHeaderSerializer
