from django.urls import path, re_path, include
from . import views
from rest_framework import routers
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('rest_auth.urls')),
    path('register/', views.UserCreate.as_view(), name='register'),

]
