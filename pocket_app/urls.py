from django.urls import path
from . import views

urlpatterns = [
    path('mypockets/', views.userpage),
]
