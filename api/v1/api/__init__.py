from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
from flask import abort
from flasgger import Swagger

from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    swagger = Swagger(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    from .models.user import User
    from .models.review import Review
    from .models.business import Business
    from .models.location import Location
    from .models.category import Category

    @app.route('/api/v1/auth/register', methods=['POST'])
    def register():
        """
    ---
    tags:
      - WeConnect
    parameters:
      - name: username
        in: formData
        type: string
        description: The username
      - name: email
        in: formData
        type: string
        description: user's email
      - name: password
        in: formData
        type: string
        description: user's password
    responses:
      400:
        description: Registration Failed.
      201:
        description: Registration Successful
        schema:
          type: object
          properties:
            message:
              type: string
              description: The result of the operation.
              default: Registration Successful
            User:
              type: object
              properties:
                username:
                  type: string
                  description: Username
                  default: Jim
                email:
                  type: string
                  description: user's email
                  default: jim@jim.com
                createdAt:
                  type: string 
                  description:  time the user registered
                  default: Tue, 27 Feb 2018 11:46:44 GMT
                updatedAt:
                  type: string 
                  description:  last time the user's details were updated
                  default: Tue, 27 Feb 2018 11:46:44 GMT
        """
        response = jsonify({})
        if request.method == "POST":
            user = User.query.filter_by(username=str(request.data['username']), email=str(request.data['email'])).first()
            if not user:
                user = User(username=str(request.data['username']), email=str(request.data['email']))
                user.password=str(request.data['password'])
                user.create()
                user = User.query.filter_by(username=str(request.data['username']), email=str(request.data['email'])).first()
                if user:
                    response = jsonify({'message': 'Registration Successful', 'user':user.get_user_details(user)})
                    response.status_code = 201
                else:
                    response = jsonify({'message': 'Registration Failed.'})
                    response.status_code = 400
            else:
                response = jsonify({'message': 'Registration Failed username or email exist.'})
                response.status_code = 400
        return response

    @app.route('/api/v1/auth/login', methods=['POST'])
    def login():
            """
    ---
    tags:
      - WeConnect
    parameters:
      - name: username
        in: formData
        type: string
        description: The username
      - name: password
        in: formData
        type: string
        description: user's password
    responses:
      400:
        description: Invalid Credentials!
      200:
        description: Login Successful!
        schema:
          type: object
          properties:
            message:
              type: string
              description: The result of the operation.
              default: Login Successful!
            code:
              type: integer
              description: status
              default: 200
            token: 
              type: string
              description: auth token
              default: eyJhbGciOiJIUzI1NiIs
            userId:
              type: integer 
              description:  loged in user's id
              default: 1
        """
            response = jsonify({})
            if  request.method == "POST":
                user = User(username=str(request.data['username']))
                result = user.login(password=str(request.data['password']))
                response = jsonify(result)
                response.status_code = result['code']        
            return response

    @app.route('/api/v1/auth/logout', methods=['POST'])
    def logout():
        response = jsonify({})
        result = auth_check()
        if isinstance(result, str):
            response = jsonify({'message': result})
            response.status_code = 401
        else:
            User.logout(result)
            response = jsonify({'message':'You are now logged out.'})       
            response.status_code = 200
        return response

    @app.route('/api/v1/auth/reset-password', methods=['POST'])
    def password_reset():
        response = jsonify({})
        result = auth_check()
        if isinstance(result, str):
            response = jsonify({'message': result})
            response.status_code = 401
        else:
            if request.method == "POST":
                user = User(username=str(request.data['username']))
                result = user.reset_password(new_password=request.data['password'])
                response = jsonify(result)      
                response.status_code = result['code'] 
        return response

    @app.route('/api/v1/businesses', methods=['POST', 'GET'])
    def businesses():
        response=jsonify({})
        if request.method == "POST":
            result = auth_check()
            if isinstance(result, str):
                response = jsonify({'message': result})
                response.status_code = 401
            else:
                business = Business.query.filter_by(name=str(request.data['name'])).first()
                if not business:
                    categories = [Category.get_category(int(id)) for id in request.data['categories'].split(',')]
                    user = User.get_user(int(request.data['userId']))
                    location = Location.get_location(int(request.data['locationId']))
                    business = Business(name=str(request.data['name']), description=str(request.data['description']), \
                                        user = user, location = location, photo = str(request.data['photo']))
                    for c in categories:
                        if c:
                            business.categories.append(c)
                    business.create()
                    business=Business.query.filter_by(name=str(request.data['name'])).first()
                    if business:
                        response = jsonify(Business.get_business_details(business))       
                        response.status_code = 201
                    else:
                        response = jsonify({'message': 'Failed to create business.'})
                        response.status_code = 400
                else:
                    response = jsonify({'message': 'Business name exists.'})
                    response.status_code = 400
        elif request.method == "GET":
            businesses = Business.get_businesses()
            if len(businesses) > 0:
                businesses = [Business.get_business_details(b) for b in businesses]            
                response = jsonify(businesses)
                response.status_code = 200
            else:
                response = jsonify({'message': 'No businesses to show.'})
                response.status_code = 400
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['PATCH','PUT'])
    def edit_business(businessId):
        response = jsonify({})
        result = auth_check()
        if isinstance(result, str):
            response = jsonify({'message': result})
            response.status_code = 401
        else:
            business = Business.query.filter_by(name=str(request.data['name'])).first()
            if not business:
                business = Business.get_business(businessId)
                user = User.get_user(int(request.data['userId']))
                if business and business.user.id == user.id:
                    location = Location.get_location(int(request.data['locationId']))
                    categories = [Category.get_category(int(id)) for id in request.data['categories'].split(',')]
                    business.name = str(request.data['name'])
                    business.description = str(request.data['description'])
                    business.user = user
                    business.location = location
                    business.photo = str(request.data['photo'])
                    for c in categories:
                        if c:
                            business.categories.append(c)
                    result = business.update()
                    response = jsonify(result)         
                    response.status_code = result['code']
                else:
                    response = jsonify({'message': 'Business does not exist. Or does not belong to you.'})
                    response.status_code = 404
            else:
                response = jsonify({'message': 'Business name exists.'})
                response.status_code = 400
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['DELETE'])
    def delete_business(businessId):
        result = {'message': 'Business not found.'}
        response = jsonify({})
        result = auth_check()
        if isinstance(result, str):
            response = jsonify({'message': result})
            response.status_code = 401
        else:
            response.status_code = 404
            business = Business.get_business(businessId)
            if business and business.user.id == int(request.data['userId']):
                result = business.delete()
                response.status_code = 200
                result = {'message': 'Business successfully deleted.'}
                response = jsonify(result)
            else:
                response = jsonify({'message': 'Business does not exist. Or It does not belong to you.'})
                response.status_code
        return response

    @app.route('/api/v1/businesses/<int:businessId>', methods=['GET'])
    def business_details(businessId):
        response = jsonify({})
        business = Business.get_business(businessId)
        if business:        
            response = jsonify(Business.get_business_details(business)) 
            response.status_code = 200
        else:
            response = jsonify({'message': 'Business not found.'})
            response.status_code = 404
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['POST'])
    def review(businessId):
        result = auth_check()
        if isinstance(result, str):
            response = jsonify({'message': result})
            response.status_code = 401
        else:
            business = Business.get_business(int(businessId))
            user = User.get_user(int(request.data['userId']))
            if business:
                review = Review(comment=str(request.data['comment']), business=business, user=user)
                review.create()
                response = jsonify(Review.get_review_details(review))       
                response.status_code = 201
            else:
                response = jsonify({'message': 'Specified business not found.'})
                response.status_code = 404
        return response

    @app.route('/api/v1/businesses/<int:businessId>/reviews', methods=['GET'])
    def reviews(businessId):
        response = jsonify({'message': 'Business not found.'})
        response.status_code = 404
        business = Business.get_business(businessId)
        if business:
            reviews = business.reviews
            if len(reviews) > 0:
                reviews = [Review.get_review_details(r) for r in reviews]
                response = jsonify(reviews)       
                response.status_code = 200
            else:
                response = {'message': 'No reviews to show.'}
                response.status_code = 404
        return response
    @app.route('/api/v1/categories', methods=['POST'])
    def categories():
        category = Category.query.filter_by(name=str(request.data['name'])).first()
        if not category:
            category = Category(name=str(request.data['name']))
            category.create()
            category = Category.query.filter_by(name=str(request.data['name'])).first()
        response = jsonify(Category.get_categories_details(category))
        return response
    
    @app.route('/api/v1/locations', methods=['POST'])
    def locations():
        location = Location.query.filter_by(name=str(request.data['name'])).first()
        if not location:
            location = Location(name=str(request.data['name']))
            location.create()
            location = Location.query.filter_by(name=str(request.data['name'])).first()
        response = jsonify(Location.get_location_details(location))
        return response

    @app.route('/api/v1/search', methods=['GET'])
    def search():
        q = request.args.get('q')
        response = jsonify({})
        if q is None:
            businesses = [Business.get_business_details(b) for b in Business.query.all()]
            response = jsonify(businesses)
        else:
            businesses = [
               Business.get_business_details(b) for b in Business.query.filter(Business.name.like("%{}%".format(str(q)))).all()
            ]
            response = jsonify(businesses)

        if businesses:
            response.status_code = 200
        else:
            response.status_code = 404
        return response
    
    @app.route('/api/v1/filter/<string:filter>/category', methods=['GET'])
    def category_businesses(filter):
        response = jsonify({})
        if filter:
            businesses = []
            category = Category.query.filter_by(name=str(filter)).first()
            if category:
                businesses = [ Business.get_business_details(b) for b in category.businesses ]
                response.status_code = 200
                response = jsonify(businesses)
            else:
                response.status_code = 404
        else:
            response.status_code = 404
        return response

    @app.route('/api/v1/filter/<string:filter>/location', methods=['GET'])
    def location_businesses(filter):
        response = jsonify({})
        businesses = []
        location = Location.query.filter_by(name=str(filter)).first()
        if filter:
            if location:
                businesses = [Business.get_business_details(b) for b in location.businesses]
                response.status_code = 200
                response = jsonify(businesses)
            else:
                response.status_code = 404
        else:
            response.status_code = 404
        return response


    def auth_check():
        result = 'Token not provided. Please Login And Provide The Token.'
        authorization = request.headers.get('Authorization')
        if authorization is not None:
            token = authorization.split(' ')
            if token[1]:
                result = User.decode_token(token[1])
        return result

    return app
