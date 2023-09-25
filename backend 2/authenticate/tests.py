from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from rest_framework import status

# Create your tests here.

class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('signup')

    # test to create valid user
    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'signup': {
                'username': 'foobar',
                'email': 'foobar@example.com',
                'password1': 'somepassword',
                'password2': 'somepassword'
            }
           
        }

        response = self.client.post(self.create_url , data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['registered'], True)
        self.assertFalse('password1' in response.data)
        # test there's no form errors
        self.assertEqual(len(response.data['form-errors']), 0)


    # test for short password
    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
            'signup': {
                'username': 'foo' ,
                'email': 'foo@gmail.com',
                'password1': 'any',
                'password2': 'any'
            }
           
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['form-errors']), 1)


    # test with no password
    def test_create_user_with_no_password(self):
        data = {
            'signup': {
                'username': 'foobar',
                'email': 'foobar@example.com',
                'password1': '',
                'password2': ''
            }
           
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['registered'], False)
        # both password fields not filled in
        self.assertEqual(len(response.data['form-errors']), 2)

    # test with no username
    def test_create_user_with_no_username(self):
        data = {
            'signup': {
                'username': '',
                'email': 'foobar@example.com',
                'password1': 'anywhere123',
                'password2': 'anywhere123'
            }
           
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['registered'], False)
        # username field is not filled in
        self.assertEqual(len(response.data['form-errors']), 1)

    # test with existing username
    def test_create_user_with_existing_username(self):
        data = {
            'signup': {
                'username': 'testuser',
                'email': 'foobar@example.com',
                'password1': 'anywhere123',
                'password2': 'anywhere123'
            }
           
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['registered'], False)
        # username field is not filled in
        self.assertEqual(len(response.data['form-errors']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'signup': {
                'username': 'foo' ,
                'email': 'test@example.com',
                'password1': 'anywhere123',
                'password2': 'anywhere123'
            }
           
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['form-errors']), 1)

    # test with invalid email
    def test_create_user_with_invalid_email(self):
        data = {
            'signup': {
                'username': 'foo' ,
                'email': 'user.com',
                'password1': 'anywhere123',
                'password2': 'anywhere123'
            }
           
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['form-errors']), 1)

    # test with no email
    def test_create_user_with_no_email(self):
        data = {
            'signup': {
                'username': 'foo' ,
                'email': '',
                'password1': 'anywhere123',
                'password2': 'anywhere123'
            }
           
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['form-errors']), 1)
