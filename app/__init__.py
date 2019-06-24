from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/event_management"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'event_management'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)
#mysql = MySQL()
db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
