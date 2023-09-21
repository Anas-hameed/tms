"""Testing case for the user route"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserTests(APITestCase):
    """This file test all the user related routes"""

    def setUp(self):
        """setup for the test cases, create a test user"""
        self.url = '/api/v0.1/user/'
        self.data = {
            'username': 'danyal.faheem',
            'email': 'danyal.faheem@gmail.com',
            'password': 'anas001',
            'role': 'Trainer',
        }
        self.response = self.client.post(self.url, self.data)
        self.response_user = {
            'id': 1,
            'first_name': '',
            'last_name': '',
            'username': 'danyal.faheem',
            'email': 'danyal.faheem@gmail.com',
            'role': 'Trainer',
            'profile': {
                'id': 1,
                'gender': 'none',
                'bio': '',
                'user': 1,
            },
        }

    def test_create_user(self):
        """testing creation of the user"""
        self.response_user['profile'][
            'profile_image'
        ] = 'http://testserver/images/man.png'
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.data, self.response_user)

    def test_get_token(self):
        """this is to test getting JWT token from token endpoint"""
        url = reverse('api_token_auth')
        response = self.client.post(
            url, {'username': self.data['email'], 'password': self.data['password']}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_user(self):
        """test the user get route for the tms app"""
        self.response_user['profile']['profile_image'] = '/images/man.png'
        response = self.client.login(
            username=self.data['email'], password=self.data['password']
        )
        url = '/api/v0.1/user/me/'
        response = self.client.get(url)
        self.assertEqual(self.response_user, response.data)
        self.client.logout()

    def test_get_list(self):
        """This function test the get list user method"""
        url = '/api/v0.1/user/'
        response = self.client.get(url)
        self.assertEqual(1, len(response.data))

    def test_user_me(self):
        """This function test the user me route"""
        self.response_user['profile']['profile_image'] = '/images/man.png'
        self.client.login(username=self.data['email'], password=self.data['password'])
        response = self.client.get('/api/v0.1/user/me/')
        self.assertDictContainsSubset(self.response_user, response.data)

    def test_update_user(self):
        """This function testing the update user"""
        self.response_user['profile'][
            'profile_image'
        ] = 'http://testserver/images/man.png'
        self.response_user['username'] = 'anas.hameed'
        self.client.login(username=self.data['email'], password=self.data['password'])
        response = self.client.patch('/api/v0.1/user/1/', {'username': 'anas.hameed'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictContainsSubset(self.response_user, response.data)

    def test_delete_user(self):
        """This function test the delete user functionality"""
        self.client.login(username=self.data['email'], password=self.data['password'])
        response = self.client.delete('/api/v0.1/user/1/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
