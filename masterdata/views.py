from django.shortcuts import render
from rest_framework import generics
from users.models import CustomUser
from .serialozers import *

class AllMembersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer