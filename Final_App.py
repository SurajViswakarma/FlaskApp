from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from werkzeug.security import safe_str_cmp


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


my_user = [
    User(1,'suraj','suraj1234'),
    User(2,'anand','anand1234')
]

userid_mapping = {u.id: u for u in my_user}
username_mapping = {u.username: u for u in my_user}

def authenticate(username, password):
    search_user = username_mapping.get(username, None)
    if search_user and safe_str_cmp(search_user.password.encode('UTF-8'), password.encode('UTF-8')):
        return search_user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)


app = Flask(__name__)
api = Api(app)
api.security_key = 'suraj'
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

store = [
    {
        'name':'store1',
        'owner': 'ram'
    }
]

class All_Store(Resource):
    #@jwt_required()
    def get(self):
        return {'All_Store': store}, 200


class Add_Store(Resource):
    def post(self, name):
        existing_store = next(filter(lambda x: x['name'] == name ,store), None)
        if existing_store is not None:
            return 'store already exists', 400

        new_store = {'name':name, 'owner':'raju'}
        store.append(new_store)
        return new_store




api.add_resource(All_Store,'/')
api.add_resource(Add_Store,'/<string:name>')
app.run(debug = True, port = 5000)
