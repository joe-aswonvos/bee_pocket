from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from admin_app.models import Account, BeePocket, UserPermission
from pocket_app.models import Item, Category, ItemInstance

User = get_user_model()

class CreateAppTests(TestCase):
    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='superpassword'
        )

        # Create a regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='userpassword'
        )

        # Create an account for the superuser
        self.superuser_account = Account.objects.create(
            account_name='Superuser Account',
            account_type='Free',
            account_owner=self.superuser
        )

        # Create a BeePocket for the superuser
        self.beepocket = BeePocket.objects.create(
            beepocket_name='Test BeePocket',
            account=self.superuser_account,
            units='non-currency',
            starting_balance=100
        )

        # Create a category
        self.category = Category.objects.create(
            category_name='Test Category'
        )

        # Create an item
        self.item = Item.objects.create(
            item_name='Test Item',
            item_description='Test Description',
            item_category=self.category,
            item_type='Task',
            item_value=10,
            createdby=self.superuser
        )

        # Create an item instance
        self.item_instance = ItemInstance.objects.create(
            item=self.item,
            BeePocketID=self.beepocket,
            Lasteditedby=self.superuser,
            CreatedBy=self.superuser,
            expireon=timezone.now() + timedelta(hours=24)
        )
        
    def test_create_item(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_item'), {
            'item_name': 'New Item',
            'item_description': 'New Description',
            'item_category': self.category.id,
            'item_type': 'Task',
            'item_value': 20
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Item.objects.filter(item_name='New Item').exists())

    def test_create_item_instance(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_item_instance'), {
            'select-item': self.item.id,
            'beepocket': self.beepocket.id,
            'expireon': (timezone.now() + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ItemInstance.objects.filter(item=self.item, BeePocketID=self.beepocket).exists())
        
    def test_read_item(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.get(reverse('edit_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')

    def test_read_item_instance(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.get(reverse('edit_item_instance', args=[self.item_instance.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        
    def test_update_item(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('edit_item', args=[self.item.id]), {
            'item_name': 'Updated Item',
            'item_description': 'Updated Description',
            'item_category': self.category.id,
            'item_type': 'Task'
        })
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.item_name, 'Updated Item')
        self.assertEqual(self.item.item_description, 'Updated Description')

    def test_update_item_instance(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('edit_item_instance', args=[self.item_instance.id]), {
            'item': self.item.id,
            'beepocket': self.beepocket.id,
            'expireon': (timezone.now() + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 302)
        self.item_instance.refresh_from_db()
        self.assertEqual(self.item_instance.item.id, self.item.id)
        self.assertEqual(self.item_instance.BeePocketID.id, self.beepocket.id)
        
    def test_delete_item_instance(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('delete_item_instance', args=[self.item_instance.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ItemInstance.objects.filter(id=self.item_instance.id).exists())
        
    def test_delete_item(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        
        response = self.client.post(reverse('delete_item_instance', args=[self.item_instance.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ItemInstance.objects.filter(id=self.item_instance.id).exists())
        
        response = self.client.post(reverse('delete_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

