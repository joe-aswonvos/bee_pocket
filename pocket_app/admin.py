from django.contrib import admin
from .models import Item, Category, ItemInstance, Comment, Repeatability, Weekday

# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(ItemInstance)
admin.site.register(Comment)
admin.site.register(Repeatability)
admin.site.register(Weekday)