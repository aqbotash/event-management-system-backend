from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import SignUpSerializer, EventSerializer
from django.contrib.auth.models import User
from .models import Event


class SignUpCreateAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=password,
        )
        return user
    
    

class EventsListAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('event_id') 
    permission_classes = (AllowAny,)