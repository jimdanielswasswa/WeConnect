from datetime import datetime

from api import db

from .category import Category
from .review import Review

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


    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        business = Business.query.get(self.id)
        result = { 
            'message': 'Business updated successfully.', 'code': 200, 'business': Business.get_business_details(business) 
            }
        return result
    def delete(self):
        db.session.delete(self)
        db.session.commit()        
        

    @staticmethod
    def get_business(id):
        business = Business.query.get(int(id))
        return business

    @staticmethod
    def get_business_details(business):
        categories = [ Category.get_categories_details(c) for c in business.categories ]
        return {'id': business.id, 'name':business.name, 'description': business.description, 'userId':business.user_id, \
            'locationId':business.location_id, 'categories':categories, 'photo':business.photo}

    @staticmethod
    def get_businesses():
        businesses = Business.query.all()
        return businesses

    def __repr__(self):
        """"""
        return '<Business : {0} >'.format(self.name)
