import config
from os import abort
from datetime import datetime
import jsonschema
from flask import Flask, jsonify, request, g
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from models import User, Advertisement

app = Flask(__name__)
db = SQLAlchemy(app)

SELL_THING = {
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



@app.route('/health/', methods=['GET',])
def check_health():
    return jsonify(status='OK')


class UserView(MethodView):
    auth = HTTPBasicAuth()
    @auth.login_required()
    def login(self):
        return jsonify({'data': f'Hello, {g.user.user_name}'})

    @auth.verify_password
    def verify_password(self, user_name, password):
        user = User.query.filter_by(username=user_name).first()
        if not user or not user.verify_password(password):
            return False
        g.user = user
        return True

    # создание нового пользователя
    # @app.route('/new_user/', methods=['POST'])
    def post(self):
        user_name = request.json.get('user_name')
        password = request.json.get('password')
        if user_name is None or password is None:
            abort(400)
        if User.query.filter_by(username=user_name).first() is not None:
            abort(400)
        user = User(username=user_name)
        user.hash_password(password)
        db.session.add(user)
        db.session.comit()

    # получения из базы
    def get_adv(self):
        # из базы данных
        data = request.args
        #
        # adv = Advertisement.query.filter_by(id=)
        # user = USERS.get(user_id)
        # if user is not None:
        #     user_data = user.copy()
        #     user_data.pop('hash_passw')
        #     return jsonify(user_data)
        return ...
    # Выдача всех объявлений
    def get_all(self):
        return ...
    # добавление нового товара self.verify_password()
    def new_adv(self):
        if self.verify_password():
            try:
                adv_date = dict(request.json)
                jsonschema.validate(adv_date, SELL_THING)
                title = adv_date.pop('title')
                description = adv_date.pop('description')
                user = User.query.filter_by(username=adv_date.pop('user_name')).first()
                adv = Advertisement(title=title,
                                    description=description,
                                    create_date=datetime.now(),
                                    owner=user
                                    )
                db.session.add(adv)
                db.session.comit()
                response = jsonify(title=title,
                                   description=description,
                                   create_date=datetime.now(),
                                   owner=user,
                                   data='Success save')
                response.status_code = 201
                return response
            except jsonschema.ValidationError as er:
                response = jsonify(error=er.message)
                response.status_code = 400
                return response
        response = jsonify(error='Не пройдена верификация пользователя')
        response.status_code = 401
        return response

        # user_id = str(uuid4())
        # try:
        #     user_data = dict(request.json)
        #     jsonschema.validate(user_data, USER_POST)
        #     pasw = user_data.pop('password')
        #     hash_passw = hashlib.md5(pasw.encode()).hexdigest()
        #     USERS[user_id] = {'hash_passw': hash_passw, **user_data}
        #     return {'id': user_id, **user_data, }
        # except jsonschema.ValidationError as er:
        #     response = jsonify(error=er.message)
        #     response.status_code = 400
        #     return response

    # удаление товара
    def del_adv(self, adv_id):
        if self.verify_password():
            return ...
        return ...

    # изменение товара
    def patch_adv(self, adv_id):
        if self.verify_password():
            return ...
        return ...


app.add_url_rule('/advertisement/get', view_func=UserView.as_view('get_adv'), methods=['GET'])
app.add_url_rule('/advertisement/get_all/', view_func=UserView.as_view('get_all'), methods=['GET'])

app.add_url_rule('/api/new_user/', view_func=UserView.as_view('new_user'), methods=['POST'])
app.add_url_rule('/advertisement/new_adv/', view_func=UserView.as_view('new_adv'), methods=['POST'])
app.add_url_rule('/advertisement/del_adv/<adv_id>', view_func=UserView.as_view('del_adv'), methods=['DELETE'])
app.add_url_rule('/advertisement/patch_adv/<adv_id>', view_func=UserView.as_view('patch_adv'), methods=['PATCH'])

app.add_url_rule('/login', view_func=UserView.as_view('login'))


# app.add_url_rule('/user/<user_id>', view_func=UserView.as_view('get_user'), methods=['GET'])
# app.add_url_rule('/user/', view_func=UserView.as_view('create_user'), methods=['POST'])

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flask:12345678@localhost:5432/flask_app"
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRE_URI)
app.run(host='127.0.0.1', port=8000)
