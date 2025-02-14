from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser  # Replace with your actual User model

class PhoneNumberAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=username)  # Authenticate with phone_number
            if user.check_password(password):  # Verify password
                return user
        except CustomUser.DoesNotExist:
            return None
