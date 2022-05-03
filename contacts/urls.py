from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('create-group/', CreateGroup.as_view()),
    path('get-group/', GetGroup.as_view()),
    path('get-contacts/', GetGroup.as_view()),
]
