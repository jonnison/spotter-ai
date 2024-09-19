from django.test import TestCase

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from auth.serializers import UserRegisterSerializer

class UserRegisterSerializerTestCase(APITestCase):
    
    def setUp(self):
        # Create a user to test the unique email validator
        self.user = User.objects.create_user(
            username="existinguser",
            email="existingemail@example.com",
            password="Password123"
        )

    def test_valid_data(self):
        data = {
            'username': 'newuser',
            'email': 'newemail@example.com',
            'password': 'a97sd87as987J',
            'password2': 'a97sd87as987J',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])

    def test_password_mismatch(self):
        data = {
            'username': 'newuser',
            'email': 'newemail@example.com',
            'password': 'a97sd87as987J',
            'password2': 'a97sd87as987Js',  # Different password
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], "Password fields didn't match.")

    def test_unique_email_validation(self):
        data = {
            'username': 'anotheruser',
            'email': 'existingemail@example.com',  # Email already exists
            'password': 'Password123',
            'password2': 'Password123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'][0], 'This field must be unique.')

    def test_missing_first_name(self):
        data = {
            'username': 'newuser',
            'email': 'newemail@example.com',
            'password': 'Password123',
            'password2': 'Password123',
            'last_name': 'Doe'  # Missing first name
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('first_name', serializer.errors)

    def test_missing_last_name(self):
        data = {
            'username': 'newuser',
            'email': 'newemail@example.com',
            'password': 'Password123',
            'password2': 'Password123',
            'first_name': 'John',  # Missing last name
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('last_name', serializer.errors)

    def test_password_validation(self):
        data = {
            'username': 'newuser',
            'email': 'newemail@example.com',
            'password': '123',  # Weak password
            'password2': '123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)


