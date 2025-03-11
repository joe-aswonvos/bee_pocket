from django.urls import path
from . import views

urlpatterns = [
    path('', views.userpage, name='userpage'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]