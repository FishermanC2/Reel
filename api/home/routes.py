from flask import Blueprint, jsonify, session, render_template, send_from_directory
import os

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/favicon.ico')
def favicon():
    from api.server import app
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@bp.route('/alive', methods=['GET', 'POST'])
def alive():
    from api.server import app
    app.logger.info(f'Got alive signal from {session.get('hook_id')}')
    return jsonify(message='Hello')