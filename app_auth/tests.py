import unittest
from django.test import Client
from app_auth.models import User
from faker import Faker
fake = Faker()

# Create your tests here.
class AppAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.all().delete()
        User.objects.create_user(
            "johnwick", 
            "johnwick@mail.com", 
            "mydog1234", 
            first_name=fake.first_name(), 
            last_name=fake.last_name())
        
    def test_register(self):
       
        result = self.client.post('/accounts/register', { 
            'password':'test',
            'email': 'johnwick11@mail.com',
            'full_name': 'John Wick',
            'destination_url': '/accounts/login/'
            })

        self.assertEqual(result.headers['Location'], '/accounts/login/')
        
    def test_login(self):
        result = self.client.post('/accounts/login/', {
            'password':'mydog1234',
            'email': 'johnwick@mail.com',
            'destination_url': '/'
      })
        
        self.assertEqual(result.headers['Location'], '/')
        
        
        
        