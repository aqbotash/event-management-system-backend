from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Event


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {'event_id': {'read_only': True}}