from datetime import datetime

from api import db
from . business import Business


class Location(db.Model):
    """"""
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    businesses = db.relationship(
        'Business', backref='location', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def create(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """"""
        return '<Location : {0} >'.format(self.name)

    @staticmethod
    def get_location(id):
        location = Location.query.get(int(id))
        return location 

    @staticmethod
    def get_locations():
        locations = Location.query.all()
        return locations
    @staticmethod
    def get_location_details(location):
        if location:
            location_details = { 
                'id': location.id, 'name': location.name, 'createdAt': location.created_at, 'updatedAt': location.updated_at
            }
        return location_details