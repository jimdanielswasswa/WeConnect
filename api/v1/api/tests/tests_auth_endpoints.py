import unittest
from flask import request
from flask import jsonify
from flask import abort
import json

from .testbase import TestBase

class TestAuthEndPoints(TestBase):

    def test_register_user_endpoint(self):
        """
        Test register_user endpoint
        """
        # Test user registration
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Registration Successful")
        self.assertEqual(res.status_code, 201)

    def test_login_endpoint(self):
        """
        Test login endpoint
        """
        # Test User login
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        details = {
            'username': self.user_data['username'], 'password': self.user_data['password']}
        login_res = self.client().post('/api/v1/auth/login', data=details)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "Login Successful!")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['token'])

    def test_password_reset_endpoint(self):
        """
        Test password reset endpoint is not accessible a GET Request
        """
        response = self.client().get('/api/v1/auth/reset-password')
        self.assertEqual(response.status_code, 405)

    def test_logout_endpoint(self):
        """
        Test logout endpoint
        """
        # Test logout endpoint is not accessible with a GET Request
        response = self.client().get('/api/v1/auth/logout')
        self.assertEqual(response.status_code, 405)
        # Test user logout
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)

        details = {
            'username': self.user_data['username'], 'password': self.user_data['password']
        }
        login_res = self.client().post('/api/v1/auth/login', data=details)

        response = self.client().post('/api/v1/auth/logout',
                                      headers=TestAuthEndPoints.getheaders(login_res))
        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == 'You are now logged out.')
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def getheaders(login_res):
        headers = dict(Authorization="Bearer " +
                       json.loads(login_res.data.decode())['token'])
        return headers

if __name__ == '__main__':
    unittest.main()
