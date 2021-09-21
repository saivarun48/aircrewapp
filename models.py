from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cx_Oracle
import os
from config.config import DB_CONNECT_STRING, DB_USER, DB_PASSWORD

# Initialize Oracle Client on MacOS
#cx_Oracle.init_oracle_client(lib_dir="/Users/jeanrodrigues/Downloads/instantclient_19_8/")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://{}:{}@{}'.format(DB_USER,DB_PASSWORD,DB_CONNECT_STRING)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Person(db.Model):

    __tablename__ = 'person'

    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True, unique=False)
    phone = db.Column(db.String(100), nullable=True, unique=False)
    role = db.Column(db.String(100), nullable=True, unique=False)
    attachment = db.Column(db.String(100), nullable=True, unique=False)

    def __repr__(self):
        return '<Persons %r>' % self.name