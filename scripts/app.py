from flask import Flask, jsonify, request


app = Flask(__name__)

stores = [
    {
        'name': 'My store',
        'items': [
            {
                'name': 'My item',
                'price': '14$'
            }
        ]
    }
]

@app.route('/')
def home():
    return 'Hello, world!'

# Post request to create a store
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store =  {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store) 

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'errorMessage': 'Store not found'})

# GET /stores
@app.route('/stores')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'errorMessage': 'Store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'errorMessage': 'Store not found'})

app.run(port=5000)