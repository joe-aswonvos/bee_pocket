from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from admin_app.models import Account, BeePocket, UserPermission

User = get_user_model()

class AdminViewTests(TestCase):
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

        # Create an account for the regular user
        self.user_account = Account.objects.create(
            account_name='User Account',
            account_type='Free',
            account_owner=self.user
        )

        # Create a BeePocket for the superuser
        self.beepocket = BeePocket.objects.create(
            beepocket_name='Test BeePocket',
            account=self.superuser_account,
            units='non-currency',
            starting_balance=100
        )

        # Create a UserPermission for the regular user
        self.permission = UserPermission.objects.create(
            user=self.user,
            account=self.superuser_account,
            beepocket=self.beepocket,
            permission='manager'
        )
        
        # Test Create Functionality
        
    def test_create_beepocket(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_beepocket', args=[self.superuser_account.id]), {
            'beepocket_name': 'New BeePocket',
            'account': self.superuser_account.id,
            'units': 'non-currency',
            'starting_balance': 50
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BeePocket.objects.filter(beepocket_name='New BeePocket').exists())

    def test_create_permission(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_permission', args=[self.superuser_account.id]), {
            'user': self.user.id,
            'beepocket': self.beepocket.id,
            'permission': 'user'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserPermission.objects.filter(user=self.user, permission='user').exists())
        
        # Read Tests
        
    def test_read_beepocket(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.get(reverse('edit_beepocket', args=[self.superuser_account.id, self.beepocket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test BeePocket')

    def test_read_permission(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.get(reverse('edit_permission', args=[self.superuser_account.id, self.permission.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'manager')
        
        # Update Tests
    
    def test_update_beepocket(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('edit_beepocket', args=[self.superuser_account.id, self.beepocket.id]), {
            'beepocket_name': 'Updated BeePocket',
            'account': self.superuser_account.id,
            'units': 'non-currency',
            'starting_balance': 150
        })
        self.assertEqual(response.status_code, 302)
        self.beepocket.refresh_from_db()
        self.assertEqual(self.beepocket.beepocket_name, 'Updated BeePocket')

    def test_update_permission(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('edit_permission', args=[self.superuser_account.id, self.permission.id]), {
            'user': self.user.id,
            'beepocket': self.beepocket.id,
            'permission': 'user'
        })
        self.assertEqual(response.status_code, 302)
        self.permission.refresh_from_db()
        self.assertEqual(self.permission.permission, 'user')
        
        # Delete Tests
    
    def test_delete_beepocket(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('delete_beepocket', args=[self.superuser_account.id, self.beepocket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BeePocket.objects.filter(id=self.beepocket.id).exists())

    def test_delete_permission(self):
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('delete_permission', args=[self.superuser_account.id, self.permission.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserPermission.objects.filter(id=self.permission.id).exists())