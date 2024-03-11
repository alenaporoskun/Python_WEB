from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path('add/', views.add_quote, name='add_quote'),
    #path('author/<str:author_id>/', views.author_detail, name='author_detail'),
    path('author/<slug:author_slug>/', views.author_detail, name='author_detail'),
]
