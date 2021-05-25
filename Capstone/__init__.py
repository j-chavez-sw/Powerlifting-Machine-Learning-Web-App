from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dashboard import init_dash_app


app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'mysecret'
#
#######DASH###########
init_dash_app(app)
######################

#######DATABASE###########
URI = "postgresql+psycopg2://kszehnilxhvbqp:f24a461e28fb2fe47d5b620d87c7375ffa34cba7f4e24d2cdfa50fdbcef9100b@ec2-184-73-198-174.compute-1.amazonaws.com:5432/datc0rmuf010ql"

app.config['SQLALCHEMY_DATABASE_URI'] = URI
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
