from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'mysecret'
#
#######DATABASE###########
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# Migrate(app, db)
##########################

#######DATABASE2###########
URI = "postgresql://kszehnilxhvbqp:f24a461e28fb2fe47d5b620d87c7375ffa34cba7f4e24d2cdfa50fdbcef9100b@ec2-184-73-198-174.compute-1.amazonaws.com:5432/datc0rmuf010ql"

app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
# from sqlalchemy import create_engine
#
# engine = create_engine(URI)
#
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Date
#
# Base = declarative_base()
#
# class User(Base):
#
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50), unique=True, index=True)
#     username = db.Column(db.String(50), unique=True, index=True)
#     password_hash = db.Column(db.String(128))
#
#
#     def __repr__(self):
#         return f"Username {self.username}"
#
# Base.metadata.create_all(engine)

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
