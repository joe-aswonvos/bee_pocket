from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .models import Account

def account_owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        account_id = kwargs.get('account_id')
        account = Account.objects.get(id=account_id)
        if account.account_owner != user:
            return redirect('/')  # Redirect to the base URL if the user is not the account owner
        return view_func(request, *args, **kwargs)
    return _wrapped_view