from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, OuterRef, Subquery, Exists
from admin_app.models import Account
from pocket_app.models import BeePocket, ItemInstance, Comment, CommentReadStatus
from .utils import calculate_balance


@login_required
def index_page(request):
    """
    Render the index page with the user's account information.
    If the user has an account, include the account ID in the context.
    """
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
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        context = {
            'account_id': None,
        }
    return render(request, 'base.html', context)


@login_required
def userpage(request):
    """
    Render the user page with the BeePockets the user has access to.
    Display item instances grouped by type and calculate the balance.
    """
    user = request.user
    try:
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
            
            # Subquery to check if a comment has been read by the user
            read_status_subquery = Comment.objects.filter(
                ItemInstance=OuterRef('pk')
            ).exclude(
                commentreadstatus__user=user
            ).values('pk')
            
            item_instances = ItemInstance.objects.filter(
                BeePocketID=selected_beepocket,
                Approved=show_approved,
                ActiveStatus=not show_approved
            ).annotate(
                comment_count=Count('comment'),
                has_unread_comments=Exists(read_status_subquery)
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
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        context = {
            'beepockets': [],
            'selected_beepocket': None,
            'balance': 0,
            'pollen_items': [],
            'sting_items': [],
            'honey_items': [],
            'show_approved': False,
        }

    return render(request, 'pocket.html', context)

@login_required
def item_detail(request, item_id):
    """
    Render the item detail page with the item's comments.
    Ensure the user has access to the item's BeePocket and handle comment submission.
    """
    try:
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
        
        # Mark comments as read
        
        for comment in comments:
            read_status, created = CommentReadStatus.objects.get_or_create(comment=comment, user=request.user)
            if not read_status.read:
                read_status.read = True
                read_status.save()
                comment.ReadFlag = True
            else:
                comment.ReadFlag = False

        # Get the Beepocket associated with this item instance
        bee_pocket = item_instance.BeePocketID

        context = {
            'item': item_instance,
            'comments': comments,
            'bee_pocket': bee_pocket,
        }
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        context = {
            'item': None,
            'comments': [],
            'bee_pocket': None,
        }

    return render(request, 'item_detail.html', context)


@login_required
def delete_comment(request, comment_id):
    """
    Delete a comment if the user has permission to do so.
    """
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        item_instance = get_object_or_404(ItemInstance, id=comment.ItemInstance.id)
        beepocket = get_object_or_404(BeePocket, id=item_instance.BeePocketID.id)
        
        if comment.CreatedBy != request.user and request.user != beepocket.manager:
            messages.error(
                request, "You do not have permission to delete this comment.")
            return redirect('item_detail', item_id=comment.ItemInstance.id)

        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    return redirect('item_detail', item_id=comment.ItemInstance.id)

@login_required
def edit_comment(request, comment_id):
    """
    Edit a comment if the user has permission to do so.
    """
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        item_instance = get_object_or_404(ItemInstance, id=comment.ItemInstance.id)
        beepocket = get_object_or_404(BeePocket, id=item_instance.BeePocketID.id)
        
        if comment.CreatedBy != request.user and request.user != beepocket.manager:
            messages.error(request, "You do not have permission to edit this comment.")
            return redirect('item_detail', item_id=comment.ItemInstance.id)
        
        if request.method == 'POST':
            comment_text = request.POST['comment_text']
            comment.Comment = comment_text
            comment.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('item_detail', item_id=comment.ItemInstance.id)
        
        context = {
            'comment': comment,
        }
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        context = {
            'comment': None,
        }
    return render(request, 'edit_comment.html', context)