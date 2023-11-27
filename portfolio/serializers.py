from rest_framework import serializers
from .models import Portlofios


class PortlofiosSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    class Meta:
        model = Portlofios
        fields = ('id', 'name', 'unit', 'description', 'image')
        
class PortlofiosRetriveUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    class Meta:
        model = Portlofios
        fields = ('id', 'name', 'unit', 'description', 'image')

class PortlofiosCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    class Meta:
        model = Portlofios
        fields = ('id', 'name', 'unit', 'description', 'image')