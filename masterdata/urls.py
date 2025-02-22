from django.urls import path
from .views import *

urlpatterns = [

    path('allmembers/', AllMembersView.as_view(), name='All availble member details'),
    path('memberdetails/', MemberDetailView.as_view(), name='login member details'),

]
