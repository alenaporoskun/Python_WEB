from django.contrib import admin
from django.urls import path, include
from users import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("quotes.urls")),
    path('register/', views.register, name='register'),
    #path('login/', views.login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
]


