from flask import Blueprint
from flask_socketio import send, emit
from ..extensions import socketio, output_buffer, auth

bp = Blueprint('console', __name__)

@socketio.on('connect')
def test_connect():
    if not auth.authenticate():
        return
    
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('message')
def pipe_console():
    # Allow only admin to access websocket
    curr_buffer = output_buffer.getvalue()
    lines = curr_buffer.splitlines()
    for line in lines:
        send(line)
    output_buffer.truncate(0)
    output_buffer.seek(0)
