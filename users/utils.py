import random
from django.core.cache import cache
from twilio.rest import Client
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))  # Generate 6-digit OTP

def send_otp(phone_number):
    otp = generate_otp()
    cache.set(f"otp_{phone_number}", otp, timeout=300)  # Store OTP for 5 minutes

    # Send OTP via Twilio
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp  # For testing, return OTP (remove this in production)

def verify_otp(phone_number, otp):
    stored_otp = cache.get(f"otp_{phone_number}")
    if stored_otp and stored_otp == otp:
        cache.delete(f"otp_{phone_number}")  # Remove OTP after verification
        return True
    return False
