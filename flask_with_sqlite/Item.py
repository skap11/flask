import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help='This field cannot be left blank')
    
    def get(self, name):
        try:
            row = self.get_by_name(name)
            if row:
                return row
            return {'item': None}, 404
        except Exception as e:
            print e
            return {'errorMessage': 'An error occurred while fetching the data from the database.'}, 500
    
    @classmethod
    def get_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        
        connection.close()
        
        if row:
            return {'name': row[0], 'price': row[1]}
        
    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES(?, ?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if self.get_by_name(name):
            return {'errorMessage': 'Resource with name {} already exists.'.format(name)}, 400
        
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert_item(item)
            return item, 201
        except:
            return {'errorMessage': 'An error occurred while inserting the data into database.'}, 500
        
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        try:
            row = self.get_by_name(name)
            if row:
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()

                query = 'UPDATE items SET price = ? WHERE name = ?'
                cursor.execute(query, (data['price'], name))

                connection.commit()
                connection.close()
                row['price'] = data['price']
                return row

            new_item = {'name': name, 'price': data['price']}    
            self.insert_item(new_item)
            return new_item
        except:
            return {'errorMessage': 'An error occurred while inserting the data into database.'}, 500
    
    @jwt_required()
    def delete(self, name):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = 'DELETE FROM items WHERE name = ?'
            cursor.execute(query, (name, ))

            connection.commit()
            connection.close()
            return {'message': 'item deleted'}
        except:
            return {'errorMessage': 'An error occurred while inserting the data into database.'}, 500

class Items(Resource):
    def get(self):
        try:
            items = []
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = 'SELECT * FROM items'
            result = cursor.execute(query)
            rows = result.fetchall()
            connection.commit()
            connection.close()

            for row in rows:
                items.append({'name': row[0], 'price': row[1]})

            return {'items': items}
        except Exception as e:
            print e
            return {'errorMessage': 'An error occurred while inserting the data into database.'}, 500