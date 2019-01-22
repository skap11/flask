from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class User(object):

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
        self.create_connection()
    
    def create_connection(self):
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    @classmethod
    def get_user_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username = ?'
        result = cursor.execute(query, (username, ))
        row = result.fetchone()
        
        connection.close()

        if row:
            return cls(*row)
        else:
            return None

    @classmethod
    def get_user_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id = ?'
        result = cursor.execute(query, (_id, ))
        row = result.fetchone()

        connection.close()
        
        if row:
            return cls(*row)
        else:
            return None

    def __del__(self):
        self.close_connection()

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    
    parser.add_argument('username', 
        type = str,
        required = True, 
        help = 'This block is required.')

    parser.add_argument('password', 
        type = str,
        required = True, 
        help = 'This block is required.')

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if(User.get_user_by_username(data['username'])):
            return {'message': 'User with that username already exists.'}, 400
            
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = 'INSERT INTO users VALUES(NULL, ?, ?)'
        cursor.execute(query, (data['username'], data['password'], ))

        connection.commit()
        connection.close()
        return {'message': 'User added successfully.'}, 201