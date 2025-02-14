from django.utils.timezone import now
from .models import CustomUser

class CheckMembershipMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.user_type == "member":
            if request.user.expiry_date and request.user.expiry_date < now().date():
                request.user.is_active = False
                request.user.save()
        return self.get_response(request)
