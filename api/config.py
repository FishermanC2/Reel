import dotenv
import os


# TODO: change to only using config or only using .env
dotenv.load_dotenv()

SECRET_KEY = os.environ["FLASK_SECRET_KEY"]

# Flask-Sqlalchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\Reel\\api\\db\\hooks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-Admin
FLASK_ADMIN_SWATCH = 'slate'

CORS_HEADERS = 'Content-Type'

