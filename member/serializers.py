from rest_framework import serializers
from .models import *

class TestmonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
