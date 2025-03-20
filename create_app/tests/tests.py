from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from pocket_app.models import Item, Category

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
            item_value=10
        )
        
        # Create Functionality Tests
        
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
        
        #Read Tests
        
    def test_read_item(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.get(reverse('edit_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        
        # Update Tests
        
    def test_update_item(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('edit_item', args=[self.item.id]), {
            'item_name': 'Updated Item',
            'item_description': 'Updated Description',
            'item_category': self.category.id,
            'item_type': 'Task'
            # Remove 'item_value' field to prevent changing it
        })
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.item_name, 'Updated Item')
        self.assertEqual(self.item.item_description, 'Updated Description')
        
        # Delete Tests
        
    def test_delete_item(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('delete_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())