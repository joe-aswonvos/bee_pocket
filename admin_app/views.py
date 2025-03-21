from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import User, Account, BeePocket, UserPermission
from .decorators import account_owner_required
from pocket_app.utils import calculate_balance


@login_required
@account_owner_required
def manage_account(request, account_id):
    """
    View to manage user permissions and beepockets for an account.
    """

    account = Account.objects.get(id=account_id)
    permissions = UserPermission.objects.filter(account=account)
    beepockets = BeePocket.objects.filter(account=account)
    users = User.objects.all()

    # Calculate balance for each BeePocket and group by units
    beepocket_balances = {}
    unit_totals = defaultdict(int)
    for beepocket in beepockets:
        balance = calculate_balance(beepocket)
        beepocket_balances[beepocket.id] = balance
        if balance != 0:
            unit_totals[beepocket.units] += balance

    context = {
        'account': account,
        'permissions': permissions,
        'beepockets': beepockets,
        'beepocket_balances': beepocket_balances,
        'unit_totals': dict(unit_totals),
        'users': users,
    }
    return render(request, 'admin.html', context)


@login_required
@account_owner_required
def create_permission(request, account_id):
    """
    Create a new user permission for a beepocket within an account. Each user can have multiple permissions for different beepockets within the same account.
    Error handling is done to ensure that the user, beepocket, and account exist before creating the permission.
    """
    user = request.user
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        try:
            user_id = request.POST['user']
            beepocket_id = request.POST['beepocket']
            permission = request.POST['permission']

            user = User.objects.get(id=user_id)
            beepocket = BeePocket.objects.get(id=beepocket_id)
            account = beepocket.account

            UserPermission.objects.create(
                user=user, account=account, beepocket=beepocket, permission=permission)
            messages.success(
                request, f'Permission "{permission}" for user "{user.username}" on beepocket "{beepocket.beepocket_name}" created successfully')
            return redirect('manage_account', account_id=account_id)
        except (User.DoesNotExist, BeePocket.DoesNotExist, Account.DoesNotExist) as e:
            messages.error(request, f'Error: {str(e)}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
    return render(request, 'admin.html', {'account': account})

@login_required
@account_owner_required
def create_beepocket(request, account_id):
    """
    Create a new beepocket for an account.
    """
    user = request.user
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        try:
            beepocket_name = request.POST['beepocket_name']
            units = request.POST['units']
            starting_balance = request.POST['starting_balance']

            BeePocket.objects.create(beepocket_name=beepocket_name, units=units,
                                    starting_balance=starting_balance, account=account)
            messages.success(
                request, f'BeePocket "{beepocket_name}" created successfully')
            return redirect('manage_account', account_id=account_id)
        except Account.DoesNotExist as e:
            messages.error(request, f'Error: {str(e)}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
    return render(request, 'admin.html', {'account': account})


@login_required
@account_owner_required
def edit_permission(request, account_id, permission_id):
    """
    Edit an existing user permission for a beepocket within an account.
    """
    permission = get_object_or_404(UserPermission, id=permission_id)
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        try:
            permission.user_id = request.POST['user']
            permission.beepocket_id = request.POST['beepocket']
            permission.permission = request.POST['permission']
            permission.save()
            messages.success(request, 'Permission updated successfully')
            return redirect('manage_account', account_id=account_id)
        except (User.DoesNotExist, BeePocket.DoesNotExist, Account.DoesNotExist) as e:
            messages.error(request, f'Error: {str(e)}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
    users = User.objects.all()
    beepockets = BeePocket.objects.all()
    context = {
        'account': account,
        'permission': permission,
        'users': users,
        'beepockets': beepockets,
    }
    return render(request, 'edit_permission.html', context)


@login_required
@account_owner_required
def delete_permission(request, account_id, permission_id):
    """
    Delete an existing user permission for a beepocket within an account.
    """
    try:
        permission = get_object_or_404(UserPermission, id=permission_id)
        permission.delete()
        messages.success(
            request, f'Permission "{permission.permission}" for user "{permission.user.username}" on BeePocket "{permission.beepocket.beepocket_name}"deleted successfully')
    except UserPermission.DoesNotExist as e:
        messages.error(request, f'Error: {str(e)}')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
    return redirect('manage_account', account_id=account_id)


@login_required
@account_owner_required
def edit_beepocket(request, account_id, beepocket_id):
    """ 
    Edit an existing beepocket for an account. 
    """
    beepocket = get_object_or_404(BeePocket, id=beepocket_id)
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        try:
            beepocket.beepocket_name = request.POST['beepocket_name']
            beepocket.units = request.POST['units']
            beepocket.starting_balance = request.POST['starting_balance']
            beepocket.save()
            messages.success(
                request, f'BeePocket "{beepocket.beepocket_name}" updated successfully')
            return redirect('manage_account', account_id=account_id)
        except Account.DoesNotExist as e:
            messages.error(request, f'Error: {str(e)}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}') 
    context = {
        'account': account,
        'beepocket': beepocket,
    }
    return render(request, 'edit_beepocket.html', context)


@login_required
@account_owner_required
def delete_beepocket(request, account_id, beepocket_id):
    """
    Delete an existing beepocket for an account.
    """
    try:
        beepocket = get_object_or_404(BeePocket, id=beepocket_id)
        beepocket.delete()
        messages.success(
            request, f'BeePocket "{beepocket.beepocket_name}" deleted successfully')
    except BeePocket.DoesNotExist as e:
        messages.error(request, f'Error: {str(e)}')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
    return redirect('manage_account', account_id=account_id)
