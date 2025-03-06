from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from admin_app.models import Account

@login_required
def index_page(request):
    user = request.user
    try:
        account = Account.objects.get(account_owner=user)
        context = {
            'account_id': account.id,
        }
    except Account.DoesNotExist:
        context = {
            'account_id': None,
        }
    return render(request, 'base.html', context)

def userpage(request):
    return render(request, 'pocket.html')


