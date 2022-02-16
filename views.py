from os import abort
from datetime import datetime
import jsonschema
from flask import jsonify, g, request
from flask.views import MethodView
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

from models import User, Advertisement
from new_app import db, app
from schema import NEW_USER, NEW_THING


@app.route('/health/', methods=['GET'])
def check_health():
    return jsonify(status='ok')


class UserView(MethodView):
    auth = HTTPBasicAuth()

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

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

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        response = jsonify(user_id=user.id,
                           user_name=user.username,
                           advertisement=user.advertisements)
        response.status_code = 200
        return response

    def post(self,):
        try:
            jsonschema.validate(request.json, NEW_USER)
            user_name = request.json['user_name']
            password = request.json['password']
            self.hash_password(password)
            if user_name is None or password is None:
                response = jsonify(msg='user name or password is none')
                response.status_code = 400
                return response
            if User.query.filter_by(username=user_name).first() is not None:
                response = jsonify(msg='user exist')
                response.status_code = 400
                return response
            user = User(username=user_name)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            user_response = User.query.filter_by(username=user_name).first()
            response = jsonify(data='user create', user_id=user_response.id, user_name=user_response.username, )
            response.status_code = 201
            return response
        except jsonschema.ValidationError as er:
            response = jsonify(error=er.message)
            response.status_code = 400
            return response



class AdvertisementView(MethodView):
    auth = HTTPBasicAuth()

    @auth.verify_password
    def verify_password(self, user_name, password):
        user = User.query.filter_by(username=user_name).first()
        if not user or not user.verify_password(password):
            return False
        g.user = user
        return True

    def get(self):
        adv_all = Advertisement.query.all()
        response = jsonify(adv_all)
        response.status_code = 200
        return response

    def get(self, adv_id):
        adv_all = Advertisement.query.filter+by(id)
        response = jsonify(adv_all)
        response.status_code = 200
        return response

    def post(self):
        try:
            jsonschema.validate(request.json, NEW_THING)
            user_name = request.json['user_name']
            password = request.json['password']
            if self.verify_password(user_name, password):
                title = request.json['title']
                description = request.json['description']
                date = datetime.now()
                user = User.query.filter_by(username=user_name).first()
                adv = Advertisement(title=title,
                                    description=description,
                                    create_date=date,
                                    owner=user.id)
                db.session.add(adv)
                db.session.commit()
                response = jsonify(data='Advertisement successful create',
                                   title=title,
                                   description=description,
                                   create_date=date,
                                   owner=user.username
                                   )
                response.status_code = 201
                return response
        except jsonschema.ValidationError as er:
            response = jsonify(error=er.message)
            response.status_code = 400
            return response

    def delete(self, adv_id):
        return

    def patch(self, adv_id):
        return


app.add_url_rule('/new_user/', view_func=UserView.as_view('new_user'), methods=['POST'])
app.add_url_rule('/get_use/<user_id>', view_func=UserView.as_view('get_user'), methods=['GET'])

app.add_url_rule('/adv_new/', view_func=AdvertisementView.as_view('adv_new'), methods=['POST'])
app.add_url_rule('/adv_new/<adv_id>', view_func=AdvertisementView.as_view('get_adv_id'), methods=['GET'])
app.add_url_rule('/adv/', view_func=AdvertisementView.as_view('get_adv'), methods=['GET'])
