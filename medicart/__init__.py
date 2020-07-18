from flask import Flask
# from medicart.config import Config
# from medicart.dbconnect import connection
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# app.config.from_object(Config)
app.config['SECRET_KEY'] = 'never-guess'
# cur,db = connection()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicart.db'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from medicart import routes
