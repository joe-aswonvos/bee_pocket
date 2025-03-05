from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_account, name='manage_account'),
    path('create_permission/', views.create_permission, name='create_permission'),
    path('create_beepocket/', views.create_beepocket, name='create_beepocket'),
]
