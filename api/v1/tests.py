import unittest
import os
import json
import unittest
from flask import request
from flask import jsonify
from flask import abort

from api import create_app, db


class TestBase(unittest.TestCase):

    def setUp(self):
        """
        Called before every test
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

    def tearDown(self):
        """
        Called after every test
        """
        pass

class TestEndPoints(TestBase):

    def test_login_endpoint(self):
        """
        Test login endpoint accessible without login
        """
        response = self.client().get('/api/v1/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_logout_endpoint(self):
        """
        Test logout endpoint is not accessible with a GET Request
        """
        response = self.client().get('/api/v1/auth/logout')
        self.assertEqual(response.status_code, 405)

    def test_register_user_endpoint(self):
        """
        Test register_user is accessible without login
        """
        response = self.client().get('/api/v1/auth/register')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_endpoint(self):
        """
        Test password reset endpoint is accessible without login
        """
        response = self.client().get('/api/v1/auth/reset-password')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
