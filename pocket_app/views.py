from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_app.models import Account, UserPermission
from pocket_app.models import BeePocket, ItemInstance, Comment


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


@login_required
def userpage(request):
    user = request.user

    # Get all BeePockets the user has access to (either as manager or regular user)
    user_permissions = user.userpermission_set.all()
    accessible_beepockets = [
        permission.beepocket for permission in user_permissions]

    # Default to first BeePocket if available
    selected_beepocket = None
    pollen_items = []
    sting_items = []
    honey_items = []
    show_approved = request.GET.get('show_approved', 'false').lower() == 'true'

    if request.GET.get('beepocket_id'):
        beepocket_id = request.GET.get('beepocket_id')
        for bp in accessible_beepockets:
            if str(bp.id) == beepocket_id:
                selected_beepocket = bp
                break
    elif accessible_beepockets:
        selected_beepocket = accessible_beepockets[0]

    # Calculate balance separately
    balance = calculate_balance(
        selected_beepocket) if selected_beepocket else 0

    # Get item instances for display based on approval status
    if selected_beepocket:
        item_instances = ItemInstance.objects.filter(
            BeePocketID=selected_beepocket,
            Approved=show_approved,
            ActiveStatus=True
        )

        # Group items by type
        for item in item_instances:
            if item.item.item_type == 'Task':  # Pollen/Task (positive)
                pollen_items.append(item)
            # Sting/Consequence (negative)
            elif item.item.item_type == 'Consequence':
                sting_items.append(item)
            elif item.item.item_type == 'Reward':  # Honey/Reward (negative)
                honey_items.append(item)

    context = {
        'beepockets': accessible_beepockets,
        'selected_beepocket': selected_beepocket,
        'balance': balance,
        'pollen_items': pollen_items,
        'sting_items': sting_items,
        'honey_items': honey_items,
        'show_approved': show_approved,
    }

    return render(request, 'pocket.html', context)


def calculate_balance(beepocket):
    if not beepocket:
        return 0

    balance = beepocket.starting_balance

    # Get all approved item instances for this BeePocket for balance calculation
    approved_item_instances = ItemInstance.objects.filter(
        BeePocketID=beepocket,
        Approved=True,
        ActiveStatus=True
    )

    # Calculate balance
    for item in approved_item_instances:
        if item.item.item_type == 'Task':  # Pollen/Task (positive)
            balance += item.item.item_value
        # Sting/Consequence (negative)
        elif item.item.item_type == 'Consequence':
            balance -= item.item.item_value
        elif item.item.item_type == 'Reward':  # Honey/Reward (negative)
            balance -= item.item.item_value
        elif item.item.item_type == 'Adjustment':
            balance += item.item.item_value

    return balance


@login_required
def item_detail(request, item_id):
    item_instance = get_object_or_404(ItemInstance, id=item_id)
    
    # Security check: ensure the user has access to this item's BeePocket
    user_has_access = False
    user_permissions = request.user.userpermission_set.all()
    for permission in user_permissions:
        if permission.beepocket == item_instance.BeePocketID:  # Access BeePocket through BeePocketID
            user_has_access = True
            break

    if not user_has_access:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You do not have access to this item")

    # Handle comment submission
    if request.method == 'POST' and 'comment_text' in request.POST:
        comment_text = request.POST.get('comment_text').strip()
        if comment_text:
            Comment.objects.create(
                ItemInstance=item_instance,
                Comment=comment_text,
                CreatedBy=request.user
            )

    # Get all comments for this item
    comments = Comment.objects.filter(
        ItemInstance=item_instance).order_by('CreatedOn')

    #Get the Beepocket associated with this item instance
    bee_pocket = item_instance.BeePocketID
     
    context = {
        'item': item_instance,
        'comments': comments,
        'bee_pocket': bee_pocket,
    }

    return render(request, 'item_detail.html', context)
