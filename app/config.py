import dotenv
import os


# TODO: change to only using config or only using .env
dotenv.load_dotenv()

SECRET_KEY = os.environ["FLASK_SECRET_KEY"]

# Flask-Session
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

# Flask-Sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Reel\\app\\db\\hooks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Admin
FLASK_ADMIN_SWATCH = 'slate'
