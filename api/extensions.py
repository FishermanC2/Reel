from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_basicauth import BasicAuth

db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS()
auth = BasicAuth()

