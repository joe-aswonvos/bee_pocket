from admin_app.models import Account

def account_info(request):
    context = {
        'account_id': None
    }
    
    if request.user.is_authenticated:
        try:
            account = Account.objects.filter(account_owner=request.user).first()
            if account:
                context['account_id'] = account.id
        except Exception:
            pass
            
    return context