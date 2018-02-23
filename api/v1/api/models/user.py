from datetime import datetime

class User(object):
    id = 0
    username = ''
    email = ''
    password = ''
    businesses = []
    reviews = []
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self, username, email):
        self.username = username
        self.email = email
    @staticmethod
    def get_user_details(user):
        return {"username": user.username, "email": user.email}
    @staticmethod
    def get_user(id):
        users = User.get_users()
        user = User(username='', email='')
        for u in users:
            if u.id == id:
                user = u
        return user
    @staticmethod
    def get_users():
        user1 = User(username='Tom', email='tom@cats.com')
        user1.id=1
        user1. password='1234'
        user2 = User(username='Tim', email='tim@cats.com')
        user2.id=2
        user2. password='1234'
        users = [user1, user2]
        return users