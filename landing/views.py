from django.shortcuts import render, redirect
from admin_app.models import Account, UserPermission

# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        # Redirect to appropriate page based on user type
        permissions = request.user.userpermission_set.all()
        if any(p.permission == 'manager' for p in permissions):
            return redirect('create_item')
        elif any(p.permission == 'user' for p in permissions):
            return redirect('userpage')
        # Check if user is an account owner
        try:
            account = Account.objects.get(account_owner=request.user)
            return redirect('manage_account', account_id=account.id)
        except Account.DoesNotExist:
            pass
    # Show landing page for unauthenticated users
    return render(request, 'landing.html')