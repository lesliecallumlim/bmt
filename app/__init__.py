from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import babel

app = Flask(__name__)
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)
bootstrap = Bootstrap(app)
login = LoginManager(app)

def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="dd-MMM-y"
    return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime

from app import routes, models

