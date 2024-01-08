from rest_framework import serializers
from .models import Feedbacks


class FeedbacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = ('id', 'name', 'phone', 'message', 'created_at')
        
class FeedbacksRetriveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = ('id', 'name', 'phone', 'message', 'created_at')

class FeedbacksCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = ('id', 'name', 'phone', 'message', 'created_at')