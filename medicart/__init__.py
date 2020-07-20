from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sagar@localhost/NEW_MEDI'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from medicart import routes