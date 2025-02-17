from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

class Testimonialview(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestmonialSerializer


class TestimonialCreate(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestmonialSerializer


class TestimonialExternalCreate(generics.ListCreateAPIView):
    permission_classes = [] 
    authentication_classes = []
    queryset = Testimonial.objects.all()
    serializer_class = TestmonialSerializer

class TestimonialUpdate(generics.UpdateAPIView):
    lookup_field = 'testimonial_id'
    queryset = Testimonial.objects.all()
    serializer_class = TestmonialSerializer