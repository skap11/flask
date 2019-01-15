from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Resource is a thing which our api is concerned of.
# For example if we want to create and return student, then student is a resource and our student endpoints will be
# responsible for it. Usually mapped to our database tables as well.

items= [
    {
        'name': 'Chair',
        'price': 20
    }
]

app = Flask(__name__) 
app.secret_key = 'shivam' 
api = Api(app) # To allow us to add resources to app. Api works with resources and every resource has to be a class.

jwt = JWT(app, authenticate, identity) # exposes /auth api. 

class Item(Resource):
    
    @jwt_required()
    def get(self, name):
        item = filter(lambda x: x['name'] == name, items) # filter returns a list in python 2.7
        if len(item) > 0:
            return {'item': item[0]}, 200 
        return {'item': None}, 404 # 404 stands for data not found.
    
    @jwt_required() # with python 2.7 it throws exception if the token is not there, with python3.6 it handles and throws custom exception. 
    def post(self, name):
        if len(filter(lambda x: x['name'] == name, items)) > 0:
            return {'errorMessage': 'Resource with name {} already exists.'.format(name)}, 400 # Bad request
        item = {'name': name, 'price': 12}
        items.append(item)
        return item, 201 # 201 stands for created.

    # Put request are called idempotent request,
    # which means even though the thing which we are going to do might already be done, 
    # but it will still execute without failing.  
    def put(self, name):
        pass

    def delete(self, name):
        pass

class Items(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items/')
app.run(port=5000)

