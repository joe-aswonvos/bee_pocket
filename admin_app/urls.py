from django.urls import path
from . import views

urlpatterns = [
    path('<int:account_id>/', views.manage_account, name='manage_account'),
    path('create_permission/<int:account_id>/', views.create_permission, name='create_permission'),
    path('create_beepocket/<int:account_id>/', views.create_beepocket, name='create_beepocket'),
    path('edit_permission/<int:account_id>/<int:permission_id>/', views.edit_permission, name='edit_permission'),
    path('delete_permission/<int:account_id>/<int:permission_id>/', views.delete_permission, name='delete_permission'),
    path('edit_beepocket/<int:account_id>/<int:beepocket_id>/', views.edit_beepocket, name='edit_beepocket'),
    path('delete_beepocket/<int:account_id>/<int:beepocket_id>/', views.delete_beepocket, name='delete_beepocket'),
]