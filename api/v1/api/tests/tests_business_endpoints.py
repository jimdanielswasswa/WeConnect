import unittest
import os
import json
import unittest
from flask import request
from flask import jsonify
from flask import abort

from .testbase import TestBase
from api import create_app, db


class TestBusinessEndPoints(TestBase):
    def setUp(self):
        """
        Called before every test
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='postgresql://postgres:root@localhost/weconnect_test'
        )
        with self.app.app_context():
            db.create_all()
        self.user_data = {
            'username': 'jim',
            'email': 'jim@test.com',
            'password': '123'
        }
        self.register_user()
        self.business_data = {
            'name': 'Test', 'description': 'Test', 'userId': 0,
            'locationId': 1, 'categories': '1,2,3', 'photo': 'default.jpg'
        }
        self.review_data = {
            'comment': 'It Works!', 'userId': 0, 'businessId': 0
        }

    def tearDown(self):
        """
        Called after every test
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_business(self):
        """Tests Business Creation."""
        login_res = self.login_user()
        data = self.business_data
        data['userId'] = json.loads(self.login_user().data.decode())['userId']
        response = self.client().post('/api/v1/businesses',
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=data)
        result = json.loads(response.data.decode())
        self.assertTrue(result['name'] == 'Test')
        self.assertEqual(response.status_code, 201)

    def test_get_business(self):
        """Test Business Retrieval."""
        login_res = self.login_user()
        data = self.business_data
        data['userId'] = json.loads(self.login_user().data.decode())['userId']
        response = self.client().post('/api/v1/businesses',
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=data)
        businessId = json.loads(response.data.decode())['id']
        response = self.client().get(
            '/api/v1/businesses/{0}'.format(businessId))
        result = json.loads(response.data.decode())
        self.assertTrue(result['name'] == 'Test')
        self.assertEqual(response.status_code, 200)

    def test_edit_business(self):
        """Test Business Editing."""
        login_res = self.login_user()
        userId = json.loads(self.login_user().data.decode())['userId']
        data = self.business_data
        data['userId'] = userId
        response = self.client().post('/api/v1/businesses',
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=data)
        businessId = json.loads(response.data.decode())['id']
        response = self.client().get(
            '/api/v1/businesses/{0}'.format(businessId)
        )
        data['name'] = 'Test I'
        data['description'] = 'Test'
        data['userId'] = userId
        data['locationId'] = 1
        data['categories'] = '1,2,3'
        data['photo'] = 'default.jpg'
        response = self.client().patch(
            '/api/v1/businesses/{0}'.format(businessId), data=data,
            headers=TestBusinessEndPoints.getheaders(login_res)
        )

        result = json.loads(response.data.decode())
        self.assertTrue(result['business']['name'] == 'Test I')
        self.assertEqual(response.status_code, 200)

    def test_delete_business(self):
        """Test Business Deletion."""
        login_res = self.login_user()
        userId = json.loads(login_res.data.decode())['userId']
        data = self.business_data
        data['userId'] = userId
        response = self.client().post('/api/v1/businesses',
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=data)
        businessId = json.loads(response.data.decode())['id']
        response = self.client().delete(
            '/api/v1/businesses/{0}'.format(businessId), headers=TestBusinessEndPoints.getheaders(login_res),
            data ={'userId': userId}
        )
        result = json.loads(response.data.decode())

        self.assertTrue(result['message'] == 'Business successfully deleted.')
        self.assertEqual(response.status_code, 200)

    def test_create_business_review(self):
        """Tests Review Creation."""
        login_res = self.login_user()
        data = self.business_data
        userId = json.loads(self.login_user().data.decode())['userId']
        data['userId'] = userId
        response = self.client().post('/api/v1/businesses',
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=data)
        businessId = json.loads(response.data.decode())['id']
        review_data = self.review_data
        review_data['userId'] = userId
        review_data['businessId'] = businessId
        response = self.client().post('/api/v1/businesses/{0}/reviews'.format(businessId),
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=review_data)
        result = json.loads(response.data.decode())
        self.assertTrue(result['comment'] == 'It Works!')
        self.assertEqual(response.status_code, 201)

    def test_get_business_reviews(self):
        """Tests Retrieval Of Business Reviews."""
        login_res = self.login_user()
        data = self.business_data
        userId = json.loads(self.login_user().data.decode())['userId']
        data['userId'] = userId
        response = self.client().post('/api/v1/businesses',
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=data)
        businessId = json.loads(response.data.decode())['id']
        review_data = self.review_data
        review_data['userId'] = userId
        review_data['businessId'] = businessId
        response = self.client().post('/api/v1/businesses/{0}/reviews'.format(businessId),
                                      headers=TestBusinessEndPoints.getheaders(login_res), data=review_data)
        response = self.client().get(
            '/api/v1/businesses/{0}/reviews'.format(businessId))
        result = json.loads(response.data.decode())
        self.assertTrue(len(result) == 1)
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def getheaders(login_res):
        headers = dict(
            Authorization="Bearer " +
            json.loads(login_res.data.decode())['token']
        )
        return headers

    def register_user(self):
        return self.client().post('/api/v1/auth/register', data=self.user_data)

    def login_user(self):
        details = {
            'username': self.user_data['username'], 'password': self.user_data['password']
        }
        return self.client().post('/api/v1/auth/login', data=details)


if __name__ == '__main__':
    unittest.main()
