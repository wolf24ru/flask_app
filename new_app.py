import jsonschema
from os import abort
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from passlib.apps import custom_app_context as pwd_context

SEAYLE_SING = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'user_name': {
            'type': 'string'
        },
        'password': {
            'type': 'string',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        },
    },
    'required': ['title', 'description', 'user_name', 'password']
}
NEW_USER = {
    'type': 'object',
    'properties': {
        'user_name': {
            'type': 'string'
        },
        'password': {
            'type': 'string',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        }
    },
    'required': ['user_name', 'password']
}


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flask:12345678@localhost:5432/flask_app"
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash =db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Advertisement(db.Model):
    ...

@app.route('/health/', methods=['GET'])
def check_health():
    return jsonify(status='ok')

class UserView(MethodView):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        response = jsonify(**user)
        return response

    def post(self):
        try:
            jsonschema.validate(request.json, NEW_USER)
            user_name = request.json['user_name']
            password = request.json['password']
            if user_name is None or password is None:
                abort(400)
            if User.query.filter_by(username=user_name).first() is not None:
                abort(400)
            user = User(username=user_name)
            user.hash_password(password)
            db.session.add(user)
            db.session.comit()
            id = User.query.filter_by(username=user_name).first()
            response = jsonify(data='ok', **request.json)
            response.status_code = 201
            return response
        except jsonschema.ValidationError as er:
            response = jsonify(error=er.message)
            response.status_code = 400
            return response


# class AdvertisementView(MethodView):
#     def get(self):
#
#         return
#
#     def post(self):
#         return
#
#     def delete(self, adv_id):
#         return
#
#     def patch(self, adv_id):
#         return
app.add_url_rule('/new_user/', view_func=UserView.as_view('new_user'), methods=['POST'])
app.add_url_rule('/get_use/<user_id>', view_func=UserView.as_view('get_user'), methods=['GET'])
app.run(host='127.0.0.1', port=8000)

# https://github.com/tabelsky/flask_example
