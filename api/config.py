import dotenv
import os


dotenv.load_dotenv()

SECRET_KEY = os.environ["FLASK_SECRET_KEY"]

# Flask-Sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\Reel\\api\\db\\hooks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Admin
FLASK_ADMIN_SWATCH = 'slate'

# CORS
CORS_HEADERS = 'Content-Type'

# Basic Auth
BASIC_AUTH_USERNAME = os.environ["ADMIN_AUTH_USERNAME"]
BASIC_AUTH_PASSWORD = os.environ["ADMIN_AUTH_PASSWORD"]
