from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AccountEndpointsTests(APITestCase):
    def test_registration_login_profile_and_logout(self):
        registration = self.client.post(
            reverse('register'),
            {
                'email': 'amina@example.com',
                'password': 'Un-mot-de-passe-solide-2026!',
                'first_name': 'Amina',
            },
            format='json',
        )
        self.assertEqual(registration.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', registration.data)
        user = User.objects.get(email='amina@example.com')
        self.assertTrue(user.check_password('Un-mot-de-passe-solide-2026!'))

        login = self.client.post(
            reverse('login'),
            {'email': user.email, 'password': 'Un-mot-de-passe-solide-2026!'},
            format='json',
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        token = login.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        profile = self.client.get(reverse('profile'))
        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.data['email'], user.email)
        self.assertNotIn('password', profile.data)

        updated_profile = self.client.patch(
            reverse('profile'), {'tel': '+260970000000'}, format='json'
        )
        self.assertEqual(updated_profile.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_profile.data['tel'], '+260970000000')

        logout = self.client.post(reverse('logout'))
        self.assertEqual(logout.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.client.get(reverse('profile')).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_login_rejects_invalid_credentials(self):
        User.objects.create_user(
            email='amina@example.com', password='Un-mot-de-passe-solide-2026!'
        )
        response = self.client.post(
            reverse('login'),
            {'email': 'amina@example.com', 'password': 'mauvais-mot-de-passe'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_directory_is_not_public(self):
        response = self.client.get('/user/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
