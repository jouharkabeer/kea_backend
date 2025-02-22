from django.db import models
from users.models import CustomUser
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
import uuid

class Testimonial(models.Model):
    testimonial_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 30)
    email = models.EmailField(max_length=30)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    title = models.CharField(max_length=20)
    testimonial = models.TextField(validators=[MinLengthValidator(15)], max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - {self.rating} Stars"
    

class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name="events")
    event_name = models.CharField(max_length=100)  # Changed from ForeignKey to CharField
    event_sub_name = models.CharField(max_length=30)
    description = models.TextField()  # Changed from EmailField to TextField
    location = models.CharField(max_length=255)  # Changed from FloatField to CharField
    fee_for_member = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField
    fee_for_external = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField
    registration_ends = models.DateTimeField()
    event_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.event_name} - {self.event_sub_name}"
