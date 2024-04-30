from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Event, Date


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ['date']  # Adjust fields according to your Date model

class EventSerializer(serializers.ModelSerializer):
    dates = DateSerializer(many=True, read_only=True)  # Ensure 'dates' is the related name in the Event model

    class Meta:
        model = Event
        fields = ['event_id', 'name', 'img', 'address', 'category', 'price', 'contact', 'description', 'dates']