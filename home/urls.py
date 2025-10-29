from django.contrib import admin
from django.urls import path, include

from .views import BlogView

urlpatterns = [
    path('blogs/', BlogView.as_view(), name='blog-list-create'),
    path('blogs/<uuid:uid>/', BlogView.as_view(), name='blog-detail'),
]