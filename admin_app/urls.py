from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_account, name='manage_account'),
    path('create_permission/', views.create_permission, name='create_permission'),
    path('create_beepocket/', views.create_beepocket, name='create_beepocket'),
    path('edit_permission/<int:permission_id>/', views.edit_permission, name='edit_permission'),
    path('delete_permission/<int:permission_id>/', views.delete_permission, name='delete_permission'),
    path('edit_beepocket/<int:beepocket_id>/', views.edit_beepocket, name='edit_beepocket'),
    path('delete_beepocket/<int:beepocket_id>/', views.delete_beepocket, name='delete_beepocket'),
]