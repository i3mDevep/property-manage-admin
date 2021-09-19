from rest_framework import serializers

from coproperties.models import  Property

class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = '__all__'