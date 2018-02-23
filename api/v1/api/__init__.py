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

    from .models.user import User
    from .models.review import Review
    from .models.business import Business
    from .models.location import Location
    from .models.category import Category

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
            user = User.get_user(id(request.data.get('userId', 0)))
            response = jsonify(User.get_user_details(user))       
            response.status_code = 200
        elif request.method == "POST":
            user1 = User.get_user((request.data.get('userId', 0)))
            user = User.get_user_details(user1)
            user["password"] = str(request.data.get('password', user1.password))
            response = jsonify({'message':'Password Reset.'})       
            response.status_code = 200
        return response

    @app.route('/api/v1/businesses', methods=['POST', 'GET'])
    def businesses():
        if request.method == "POST":
            categories = Category.get_categories()
            business = Business(name=str(request.data.get('name', '')), description=str(request.data.get('description', '')), \
            user_id=int(request.data.get('userId', '')), location_id=int(request.data.get('locationId', 0)), \
             photo=str(request.data.get('photo', ''))) 
            business.categories=categories
            response = jsonify(Business.get_business(business))       
            response.status_code = 200
        elif request.method == "GET":
            businesses_list = Business.get_businesses()
            businesses = [Business.get_business_details(b) for b in businesses_list]            
            response = jsonify(businesses)
            response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['PATCH','PUT'])
    def edit_business(businessId):
        business = Business.get_business(businessId)
        categories = Category.get_categories()
        business = Business(name=str(request.data.get('name', business.name)), \
         description=str(request.data.get('description', business.description)), user_id=int(request.data.get('userId', 0)), \
         location_id=int(request.data.get('locationId', 0)), photo='logo.jpg') 
        business.categories = []
        business.reviews = business.reviews 
        response = jsonify(Business.get_business_details(business))         
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['DELETE'])
    def delete_business(businessId):
        businesses = Business.get_businesses()
        for bus in businesses:
            if bus.id == int(businessId):
                businesses.remove(bus)
        businesses_list = []
        for bus in businesses:
            businesses_list.append(Business.get_business_details(bus))
        response = jsonify(businesses_list)
        response.status_code = 200

        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['GET'])
    def business_details(businessId):
        business = {}
        businesses_list = Business.get_businesses()
        for bus in businesses_list:
            if bus.id == int(businessId):
                business = Business.get_business_details(bus)
        response = jsonify(business) 
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['POST'])
    def review(businessId):
        review = Review(comment=str(request.data.get('comment', '')))
        review.business_id = int(request.data.get('businessId', 0))
        review.user_id = int(request.data.get('userId', 0))
        response = jsonify(Review.get_review(review))       
        response.status_code = 200
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['GET'])
    def reviews(businessId):
        reviews = []
        reviews_list = Review.get_reviews()
        for review in reviews_list:
            if review.business_id == businessId:
                reviews.append(Review.get_review(review))
        response = jsonify(reviews)       
        response.status_code = 200
        return response

    return app
