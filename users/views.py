from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from .models import CustomUser

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!", "user_id": user.user_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateMemberView(APIView):
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


class OTPVerifyView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")
        if verify_otp(phone_number, otp):
            user = CustomUser.objects.get(phone_number=phone_number)
            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)



class OTPLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        print(phone_number)
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            otp = send_otp(phone_number)
            return Response({"message": "OTP sent!", "otp": otp}, status=status.HTTP_200_OK)  # Remove otp field in production
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class PasswordLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")  # Change from username to phone_number
        password = request.data.get("password")
        
        user = authenticate(username=phone_number, password=password)
        
        if user:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
            return Response({"error": "You need a subsription"})

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

