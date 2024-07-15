from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '3782194d5c1a4f2g69531e2l890k751f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

from project import routes