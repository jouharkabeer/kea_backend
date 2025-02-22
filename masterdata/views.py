from django.shortcuts import render
from rest_framework import generics
from users.models import CustomUser
from .serialozers import *

class AllMembersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# class MemberDetailView(generics.ListAPIView):
#     def post(self, request):
#         phone_number = request.data.get("phone_number")
#         queryset = CustomUser.objects.all(phone_number = phone_number)
#         serializer_class = UserSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class MemberDetailView(APIView):  
    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(phone_number=phone_number)  # Fetch a single user
            serializer = UserSerializer(user)  # Serialize single user object
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
