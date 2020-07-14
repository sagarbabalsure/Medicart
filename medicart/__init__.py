from flask import Flask
# from medicart.config import Config
from medicart.dbconnect import connection

app = Flask(__name__)
# app.config.from_object(Config)
app.config['SECRET_KEY'] = 'never-guess'
cur,db = connection()

from medicart import routes