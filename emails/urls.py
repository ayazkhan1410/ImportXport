from django.urls import path, include
from . import views

urlpatterns = [
    path('send-email', views.send_email,name='send_email')
]