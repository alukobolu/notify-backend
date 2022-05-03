from django.contrib import admin
from django.urls import path
from .views import *

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [

    path('sign-up/', SignUp.as_view()),
    path('check-email/', CheckEmail.as_view()),
    path('update-profile/', UpdateDetails.as_view()),
]
