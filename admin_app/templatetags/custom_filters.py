from django import template

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