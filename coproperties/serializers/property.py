from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin

from coproperties.models import  Property

class PropertySerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = '__all__'