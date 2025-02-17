from rest_framework.permissions import BasePermission

class AllowAnyForRegistration(BasePermission):
    def has_permission(self, request, view):
        return view.__class__.__name__ == 'UserRegistrationView' or request.user and request.user.is_authenticated
