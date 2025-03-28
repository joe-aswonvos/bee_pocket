from django.urls import path
from . import views
from pocket_app import views as pocket_views

urlpatterns = [
    path('', views.create_item, name='create_item'),
    path('create_item_instance/', views.create_item_instance,
         name='create_item_instance'),
    path('item_instances/<int:beepocket_id>/',
         views.item_instances, name='item_instances'),
    path('new_item_details/<int:item_id>/',
         views.new_item_details, name='new_item_details'),
    path('approve_item_instance/<int:instance_id>/',
         views.approve_item_instance, name='approve_item_instance'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('edit_item_instance/<int:instance_id>/',
         views.edit_item_instance, name='edit_item_instance'),
    path('delete_item_instance/<int:instance_id>/',
         views.delete_item_instance, name='delete_item_instance'),
    path('item/<int:item_id>/', pocket_views.item_detail, name='item_detail'),
]
