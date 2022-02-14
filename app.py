import hashlib
from os import abort

import jsonschema
from uuid import uuid4
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
USERS = {}
SEAYLE_SING = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'create_date': {
            # TODO добавить дату в тип
            'type': 'string'
        },
        'user_name': {
            'type': 'string'
        },
        'password': {
            'type': 'string',
            'pattern': '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        },
    },
    'required': ['title', 'description', 'create_date', 'user_name', 'password']
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



@app.route('/health/', methods=['GET', ])
def check_health():
    return jsonify(status='OK')


class UserView(MethodView):
    # создание нового пользователя
    def new_user(self):
        user_name = request.json.get('user_name')
        password = request.json.get('password')
        if user_name is None or password is None:
            abort(400)
        if User.query. filter_by(user_name = user_name).first() is not None:
            abort(400)
        user = User(user_name=user_name)
        user.hash_password(password)
        db.session.add(user)
        db.session.comit()

    # получения из базы
    def get_adv(self, adv_id):
        # из базы данных
        adv = db.
        user = USERS.get(user_id)
        if user is not None:
            user_data = user.copy()
            user_data.pop('hash_pasw')
            return jsonify(user_data)
    # Выдача всех объявлений
    def get_all(self):
        return ...
    # добавление нового товара
    def new_adv(self):
        user_id = str(uuid4())
        try:
            user_data = dict(request.json)
            jsonschema.validate(user_data, USER_POST)
            pasw = user_data.pop('password')
            hash_pasw = hashlib.md5(pasw.encode()).hexdigest()
            USERS[user_id] = {'hash_pasw': hash_pasw, **user_data}
            return {'id': user_id, **user_data, }
        except jsonschema.ValidationError as er:
            response = jsonify(error=er.message)
            response.status_code = 400
            return response

    # удаление товара
    def del_adv(self, adv_id):
        return ...

    # изменение товара
    def patch_adv(self, adv_id):
        return ...

app.add_url_rule('/advertisement/<adv_id>', view_func=UserView.as_view('get_adv'), methods=['GET'])
app.add_url_rule('/advertisement/get_all', view_func=UserView.as_view('get_all'), methods=['GET'])

app.add_url_rule('/new_user', view_func=UserView.as_view('new_user'), methods=['POST'])
app.add_url_rule('/advertisement/new_adv', view_func=UserView.as_view('new_adv'), methods=['POST'])
app.add_url_rule('/advertisement/del_adv/<adv_id>', view_func=UserView.as_view('del_adv'), methods=['DELETE'])
app.add_url_rule('/advertisement/patch_adv/<adv_id>', view_func=UserView.as_view('patch_adv'), methods=['PATCH'])


# app.add_url_rule('/user/<user_id>', view_func=UserView.as_view('get_user'), methods=['GET'])
# app.add_url_rule('/user/', view_func=UserView.as_view('create_user'), methods=['POST'])

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flask:flask_app@localhost:5432"
app.run(host='127.0.0.1', port=8000)
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
