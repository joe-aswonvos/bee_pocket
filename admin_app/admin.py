from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account, BeePocket, UserPermission

# Register your models here.

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'user_icon')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)
    
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_type', 'creation_date', 'active_status', 'account_owner')
    search_fields = ('account_name', 'account_owner')
    list_filter = ('account_type', 'active_status')
    ordering = ('creation_date',)

class BeePocketAdmin(admin.ModelAdmin):
    list_display = ('account', 'beepocket_name', 'units', 'starting_balance', 'creation_date')
    list_display_links = ('account',)
    search_fields = ('account', 'beepocket_name')
    list_filter = ('units',)
    ordering = ('creation_date',)
    
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('account', 'beepocket', 'user', 'permission')
    list_display_links = ('account', 'beepocket', 'user')
    search_fields = ('account', 'beepocket', 'user')
    list_filter = ('permission',)
    ordering = ('user',)

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(BeePocket, BeePocketAdmin)
admin.site.register(UserPermission, UserPermissionAdmin)