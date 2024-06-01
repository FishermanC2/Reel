from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_basicauth import BasicAuth
from flask_socketio import SocketIO

db = SQLAlchemy()
cors = CORS()
auth = BasicAuth()
socketio = SocketIO()

