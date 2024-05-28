from flask import Blueprint, request, session, json
from flask_cors import cross_origin
from api.extensions import db
from .models import Hook

bp = Blueprint('hook', __name__)


@bp.route('/')
@cross_origin(supports_credentials=True)
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

    from ..server import app
    app.logger.info(f'Hook created with ID {new_hook.id}')

    return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 