from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_login_1(self):
        
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(reverse('home'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_2(self):
       
   
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

      
        response = self.client.post(reverse('home'), data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
