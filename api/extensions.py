from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_basicauth import BasicAuth

db = SQLAlchemy()
cors = CORS()
auth = BasicAuth()

