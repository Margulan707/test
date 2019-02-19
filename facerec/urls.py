from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [
    path('', views.facerec_main, name = 'facerec_main'),
    path('api/', views.facerec, name = 'facerec_main'),
    path('api/delete/', views.check_delete, name = 'check_delete')
]
