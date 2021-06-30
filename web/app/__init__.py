from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from app.forms import *

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from . import routes


