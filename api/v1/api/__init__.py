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

    from .models.user import User, get_user_details, get_user
    from .models.review import Review, get_review, get_reviews
    from .models.business import Business, get_business, get_business_details, get_business_reviews, get_businesses, get_business_categories
    from .models.location import Location, get_location, get_locations
    from .models.category import Category, get_categories, get_category

    @app.route('/api/v1/auth/register', methods=['GET', 'POST'])
    def register():
        if request.method == "GET":
            response = jsonify({})
            response.status_code = 200
        elif request.method == "POST":
            user = User(username=str(request.data.get('username', '')), email=str(request.data.get('email', '')))
            user.password=str(request.data.get('password', ''))
            response = jsonify({'message': 'Registration Successful', 'username':user.username})
            response.status_code = 200
        return response

    @app.route('/api/v1/auth/login', methods=['GET', 'POST'])
    def login():
        if request.method == "GET":
            response = jsonify({})       
            response.status_code = 200
        elif request.method == "POST":
            user = User(username=str(request.data.get('username', '')), email=str(request.data.get('email', '')))
            user.id = 3
            user.password='1234'
            message = ''
            if user.username.lower() == str(request.data.get('username', '')).lower() and user.password == str(request.data.get('password', '')):
                message = 'Login Successful!'
            else:
                message = 'Invalid Credentials.'
            response = jsonify({'message':message})
            response.status_code = 200
        
        return response

    @app.route('/api/v1/auth/logout', methods=['POST'])
    def logout(): 
        response = jsonify({'message':'You are now logged out.'})       
        response.status_code = 200
        return response

    @app.route('/api/v1/auth/reset-password', methods=['GET', 'POST'])
    def password_reset():
        if request.method == "GET":
            user = get_user(id(request.data.get('userId', 0)))
            response = jsonify(get_user_details(user))       
            response.status_code = 200
        elif request.method == "POST":
            user1 = get_user((request.data.get('userId', 0)))
            user = get_user_details(user1)
            user["password"] = str(request.data.get('password', user1.password))
            response = jsonify({'message':'Password Reset.'})       
            response.status_code = 200
        return response

    @app.route('/api/v1/businesses', methods=['POST', 'GET'])
    def businesses():
        if request.method == "POST":
            categories = get_categories()
            business = Business(name=str(request.data.get('name', '')), description=str(request.data.get('description', '')), \
            user_id=int(request.data.get('userId', '')), location_id=int(request.data.get('locationId', 0)), \
             photo=str(request.data.get('photo', ''))) 
            business.categories=categories
            response = jsonify(get_business(business))       
            response.status_code = 200
        elif request.method == "GET":
            businesses_list = get_businesses()
            businesses = [get_business_details(b) for b in businesses_list]            
            response = jsonify(businesses)
            response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['PATCH','PUT'])
    def edit_business(businessId):
        business = get_business(businessId)
        categories = get_categories()
        business = Business(name=str(request.data.get('name', business.name)), \
         description=str(request.data.get('description', business.description)), user_id=int(request.data.get('userId', 0)), \
         location_id=int(request.data.get('locationId', 0)), photo='logo.jpg') 
        business.categories = []
        business.reviews = business.reviews 
        response = jsonify(get_business_details(business))         
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['DELETE'])
    def delete_business(businessId):
        businesses = get_businesses()
        for bus in businesses:
            if bus.id == int(businessId):
                businesses.remove(bus)
        businesses_list = []
        for bus in businesses:
            businesses_list.append(get_business_details(bus))
        response = jsonify(businesses_list)
        response.status_code = 200

        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['GET'])
    def business_details(businessId):
        business = {}
        businesses_list = get_businesses()
        for bus in businesses_list:
            if bus.id == int(businessId):
                business = get_business_details(bus)
        response = jsonify(business) 
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['POST'])
    def review(businessId):
        review = Review(comment=str(request.data.get('comment', '')))
        review.business_id = int(request.data.get('businessId', 0))
        review.user_id = int(request.data.get('userId', 0))
        response = jsonify(get_review(review))       
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['GET'])
    def reviews(businessId):
        reviews = []
        reviews_list = get_reviews()
        for review in reviews_list:
            if review.business_id == businessId:
                reviews.append(get_review(review))
        response = jsonify(reviews)       
        response.status_code = 200
        return response

    return app
