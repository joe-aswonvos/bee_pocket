from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from admin_app.models import Account, BeePocket

User = get_user_model()

class FieldValidationTests(TestCase):
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

    def test_invalid_beepocket_name(self):
        """
        Test that a BeePocket cannot be created with an empty name.
        Success Criteria: The BeePocket is not created and the response status code is not 200.
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_beepocket', args=[self.superuser_account.id]), {
            'beepocket_name': '',
            'units': 'GBP',
            'starting_balance': 200
        })
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(BeePocket.objects.filter(units='GBP', starting_balance=200).exists())

    def test_invalid_starting_balance(self):
        """
        Test that a BeePocket cannot be created with an invalid starting balance.
        Success Criteria: The BeePocket is not created and the response status code is 200 (form re-renders with errors).
        """
        self.client.login(email='superuser@example.com', password='superpassword')
        response = self.client.post(reverse('create_beepocket', args=[self.superuser_account.id]), {
            'beepocket_name': 'Invalid Balance BeePocket',
            'units': 'GBP',
            'starting_balance': 'invalid'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(BeePocket.objects.filter(beepocket_name='Invalid Balance BeePocket').exists())