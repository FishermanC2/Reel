from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/xss', methods=['GET', 'POST'])
def xss():
    return request.args.get('payload')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

app.run(host="127.0.0.1", port=5001)