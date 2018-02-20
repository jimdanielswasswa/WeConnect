from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from flask import request
from flask import abort

from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from .models import Business, Category, Location, Review,User

    @app.route('/api/v1/auth/register', methods=['GET'])
    def get_register():
        response = jsonify({})
        response.status_code = 200
        return response

    @app.route('/api/v1/auth/register', methods=['POST'])
    def post_register(): 
        user = User(username=str(request.data.get('username', '')), email=str(request.data.get('email', '')), password_hash=str(request.data.get('password', '')))
        response = jsonify({'message': 'Registration Successful', 'username':user.username})
        response.status_code = 200
        return response

    @app.route('/api/v1/auth/login', methods=['GET'])
    def get_login():
        response = jsonify({})       
        response.status_code = 200
        return response

    @app.route('/api/v1/auth/login', methods=['POST'])
    def post_login(): 
        user = User(id=1, username='Tom', email='tom@cats.com', password_hash='1234')
        message = ''
        if user.username.lower() == str(request.data.get('username', '')).lower() and user.password_hash == str(request.data.get('password', '')):
            message = 'Login Successful!'
        else:
            message = 'Invalid Credentials.'
        response = jsonify({'message':message})
        response.status_code = 200
        return response

    @app.route('/api/v1/auth/logout', methods=['POST'])
    def post_logout(): 
        response = jsonify({'message':'You are now logged out.'})       
        response.status_code = 200
        return response

    @app.route('/api/v1/auth/reset-password', methods=['GET'])
    def get_password_reset():
        user = User(id=1, username='Tom', email='tom@cats.com')
        response = jsonify({'userId':user.id, 'username':user.username, 'email':user.email})       
        response.status_code = 200
        return response

    @app.route('/api/v1/auth/reset-password', methods=['POST'])
    def post_password_reset():
        user = User(id=1, username='Tom', email='tom@cats.com')
        user.password_hash = str(request.data.get('password', user.password_hash))
        response = jsonify({'message':'Password Reset.'})       
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses', methods=['POST'])
    def post_business():
        categories = Category(id=1, name='Retail')
        location = Location(id=1, name='Kampala')
        business = Business(name=str(request.data.get('name', '')), description=str(request.data.get('description', '')), \
        user_id=int(request.data.get('userId', '')), location=location,\
         categories=[categories], photo=str(request.data.get('photo', ''))) 
        response = jsonify({'name':business.name, 'description':business.description, 'userId':business.user_id, \
         'locationId':business.location.id, 'categories':business.categories[0].id, 'photo':business.photo})       
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['PATCH','PUT'])
    def edit_business(businessId):
        business = Business()
        categories = Category(id=1, name='Retail')
        location = Location(id=1, name='Kampala')
        businesses_list = []
        bus1 = Business(id=1, name='Brothers And Sons', description='Brothers And Sons', user_id=1, location=location, categories=[categories], \
         photo='logo.jpg') 
        bus2 = Business(id=2, name='New Cars', description='Cars', user_id=1, location=location, categories=[categories], photo='logo.jpg')
        user = User(id=1, username='Tom', email='tom@cats.com', password_hash='1234')
        businesses_list.append(bus1)
        businesses_list.append(bus2)
        for bus in businesses_list:
            if bus.id == int(businessId):
                business = bus
        business = Business(name=str(request.data.get('name', business.name)), description=str(request.data.get('description', business.description)), \
        user_id=int(request.data.get('userId', business.user_id)), location=location,\
        categories=[categories], photo=str(request.data.get('photo', business.photo))) 

        response = jsonify({'name':business.name, 'description':business.description, 'userId':business.user_id, \
         'locationId':business.location.id, 'categories':business.categories[0].id, 'photo':business.photo})         
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['DELETE'])
    def delete_business(businessId):
        businesses = {}
        categories = Category(id=1, name='Retail')
        location = Location(id=1, name='Kampala')
        businesses_list = []
        bus1 = Business(id=1, name='Brothers And Sons', description='Brothers And Sons', user_id=1, location=location, categories=[categories], \
         photo='logo.jpg') 
        bus2 = Business(id=2, name='New Cars', description='Cars', user_id=1, location=location, categories=[categories], photo='logo.jpg')
        user = User(id=1, username='Tom', email='tom@cats.com', password_hash='1234')
        businesses_list.append(bus1)
        businesses_list.append(bus2)
        for bus in businesses_list:
            if bus.id == int(businessId):
                businesses_list.remove(bus)
        for business in businesses_list:
            businesses[business.id] = { 'name' : business.name, 'description' : business.description }

        response = jsonify(businesses)
        response.status_code = 200

        return response

    @app.route('/api/v1/businesses', methods=['GET'])
    def get_businesses():
        businesses = {}
        categories = Category(id=1, name='Retail')
        location = Location(id=1, name='Kampala')
        businesses_list = []
        bus1 = Business(id=1, name='Brothers And Sons', description='Brothers And Sons', user_id=1, location=location, categories=[categories], \
         photo='logo.jpg') 
        bus2 = Business(id=2, name='New Cars', description='Cars', user_id=1, location=location, categories=[categories], photo='logo.jpg')
        user = User(id=1, username='Tom', email='tom@cats.com', password_hash='1234')
        businesses_list.append(bus1)
        businesses_list.append(bus2)
        for business in businesses_list:
            businesses[business.id] = { 'name' : business.name, 'description' : business.description }

        response = jsonify(businesses)
        response.status_code = 200

        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['GET'])
    def get_business(businessId):
        business = Business()
        categories = Category(id=1, name='Retail')
        location = Location(id=1, name='Kampala')
        businesses_list = []
        bus1 = Business(id=1, name='Brothers And Sons', description='Brothers And Sons', user_id=1, location=location, categories=[categories], \
         photo='logo.jpg') 
        bus2 = Business(id=2, name='New Cars', description='Cars', user_id=1, location=location, categories=[categories], photo='logo.jpg')
        user = User(id=1, username='Tom', email='tom@cats.com', password_hash='1234')
        businesses_list.append(bus1)
        businesses_list.append(bus2)
        for bus in businesses_list:
            if bus.id == int(businessId):
                business = bus
        response = jsonify({'id': business.id, 'name':business.name, 'description': business.description, 'userId':business.user_id, \
         'locationId':business.location.id, 'categories':business.categories[0].id, 'photo':business.photo}) 
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['POST'])
    def post_review(businessId):
        categories = Category(id=1, name='Retail')
        location = Location(id=1, name='Kampala')
        business = Business(id=1, name='Brothers And Sons', description='Brothers And Sons', \
        user_id=1, location=location,\
         categories=[categories], photo='logo.jpg') 
        user = User(id=1, username='Tom', email='tom@cats.com', password_hash='1234', businesses=[business])
        review = Review(comment=str(request.data.get('comment', '')), user=user, business=business)
        response = jsonify({'comment':review.comment, 'userId':review.user.id, 'businessId':business.id})       
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['GET'])
    def get_review(businessId):
        reviews_dict = {}
        businesses = []
        categories = Category(id=1, name='Retail')
        location = Location(id=1, name='Kampala')
        user = User(id=1, username='Tom', email='tom@cats.com', password_hash='1234')
        bus1 = Business(id=1, name='Brothers And Sons', description='Brothers And Sons', user_id=1, location=location, categories=[categories], \
         photo='logo.jpg') 
        bus2 = Business(id=2, name='New Cars', description='Cars', user_id=1, location=location, categories=[categories], photo='logo.jpg' )
        businesses.append(bus1)
        businesses.append(bus2)
        review1 = Review(id=1, comment='This is Awsome!', user=user, business=bus1)
        review2 = Review(id=2, comment='This is Amaizing!', user=user, business=bus2)
        for bus in businesses:
            if bus.id == int(businessId):
                business = bus
        for r in business.reviews:
            reviews_dict[r.id] = {'comment':r.comment, 'userId':r.user.id, 'businessId':r.business.id}
        response = jsonify(reviews_dict)       
        response.status_code = 200
        return response

    return app
