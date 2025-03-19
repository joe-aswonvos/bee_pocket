from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelformset_factory
from django.db.models import Count, Exists, OuterRef
from datetime import timedelta
from admin_app.models import BeePocket, UserPermission, Account
from pocket_app.models import Item, Category, ItemInstance, CommentReadStatus, Comment


@login_required
def create_item(request):
    user = request.user
    try:
        # Get the first account owned by the user
        account = Account.objects.filter(account_owner=user).first()
        if account:
            account_id = account.id
        else:
            account_id = None
    except Exception as e:
        print(f"Error retrieving account: {str(e)}")
        account_id = None

    permissions = UserPermission.objects.filter(
        user=user, permission='manager')
    beepockets = BeePocket.objects.filter(
        id__in=permissions.values('beepocket'))

    # Get default beepocket (first active one)
    default_beepocket = None
    if beepockets.exists():
        default_beepocket = beepockets.first()

    items = Item.objects.filter(createdby=user)
    categories = Category.objects.all()

    CategoryFormSet = modelformset_factory(
        Category, fields=('category_name',), extra=1)
    formset = CategoryFormSet(queryset=Category.objects.none())

    if request.method == 'POST':
        item_name = request.POST['item_name']
        item_description = request.POST['item_description']
        item_category_id = request.POST['item_category']
        item_type = request.POST['item_type']
        item_value = request.POST['item_value']

        formset = CategoryFormSet(request.POST)

        if formset.is_valid():
            formset.save()

        if item_category_id == 'new':
            new_category_name = request.POST['new_category_name']
            item_category, created = Category.objects.get_or_create(
                category_name=new_category_name)
        else:
            item_category = get_object_or_404(Category, id=item_category_id)

        Item.objects.create(
            item_name=item_name,
            item_description=item_description,
            item_category=item_category,
            item_type=item_type,
            item_value=item_value,
            createdby=user,
        )
        messages.success(request, f'Item "{item_name}" created successfully')
        return redirect('create_item')

    context = {
        'items': items,
        'categories': categories,
        'beepockets': beepockets,
        'default_beepocket': default_beepocket,
        'account_id': account_id,
        'formset': formset,
    }
    return render(request, 'create.html', context)


@login_required
def create_item_instance(request):
    if request.method == 'POST':
        item_id = request.POST.get('select-item')
        beepocket_id = request.POST.get('beepocket')
        expireon = request.POST.get(
            'expireon', (timezone.now() + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M'))

        item = get_object_or_404(Item, id=item_id)
        beepocket = get_object_or_404(BeePocket, id=beepocket_id)
        user = request.user

        item_instance = ItemInstance.objects.create(
            item=item,
            BeePocketID=beepocket,
            Lasteditedby=user,
            CreatedBy=user,
            expireon=expireon
        )

        if item.item_type == 'Adjustment':
            approve_item_instance(request, item_instance.id)
            messages.success(
                request, f'Adjustment "{item.item_name}" in "{beepocket}" instance created and approved successfully'
            )

        else:
            messages.success(
                request, f'New "{item.item_name}" in "{beepocket}" instance created successfully'
            )

        return redirect('create_item')


@login_required
def item_instances(request, beepocket_id):
    user = request.user

    unread_comments_subquery = Comment.objects.filter(
        ItemInstance=OuterRef('pk')
    ).exclude(
        commentreadstatus__user=user
    ).values('pk')

    item_instances = ItemInstance.objects.filter(BeePocketID=beepocket_id).annotate(
        comment_count=Count('comment'),
        has_unread_comments=Exists(unread_comments_subquery)
    )

    data = {
        'item_instances': [
            {
                'id': instance.id,
                'item_name': instance.item.item_name,
                'created_by': instance.CreatedBy.username,
                'created_on': instance.CreatedOn.strftime('%Y-%m-%d %H:%M:%S'),
                'active_status': instance.ActiveStatus,
                'approved': instance.Approved,
                'comment_count': instance.comment_count,
                'has_unread_comments': instance.has_unread_comments
            }
            for instance in item_instances
        ]
    }
    return JsonResponse(data)


@login_required
def approve_item_instance(request, instance_id):
    instance = get_object_or_404(ItemInstance, id=instance_id)
    instance.Approved = True
    instance.ApprovedOn = timezone.now()
    instance.ActiveStatus = False
    instance.ApprovedBy = request.user
    instance.save()    
    messages.success(
        request, f'"{instance.item.item_name}" approved successfully')
    return redirect('create_item')


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.item_name = request.POST['item_name']
        item.item_description = request.POST['item_description']
        item.item_category_id = request.POST['item_category']
        item.item_type = request.POST['item_type']
        item.save()
        messages.success(request, f'"{item.item_name}" updated successfully')
        return redirect('create_item')
    categories = Category.objects.all()
    context = {
        'item': item,
        'categories': categories,
    }
    return render(request, 'edit_item.html', context)


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect('create_item')


@login_required
def edit_item_instance(request, instance_id):
    instance = get_object_or_404(ItemInstance, id=instance_id)
    beepocket = get_object_or_404(BeePocket, id=instance.BeePocketID.id)
    if request.method == 'POST':
        instance.item_id = request.POST['item']
        instance.BeePocketID_id = request.POST['beepocket']
        instance.expireon = request.POST['expireon']
        instance.save()
        messages.success(
            request, f'"{instance.item.item_name}" in "{beepocket}" updated successfully')
        return redirect('create_item')
    items = Item.objects.all()
    beepockets = BeePocket.objects.all()
    context = {
        'instance': instance,
        'items': items,
        'beepockets': beepockets,
    }
    return render(request, 'edit_item_instance.html', context)


@login_required
def delete_item_instance(request, instance_id):
    instance = get_object_or_404(ItemInstance, id=instance_id)
    beepocket = get_object_or_404(BeePocket, id=instance.BeePocketID.id)
    instance.delete()
    messages.success(
        request, f'"{instance.item.item_name}" in "{beepocket}" deleted successfully')
    return redirect('create_item')

@login_required
def new_item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    data = {
        'description': item.item_description,
        'category': item.item_category.category_name,
        'type': item.item_type,
        'value': item.item_value,
    }
    return JsonResponse(data)