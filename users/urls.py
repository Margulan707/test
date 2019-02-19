from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/change', views.profile_change, name='profile-change'),
    path('profile/change_password', views.password_change, name='profile-change-password'),
    path('signup/', views.signup, name='signin'),
] 
