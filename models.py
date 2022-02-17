from passlib.apps import custom_app_context as pwd_context
from new_app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    advertisements = db.relationship('Advertisement', backref='users', lazy=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def to_dict(self):
        return {
            'user_id': self.id,
            'user_name': self.username,
            # TODO нормальное подключение и отображение
            'advertisements': self.advertisements
        }


class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    create_date = db.Column(db.DateTime(), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'create_date': self.create_date,
            'owner': self.owner
        }
