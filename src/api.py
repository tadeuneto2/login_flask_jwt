from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager

from src.routes.login_route import api as ns1, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'tadeu-arthur'

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return "Rota ok - funcionando"


api.add_namespace(ns1)
