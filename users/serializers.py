from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_type', 'email', 'phone_number', 'whatsapp_number',
                  'company_name', 'designation', 'department_of_study', 
                  'year_of_graduation', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        if user.user_type == "admin":
            user.is_active = True  # Admins are active by default
        else:
            user.is_active = False  # Members need to pay
        user.save()
        return user
