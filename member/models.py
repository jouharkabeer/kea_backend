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
    created_by = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - {self.rating} Stars"