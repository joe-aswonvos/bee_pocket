from django import template
from admin_app.models import Account, BeePocket
from pocket_app.models import ItemInstance

register = template.Library()

@register.filter
def unique_manager_permission(permissions):
    seen = set()
    unique_permissions = []
    for permission in permissions:
        if permission.permission not in seen:
            unique_permissions.append(permission)
            seen.add(permission.permission)
    return unique_permissions

@register.filter
def toggle_boolean(value):
    return not value

@register.simple_tag
def is_account_owner(user):
    try:
        Account.objects.get(account_owner=user)
        return True
    except Account.DoesNotExist:
        return False

@register.filter
def has_instances(item):
    return ItemInstance.objects.filter(item=item).exists()

@register.filter
def pocket_has_instances(beepocket):
    return ItemInstance.objects.filter(BeePocketID=beepocket, ActiveStatus=True).exists()
