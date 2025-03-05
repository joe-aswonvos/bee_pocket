from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Account, BeePocket, UserPermission

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.get(account_owner=user)
    permissions = UserPermission.objects.filter(account=account)
    beepockets = BeePocket.objects.filter(account=account)
    users = User.objects.all()

    context = {
        'permissions': permissions,
        'beepockets': beepockets,
        'users': users,
    }
    return render(request, 'admin.html', context)

@login_required
def create_permission(request):
    if request.method == 'POST':
        user_id = request.POST['user']
        beepocket_id = request.POST['beepocket']
        permission = request.POST['permission']

        user = User.objects.get(id=user_id)
        beepocket = BeePocket.objects.get(id=beepocket_id)
        account = beepocket.account

        UserPermission.objects.create(user=user, account=account, beepocket=beepocket, permission=permission)
        return redirect('manage_account')

@login_required
def create_beepocket(request):
    if request.method == 'POST':
        beepocket_name = request.POST['beepocket_name']
        units = request.POST['units']
        starting_balance = request.POST['starting_balance']

        account = Account.objects.get(account_owner=request.user)
        BeePocket.objects.create(beepocket_name=beepocket_name, units=units, starting_balance=starting_balance, account=account)
        return redirect('manage_account')