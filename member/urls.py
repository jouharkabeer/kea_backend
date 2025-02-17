from django.urls import path
from .views import *

urlpatterns = [
    path('testimonial/', Testimonialview.as_view(), name='testimonial'),
    path('testimonial/create/', TestimonialCreate.as_view(), name='testimonial create'), 
    path('testimonial/externaluser/create/', TestimonialExternalCreate.as_view(), name='testimonial external create'),
    path('testimonial/update/<uuid:testimonial_id>/', TestimonialUpdate.as_view(), name='testimonial external create'),
]