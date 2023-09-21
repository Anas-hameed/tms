"""test case for the training routes"""

from rest_framework.test import APITestCase
from rest_framework import status


class TrainingPlanTests(APITestCase):
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
        self.trainig_data = {
            'name': 'Learning django is Fun',
            'description': 'Complete learning plan for django and django rest framework',
        }
        self.response_training = self.client.post(training_url, self.trainig_data)

    def test_create_training(self):
        """testing creation of the training"""
        self.assertEqual(self.response_training.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(self.trainig_data, self.response_training.data)

    def test_get_training(self):
        """test the training get route for the tms app"""
        response = self.client.get('/api/v0.1/trainingplan/1/')
        self.assertDictContainsSubset(self.trainig_data, response.data)

    def test_get_list(self):
        """This function test the get list training method"""
        response = self.client.get('/api/v0.1/trainingplan/')
        self.assertEqual(1, len(response.data))

    def test_update_training(self):
        """testing for the update route"""
        self.trainig_data['name'] = 'update name'
        response = self.client.patch(
            '/api/v0.1/trainingplan/1/', {'name': 'update name'}
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictContainsSubset(self.trainig_data, response.data)

    def test_delete_training(self):
        """testing for the update route"""
        response = self.client.delete('/api/v0.1/trainingplan/1/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
