from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.POSTGRE_URI
db = SQLAlchemy(app)
