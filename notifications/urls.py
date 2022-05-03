from django.urls import path
from .views import *

urlpatterns = [
    path('send/', NotifyMe.as_view() ,name="send-notifications"),
    path('get/', NotifyMe.as_view() ,name="get-notifications"),
]
