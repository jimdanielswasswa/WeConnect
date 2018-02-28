from datetime import datetime

from api import db


class Category(db.Model):
    """"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def create(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """"""
        return '<Category : {0} >'.format(self.name)

    @staticmethod
    def get_category(id):
        category = Category.query.get(int(id))
        return category

    @staticmethod
    def get_categories():
        categories = Category.query.all()
        return categories
    @staticmethod
    def get_categories_details(category):
        return { 
            'id': category.id, 'name': category.name, 'createdAt': category.created_at, 'updatedAt': category.updated_at
         }
