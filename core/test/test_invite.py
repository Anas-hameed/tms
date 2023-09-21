"""This module contain test cases for the invite follow"""

from rest_framework.test import APITestCase
from rest_framework import status


class InviteTests(APITestCase):
    """This file test all the training related routes"""

    def setUp(self):
        """setup for the test cases, create a test user"""
        self.client.post(
            '/api/v0.1/user/',
            {
                'username': 'danyal.faheem',
                'email': 'danyal.faheem@gmail.com',
                'password': 'anas001',
                'role': 'Trainer',
            },
        )
        self.client.login(username='danyal.faheem@gmail.com', password='anas001')
        training_url = '/api/v0.1/trainingplan/'
        self.response_training = self.client.post(
            training_url,
            {
                'name': 'Learning django is Fun',
                'description': 'Complete learning plan for django and django rest framework',
            },
        )
        self.invite_data = {'email': 'anas.hameed@arbisoft.com'}
        self.invite_response = self.client.post(
            '/api/v0.1/trainingplan/1/invites/', self.invite_data
        )

    def test_create_invite(self):
        """testing creation of the training"""
        self.assertEqual(status.HTTP_201_CREATED, self.invite_response.status_code)
        self.assertDictContainsSubset(self.invite_data, self.invite_response.data)

    def test_get_invite(self):
        """test the training get route for the tms app"""
        response = self.client.get('/api/v0.1/trainingplan/1/invites/1/')
        self.assertDictContainsSubset(self.invite_data, response.data)

    def test_get_list(self):
        """This function test the get list of training invite method"""
        response = self.client.get('/api/v0.1/trainingplan/1/invites/')
        self.assertEqual(1, len(response.data))

    def test_delete_training(self):
        """testing for the update route"""
        response = self.client.delete('/api/v0.1/trainingplan/1/invites/1/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
