from django.forms import widgets
from rest_framework import serializers
from spoc.models import Location, LANGUAGE_CHOICES, STYLE_CHOICES


class LocationSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Location
        fields = ('id', 'locationId', 'name', 'linenos', 'language', 'style')
