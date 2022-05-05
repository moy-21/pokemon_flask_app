from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# Register Plug-ins
login = LoginManager(app)

#init my Database manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Configure Some Settings
login.login_view = 'login'
login.login_message = 'You have to log in!'
login.login_message_category='warning'

from app import routes, models