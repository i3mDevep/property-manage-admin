from rest_framework import serializers

from coproperties.models import Coproperty

class CopropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coproperty
        fields = '__all__'
