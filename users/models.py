import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta

import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field is required")
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    whatsapp_number = models.CharField(max_length=15, unique=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    department_of_study = models.CharField(max_length=30, blank=True, null=True)
    year_of_graduation = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Only activate after payment for members
    is_staff = models.BooleanField(default=False)  # Required for Django admin panel

    username = None  # Remove the username field
    USERNAME_FIELD = 'phone_number'  # Login with phone number instead of username
    REQUIRED_FIELDS = ['email', 'user_type']

    objects = CustomUserManager()  # Use the custom user manager

    def __str__(self):
        return self.phone_number
    
    def activate_membership(self):
        self.is_active = True
        self.save()

