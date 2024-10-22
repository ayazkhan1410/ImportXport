from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='login'),
    path('sign-up', views.signup, name='signup')
]
