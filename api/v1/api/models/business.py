from datetime import datetime

from .review import get_review, get_reviews
from .category import get_categories, get_category

class Business(object):
    id = 0
    name = ''
    user_id = 0
    location_id = 0
    categories = []
    reviews = []
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self, name, description, user_id, location_id, photo):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.location_id = location_id
        self.photo = photo

def get_business(id):
    businesses = get_businesses()
    business = Business(name='', description='', user_id=0,location_id=0,photo='')
    for b in businesses:
        if b.id == id:
            business = b
    return business

def get_business_details(business):
    return {'id': business.id, 'name':business.name, 'description': business.description, 'userId':business.user_id, \
         'locationId':business.location_id, 'categories':business.categories, 'photo':business.photo}

def get_businesses():
    bus1 = Business(name='Brothers And Sons', description='Brothers And Sons', user_id=1, location_id=1, photo='logo.jpg') 
    bus1.id=1
    bus1.reviews = get_business_reviews(1)
    bus1.categories = []

    bus2 = Business(name='New Cars', description='Cars', user_id=2, location_id=2, photo='logo.jpg')
    bus2.id=2
    bus2.reviews = get_business_reviews(2)
    bus2.categories = []
    businesses = [bus1, bus2]
    return businesses

def get_business_reviews(id):
    reviews_list = get_reviews()
    reviews = []
    for r in reviews_list:
        if r.business_id == id:
            reviews.append(get_review(r))      
    return reviews

def get_business_categories(ids):
    cats = get_businesses()
    categories = []
    for cat in cats:
        if cat.id in ids:
            categories.append({"id": cat.id, "name": cat.name})
    return categories