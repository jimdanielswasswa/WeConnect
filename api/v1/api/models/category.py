from datetime import datetime

class Category(object):    
    id = 0
    name = ''
    businesses = []
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self, name):
        self.name = name

def get_category(id):
    categories = get_categories()
    category = {}
    for c in categories:
        category["id"] = c.id
        category["name"] = c.name
        category["businesses"] = c.businesses
    return category

def get_categories():
    category1 = Category(name='Retail')
    category2 = Category(name='Whole Sale')
    category1.id = 1
    category1.businesses = []
    category2.id = 2
    category2.businesses = []
    categories = [category1, category2]
    return categories