from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny

class UserRegistrationView(APIView):
    permission_classes = [] 
    authentication_classes = []
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.user_type:
                print(user.user_type, user.is_active)
            return Response({"message": "User registered successfully!", "user_id": user.user_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateMemberView(APIView):
    permission_classes = [] 
    authentication_classes = []
    def post(self, request):
        user_id = request.data.get("user_id")
        try:
            user = CustomUser.objects.get(user_id=user_id)
            if user.user_type == "member" and not user.is_active:
                user.activate_membership()
                return Response({"message": "Membership activated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": "User is already active or not a member"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import send_otp, verify_otp
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


import firebase_admin
from firebase_admin import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class OTPLoginView(APIView):
    permission_classes = [] 
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")

        try:
            # Check if user exists
            user = CustomUser.objects.get(phone_number=phone_number)

            # Firebase Phone Authentication: Send OTP
            link = auth.generate_sign_in_with_email_link(email=phone_number)  # Firebase sends an OTP to phone_number
            return Response({"message": "OTP sent!", "link": link}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class OTPVerifyView(APIView):
    permission_classes = [] 
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")
        
        try:
            # Verify Firebase OTP
            decoded_token = auth.verify_id_token(otp)  # OTP is actually the ID token in Firebase
            
            if decoded_token and decoded_token.get("phone_number") == phone_number:
                user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
                refresh = RefreshToken.for_user(user)
                return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordLoginView(APIView):
    permission_classes = [] 
    authentication_classes = []
    def post(self, request):
        phone_number = request.data.get("phone_number")  # Change from username to phone_number
        password = request.data.get("password")
        
        user = authenticate(username=phone_number, password=password)
        if user:
            user.membership_is_valid()
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
            return Response({"error": "You need a subsription","user_id": user.user_id})

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

