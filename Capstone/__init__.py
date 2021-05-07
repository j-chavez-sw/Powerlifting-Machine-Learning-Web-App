from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

#######DATABASE###########
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
##########################

##########LOGIN###########
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

##########################

from Capstone.error.error_handlers import error_pages
from Capstone.Users.views import users
from Capstone.Core.views import core
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
