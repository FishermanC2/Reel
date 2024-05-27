from flask import Blueprint, request, session, jsonify
from api.extensions import db
from .models import Hook

bp = Blueprint('hook', __name__)


@bp.route('/', methods=['GET', 'POST'])
def hook():
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr

    # Get additional fingerprinting data from the request JSON body
    # TODO : move to seperate modules
    """
    data = request.json
    screen_resolution = data.get('screen_resolution')
    timezone = data.get('timezone')
    language = data.get('language')
    browser_plugins = data.get('browser_plugins')
    """

    new_hook = Hook(
        user_agent=user_agent,
        ip_address=ip_address
    )
    db.session.add(new_hook)
    db.session.commit()

    session['hook_id'] = new_hook.id

    return jsonify({'message': f'Hook created with ID {new_hook.id}'}), 201 # TODO : Change to something else