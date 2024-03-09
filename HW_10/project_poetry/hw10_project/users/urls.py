from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('register/', views.signupuser, name='register'),
    path('login/', views.loginuser, name='login'),
    #path('logout/', views.logoutuser, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]
