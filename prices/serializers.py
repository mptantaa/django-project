from rest_framework import serializers
from .models import Prices, Categories


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('id', 'name', 'unit', 'price', 'category')
        
class PricesRetriveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('id', 'name', 'unit', 'price', 'category')

class PricesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('id', 'name', 'unit', 'price', 'category')

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name')
        
class CategoriesRetriveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name')

class CategoriesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name')
