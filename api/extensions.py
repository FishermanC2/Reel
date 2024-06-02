from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_basicauth import BasicAuth
from flask_socketio import SocketIO
from io import StringIO

# Flask extensions
db = SQLAlchemy()
cors = CORS()
auth = BasicAuth()
socketio = SocketIO()

# output from console redirected
output_buffer = StringIO()

