from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

class Testimonialview(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class TestimonialCreate(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class TestimonialExternalCreate(generics.ListCreateAPIView):
    permission_classes = [] 
    authentication_classes = []
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class TestimonialUpdate(generics.UpdateAPIView):
    lookup_field = 'testimonial_id'
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class TestimonialDelete(generics.DestroyAPIView):
    lookup_field = 'testimonial_id'  # Ensure this matches your model's field name
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class Eventview(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventCreate(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventUpdate(generics.UpdateAPIView):
    lookup_field = 'Event_id'
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDelete(generics.DestroyAPIView):
    lookup_field = 'event_id' 
    queryset = Event.objects.all()
    serializer_class = EventSerializer