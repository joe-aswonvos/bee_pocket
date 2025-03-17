from django.contrib import admin
from .models import Item, Category, ItemInstance, Comment, Repeatability, Weekday, CommentReadStatus

class RepeatabilityAdmin(admin.ModelAdmin):
    list_display = ('RepeatableDaily', 'WeeklyRepeatInterval')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('ItemInstance', 'Comment', 'CreatedBy', 'CreatedOn')
    list_display_links = ('ItemInstance', 'CreatedBy')
    search_fields = ('ItemInstance', 'Comment', 'CreatedBy')
    ordering = ('CreatedOn',)

class ItemInstanceAdmin(admin.ModelAdmin):
    list_display = ('item', 'ActiveStatus', 'CreatedBy', 'CreatedOn', 'Lasteditedby', 'Lasteditedon', 'expireon', 'Approved')
    search_fields = ('item', 'CreatedBy')
    ordering = ('CreatedOn',)
    list_filter = ('ActiveStatus', 'Approved')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_description', 'item_category', 'item_type', 'item_value', 'createdon', 'createdby')
    list_filter = ('item_category', 'item_type')
    ordering = ('createdon',)
    search_fields = ('item_name', 'item_description')
    
class CommentReadStatusAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'read')

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(ItemInstance, ItemInstanceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReadStatus, CommentReadStatusAdmin)
admin.site.register(Repeatability, RepeatabilityAdmin)
admin.site.register(Weekday)