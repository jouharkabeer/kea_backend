from django.urls import path
from .views import *

urlpatterns = [

    path('allmembers/', AllMembersView.as_view(), name='register'),

]
