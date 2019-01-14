from flask import Flask, jsonify
from flask_restful import Resource, Api

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

api = Api(app) # To allow us to add resources to app. Api works with resources and every resource has to be a class.

class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'errorMessage': 'Resource with name {} was not found.'.format(name)}, 404 # 404 stands for data not found.
    
    def post(self, name):
        for item in items:
            if item['name'] == name:
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

