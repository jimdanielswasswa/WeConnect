from datetime import datetime

class Location(object):
    id = 0
    name = ''
    businesses = []
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self, name):
        self.name = name

def get_location(id):
    locations = get_locations()
    location = {}
    for l in locations:
        location[id] = l.id
        location["name"] = l.name
        location["businesses"] = []

    return location 

def get_locations():
    location1 = Location(name='Kampala')
    location2 = Location(name='Nirobi')
    location1.id = 1
    location1.businesses = []
    location2.id = 1
    location2.businesses = []
    locations = [location1, location2]
    return locations