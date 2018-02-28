from datetime import datetime
from datetime import timedelta
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt

from blacklisted_tokens import BlacklistedToken

from api import db

class User(db.Model):
    """"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    businesses = db.relationship(
        'Business', backref='user', lazy='select', cascade='all, delete-orphan')
    reviews = db.relationship(
        'Review', backref='user', lazy='select', cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    @property
    def password(self):
        """"""
        raise AttributeError('Invalid Action. Cannot Get Password.')

    @password.setter
    def password(self, password):
        """"""
        self.password_hash = Bcrypt().generate_password_hash(password).decode()

    def verify_password(self, password):
        """"""
        return Bcrypt().check_password_hash(self.password_hash, password)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def login(self, password):
        user = User.query.filter_by(username=self.username).first()
        result = { 'message': 'Invalid Credentials!', 'code': 400 }
        if user:
            if user.verify_password(password):
                token = self.generate_token(user.id)
                if token:
                    result = {
                        'userId': user.id, 'message': 'Login Successful!', 'code': 200, 'token': token.decode()
                    }
                else:
                    result = { 'message': 'Failed to generate token. Login Failed.', 'code': 400, 'token': '' }
        return result

    @staticmethod
    def logout(token):
        blacklist_token = BlacklistedToken(token=token)
        blacklist_token.save()

    def reset_password(self, new_password):
        user = User.query.filter_by(username=self.username).first()
        result = { 'message': 'User not found.', 'code': 400 }
        if user:
            user.password = new_password
            db.session.commit()
            result={'message': 'Password Reset.', 'code': 200 }
        return result
            

    @staticmethod
    def get_user_details(user):
        if user:
            user_details = {
                "username": user.username, "email": user.email, 'createdAt': user.created_at, 'updatedAt': user.updated_at
            }
        return user_details

    @staticmethod
    def get_user(id):
        user = User.query.get(int(id))
        return user

    @staticmethod
    def get_users():
        users = User.query.all()
        return users

    def generate_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        jwt_byte_string = jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        return jwt_byte_string

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistedToken.check_blacklist(token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
