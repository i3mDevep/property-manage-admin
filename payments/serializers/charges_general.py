from rest_framework import serializers

from payments.models import ChargesGeneral

class ChargesGeneralSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargesGeneral
        fields = '__all__'
