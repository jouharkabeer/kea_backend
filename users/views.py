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


# import firebase_admin
# from firebase_admin import auth
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from django.contrib.auth import get_user_model

# CustomUser = get_user_model()

# class OTPLoginView(APIView):
#     permission_classes = [] 
#     authentication_classes = []
#     print (auth)
#     print('')
#     def post(self, request):
#         phone_number = request.data.get("phone_number")

#         # try:
#         #     # Check if user exists
#         #     user = CustomUser.objects.get(phone_number=phone_number)
            
#         #     # Firebase Phone Authentication: Send OTP
#         #     link = auth.generate_sign_in_with_email_link(email=phone_number)  # Firebase sends an OTP to phone_number
#         #     return Response({"message": "OTP sent!", "link": link}, status=status.HTTP_200_OK)

#         # except CustomUser.DoesNotExist:
#         #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             # Check if user exists
#             user = CustomUser.objects.get(phone_number=phone_number)
            
#             # Firebase Phone Authentication: Send OTP
#             verification_id = auth.verify_phone_number(phone_number)  # Firebase phone authentication method
#             return Response({"message": "OTP sent!", "verification_id": verification_id}, status=status.HTTP_200_OK)

#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
       



# class OTPVerifyView(APIView):
#     permission_classes = [] 
#     authentication_classes = []

#     def post(self, request):
#         phone_number = request.data.get("phone_number")
#         otp = request.data.get("otp")
        
#         try:
#             # Verify Firebase OTP
#             decoded_token = auth.verify_id_token(otp)  # OTP is actually the ID token in Firebase
            
#             if decoded_token and decoded_token.get("phone_number") == phone_number:
#                 user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
#                 refresh = RefreshToken.for_user(user)
#                 return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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

import phonenumbers
from firebase_admin import auth

def format_phone_number(phone_number):
    """Converts phone number to E.164 format"""
    try:
        parsed_number = phonenumbers.parse(phone_number, "IN")  # "IN" is for India; change accordingly
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            return None
    except phonenumbers.NumberParseException:
        return None

class OTPLoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")
        formatted_number = format_phone_number(phone_number)

        if not formatted_number:
            return Response({"error": "Invalid phone number format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if user exists in CustomUser database
            uservh = CustomUser.objects.get(phone_number=phone_number)

            try:
                # Check if user exists in Firebase Authentication
                user = auth.get_user_by_phone_number(formatted_number)
                
            except auth.UserNotFoundError:
                # If user is not found, create a new Firebase user
                user = auth.create_user(phone_number=formatted_number)
                print(f"New user created in Firebase: {user.uid}")

            return Response({"message": "OTP sent!"}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found in database"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")
        verification_id = request.data.get("verification_id")
        otp = request.data.get("otp")
        
        try:
            # Verify OTP with Firebase
            verification_result = auth.verify_id_token(otp)
            if verification_result:
                user = CustomUser.objects.get(phone_number=phone_number)
                refresh = RefreshToken.for_user(user)
                return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

import random
import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView


class OTPSendView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.otp_expiry:
                print(user.otp_expiry)
                print(timezone.now())
                if user.otp_expiry < timezone.now():
                    print(user.otp_expiry)
                    user.otp_expiry = None
                    user.otp_tries = 0
                    user.save()
            if user.otp_tries == None:
                user.otp_tries = 0
                user.save()
            if user.otp_tries >= 3:
                return Response({"error": "Maximum OTP attempts reached"}, status=400)

            otp = random.randint(1000, 9999)  # Generate a 4-digit OTP
            user.otp = otp
            user.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            user.otp_tries += 1
            user.save()

            print(otp)  # Ideally, you should send this OTP via SMS or email
            return Response({"message": "OTP sent successfully","otp": otp}, status=200)

        except CustomUser.DoesNotExist:
            return Response({"error": "No user found with this phone number"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class VerifyOTPview(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = str(request.data.get("otp"))  # Ensure OTP is compared as a string
        print(otp)
        
        try:
            user = CustomUser.objects.get(otp=otp, phone_number=phone_number)
            if user.otp and user.otp_expiry and user.otp_expiry > timezone.now():
                user.otp = None  # Consider setting to "" instead of None
                user.otp_expiry = None
                user.otp_tries = 0
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "OTP verified successfully",
                    "access": str(refresh.access_token),  # Access Token
                    "refresh": str(refresh)  # Refresh Token
                }, status=200)

            else:
                return Response({"error": "OTP expired or invalid"}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid OTP or phone number"}, status=400)

            if user.otp_tries == None:
                user.otp_tries = 0
                user.save()
            if user.otp_tries >= 3:
                return Response({"error": "Maximum OTP attempts reached"}, status=400)
            refresh = RefreshToken.for_user(user)
            otp = random.randint(1000, 9999)  # Generate a 4-digit OTP
            user.otp = otp
            user.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            user.otp_tries += 1
            user.save()

            print(otp)  # Ideally, you should send this OTP via SMS or email
            return Response({"message": "OTP sent successfully"}, status=200)

        except CustomUser.DoesNotExist:
            return Response({"error": "No user found with this phone number"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
