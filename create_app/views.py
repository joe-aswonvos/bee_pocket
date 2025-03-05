from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from admin_app.models import User, BeePocket, UserPermission
from pocket_app.models import Item, Category, ItemInstance

@login_required
def create_item(request):
    user = request.user
    permissions = UserPermission.objects.filter(user=user, permission='manager')
    beepockets = BeePocket.objects.filter(id__in=permissions.values('beepocket'))
    items = Item.objects.filter(createdby=user)
    categories = Category.objects.all()

    if request.method == 'POST':
        item_name = request.POST['item_name']
        item_description = request.POST['item_description']
        item_category_id = request.POST['item_category']
        item_type = request.POST['item_type']
        item_value = request.POST['item_value']
        expireon = request.POST['expireon']

        item_category = get_object_or_404(Category, id=item_category_id)
        Item.objects.create(
            item_name=item_name,
            item_description=item_description,
            item_category=item_category,
            item_type=item_type,
            item_value=item_value,
            createdby=user,
            expireon=expireon
        )
        return redirect('create_item')

    context = {
        'items': items,
        'categories': categories,
        'beepockets': beepockets,
    }
    return render(request, 'create.html', context)

@login_required
def create_item_instance(request):
    if request.method == 'POST':
        item_id = request.POST['item']
        beepocket_id = request.POST['beepocket']

        item = get_object_or_404(Item, id=item_id)
        beepocket = get_object_or_404(BeePocket, id=beepocket_id)
        user = request.user

        ItemInstance.objects.create(
            item=item,
            BeePocketID=beepocket,
            Lasteditedby=user,
            CreatedBy=user
        )
        return redirect('create_item')

@login_required
def item_instances(request, beepocket_id):
    item_instances = ItemInstance.objects.filter(BeePocketID=beepocket_id)
    data = {
        'item_instances': [
            {
                'id': instance.id,
                'item_name': instance.item.item_name,
                'created_by': instance.CreatedBy.username,
                'created_on': instance.CreatedOn.strftime('%Y-%m-%d %H:%M:%S'),
                'active_status': instance.ActiveStatus,
                'approved': instance.Approved
            }
            for instance in item_instances
        ]
    }
    return JsonResponse(data)

@login_required
def approve_item_instance(request, instance_id):
    instance = get_object_or_404(ItemInstance, id=instance_id)
    instance.Approved = True
    instance.save()
    return redirect('create_item')

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.item_name = request.POST['item_name']
        item.item_description = request.POST['item_description']
        item.item_category_id = request.POST['item_category']
        item.item_type = request.POST['item_type']
        item.item_value = request.POST['item_value']
        item.expireon = request.POST['expireon']
        item.save()
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
    return redirect('create_item')

@login_required
def edit_item_instance(request, instance_id):
    instance = get_object_or_404(ItemInstance, id=instance_id)
    if request.method == 'POST':
        instance.item_id = request.POST['item']
        instance.BeePocketID_id = request.POST['beepocket']
        instance.save()
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
    instance.delete()
    return redirect('create_item')