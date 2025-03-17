from django.urls import path
from . import views

urlpatterns = [
    path('', views.userpage, name='userpage'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]