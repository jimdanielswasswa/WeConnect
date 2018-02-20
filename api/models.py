"""Contains All Application Models."""
from datetime import datetime

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
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        """"""
        return '<User : {0} >'.format(self.username)


#ArgumentError: On Business.categories, delete-orphan cascade is not supported on a many-to-many or many-to-one relationship when single_parent is not set.   Set single_parent=True on the relationship().


business_category = db.Table('business_category',
                             db.Column('business_id', db.Integer, db.ForeignKey(
                                 'businesses.id'), primary_key=True),
                             db.Column('category_id', db.Integer, db.ForeignKey(
                                 'categories.id'), primary_key=True)
                             )


class Business(db.Model):
    """"""
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    categories = db.relationship('Category', secondary=business_category,
                                 lazy='subquery', backref=db.backref('businesses', lazy=True))
    reviews = db.relationship('Review', backref='business', lazy=True)
    photo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        """"""
        return '<Business : {0} >'.format(self.name)


class Location(db.Model):
    """"""
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    businesses = db.relationship(
        'Business', backref='location', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        """"""
        return '<Location : {0} >'.format(self.name)


class Category(db.Model):
    """"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        """"""
        return '<Category : {0} >'.format(self.name)


class Review(db.Model):
    """Represents A Review Object."""
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, index=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey(
        'businesses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        """"""
        return "<Review : {}>".format(self.id)
