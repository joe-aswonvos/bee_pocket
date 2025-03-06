from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from admin_app.models import Account, BeePocket, UserPermission

User = get_user_model()

class PermissionTests(TestCase):
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

    def test_create_permission_as_account_owner(self):
        """
        Test that the account owner can create a new permission.
        Success Criteria: The permission is created and the response status code is 302 (redirect).
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_permission', args=[self.superuser_account.id]), {
            'user': self.user.id,
            'beepocket': self.beepocket.id,
            'permission': 'user'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserPermission.objects.filter(user=self.user, beepocket=self.beepocket, permission='user').exists())

    def test_create_permission_as_non_account_owner(self):
        """
        Test that a non-account owner cannot create a new permission.
        Success Criteria: The response status code is 302 (redirect to home).
        """
        self.client.login(email='user@example.com', password='userpassword')
        response = self.client.post(reverse('create_permission', args=[self.superuser_account.id]), {
            'user': self.user.id,
            'beepocket': self.beepocket.id,
            'permission': 'user'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_edit_permission_as_account_owner(self):
        """
        Test that the account owner can edit an existing permission.
        Success Criteria: The permission is updated and the response status code is 302 (redirect).
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('edit_permission', args=[self.superuser_account.id, self.permission.id]), {
            'user': self.user.id,
            'beepocket': self.beepocket.id,
            'permission': 'user'
        })
        self.assertEqual(response.status_code, 302)
        self.permission.refresh_from_db()
        self.assertEqual(self.permission.permission, 'user')

    def test_edit_permission_as_non_account_owner(self):
        """
        Test that a non-account owner cannot edit an existing permission.
        Success Criteria: The response status code is 302 (redirect to home).
        """
        self.client.login(email='user@example.com', password='userpassword')
        response = self.client.post(reverse('edit_permission', args=[self.superuser_account.id, self.permission.id]), {
            'user': self.user.id,
            'beepocket': self.beepocket.id,
            'permission': 'user'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_delete_permission_as_account_owner(self):
        """
        Test that the account owner can delete an existing permission.
        Success Criteria: The permission is deleted and the response status code is 302 (redirect).
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('delete_permission', args=[self.superuser_account.id, self.permission.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserPermission.objects.filter(id=self.permission.id).exists())

    def test_delete_permission_as_non_account_owner(self):
        """
        Test that a non-account owner cannot delete an existing permission.
        Success Criteria: The response status code is 302 (redirect to home).
        """
        self.client.login(email='user@example.com', password='userpassword')
        response = self.client.post(reverse('delete_permission', args=[self.superuser_account.id, self.permission.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_create_beepocket_as_account_owner(self):
        """
        Test that the account owner can create a new BeePocket.
        Success Criteria: The BeePocket is created and the response status code is 302 (redirect).
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_beepocket', args=[self.superuser_account.id]), {
            'beepocket_name': 'New BeePocket',
            'units': 'GBP',
            'starting_balance': 200
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BeePocket.objects.filter(beepocket_name='New BeePocket').exists())

    def test_create_beepocket_as_non_account_owner(self):
        """
        Test that a non-account owner cannot create a new BeePocket.
        Success Criteria: The response status code is 302 (redirect to home).
        """
        self.client.login(email='user@example.com', password='userpassword')
        response = self.client.post(reverse('create_beepocket', args=[self.superuser_account.id]), {
            'beepocket_name': 'New BeePocket',
            'units': 'GBP',
            'starting_balance': 200
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_edit_beepocket_as_account_owner(self):
        """
        Test that the account owner can edit an existing BeePocket.
        Success Criteria: The BeePocket is updated and the response status code is 302 (redirect).
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('edit_beepocket', args=[self.superuser_account.id, self.beepocket.id]), {
            'beepocket_name': 'Updated BeePocket',
            'units': 'EUR',
            'starting_balance': 300
        })
        self.assertEqual(response.status_code, 302)
        self.beepocket.refresh_from_db()
        self.assertEqual(self.beepocket.beepocket_name, 'Updated BeePocket')
        self.assertEqual(self.beepocket.units, 'EUR')
        self.assertEqual(self.beepocket.starting_balance, 300)

    def test_edit_beepocket_as_non_account_owner(self):
        """
        Test that a non-account owner cannot edit an existing BeePocket.
        Success Criteria: The response status code is 302 (redirect to home).
        """
        self.client.login(email='user@example.com', password='userpassword')
        response = self.client.post(reverse('edit_beepocket', args=[self.superuser_account.id, self.beepocket.id]), {
            'beepocket_name': 'Updated BeePocket',
            'units': 'EUR',
            'starting_balance': 300
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_delete_beepocket_as_account_owner(self):
        """
        Test that the account owner can delete an existing BeePocket.
        Success Criteria: The BeePocket is deleted and the response status code is 302 (redirect).
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('delete_beepocket', args=[self.superuser_account.id, self.beepocket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BeePocket.objects.filter(id=self.beepocket.id).exists())

    def test_delete_beepocket_as_non_account_owner(self):
        """
        Test that a non-account owner cannot delete an existing BeePocket.
        Success Criteria: The response status code is 302 (redirect to home).
        """
        self.client.login(email='user@example.com', password='userpassword')
        response = self.client.post(reverse('delete_beepocket', args=[self.superuser_account.id, self.beepocket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))