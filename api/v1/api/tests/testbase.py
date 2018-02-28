import unittest
import os

from api import create_app, db

class TestBase(unittest.TestCase):

    def setUp(self):
        """
        Called before every test
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='postgresql://postgres:@localhost/weconnect_test'
        )
        with self.app.app_context():
            db.create_all()
        self.user_data = {
            'username': 'jim',
            'email': 'jim@test.com',
            'password': '123'
        }

    def tearDown(self):
        """
        Called after every test
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
